#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <linux/target_core_user.h>

#define SCSI_NO_SENSE 0x00
#define SCSI_CHECK_CONDITION 0x02

int handle_device_events(int fd, void *map);

int main()
{
	int fd, dev_fd;
	char buf[256];
	unsigned long long map_len;
	void *map;

	unsigned int ret = 0;

	fd = open("/sys/class/uio/uio0/name", O_RDONLY);
	ret = read(fd, buf, sizeof(buf));
	close(fd);
	buf[ret-1] = '\0'; /* null-terminate and chop off the \n */

	/* we only want uio devices whose name is a format we expect */
	if (strncmp(buf, "tcm-user", 8))
	        exit(-1);

	/* Further checking for subtype also needed here */

	fd = open("/sys/class/uio/%s/maps/map0/size", O_RDONLY);
	ret = read(fd, buf, sizeof(buf));
	close(fd);
	buf[ret-1] = '\0'; /* null-terminate and chop off the \n */

	map_len = strtoull(buf, NULL, 0);

	dev_fd = open("/dev/uio0", O_RDWR);
	map = mmap(NULL, map_len, PROT_READ|PROT_WRITE, MAP_SHARED, dev_fd, 0);

	while (1) {
	  char buf[4];

	  int ret = read(dev_fd, buf, 4); /* will block */

	  handle_device_events(dev_fd, map);
	}

	return 0;

}

int handle_device_events(int fd, void *map)
{
  struct tcmu_mailbox *mb = map;
  struct tcmu_cmd_entry *ent = (void *) mb + mb->cmdr_off + mb->cmd_tail;
  int did_some_work = 0;

  /* Process events from cmd ring until we catch up with cmd_head */
  while (ent != (void *)mb + mb->cmdr_off + mb->cmd_head) {

    if (tcmu_hdr_get_op(ent->hdr.len_op) == TCMU_OP_CMD) {
      uint8_t *cdb = (void *)mb + ent->req.cdb_off;
      bool success = true;

      /* Handle command here. */
      printf("SCSI opcode: 0x%x\n", cdb[0]);

      /* Set response fields */
      if (success)
        ent->rsp.scsi_status = SCSI_NO_SENSE;
      else {
        /* Also fill in rsp->sense_buffer here */
        ent->rsp.scsi_status = SCSI_CHECK_CONDITION;
      }
    }
    else if (tcmu_hdr_get_op(ent->hdr.len_op) != TCMU_OP_PAD) {
      /* Tell the kernel we didn't handle unknown opcodes */
      ent->hdr.uflags |= TCMU_UFLAG_UNKNOWN_OP;
    }
    else {
      /* Do nothing for PAD entries except update cmd_tail */
    }

    /* update cmd_tail */
    mb->cmd_tail = (mb->cmd_tail + tcmu_hdr_get_len((__u32)&ent->hdr)) % mb->cmdr_size;
    ent = (void *) mb + mb->cmdr_off + mb->cmd_tail;
    did_some_work = 1;
  }

  /* Notify the kernel that work has been finished */
  if (did_some_work) {
    uint32_t buf = 0;

    write(fd, &buf, 4);
  }

  return 0;
}