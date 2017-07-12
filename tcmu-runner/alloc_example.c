/*
 * NOTE
 *
 * This is the rewritten standard handler example for tcmu-runner
 * Unlike original version (file_example.c) this handler doesn't 
 * create file and doesn't write and read data to (from) it.
 * This handler uses it's own allocated memory as storage
 */

/*
 * Copyright 2014, Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
*/

/*
 * Example code to demonstrate how a TCMU handler might work.
 *
 * Using the example of backing a device by a file to demonstrate:
 *
 * 1) Registering with tcmu-runner
 * 2) Parsing the handler-specific config string as needed for setup
 * 3) Opening resources as needed
 * 4) Handling SCSI commands and using the handler API
 */

#define _GNU_SOURCE
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <endian.h>
#include <errno.h>
#include <scsi/scsi.h>

#include "scsi_defs.h"
#include "tcmu-runner.h"

struct alloc_state {
	char * buf;
	ssize_t ptr;
	ssize_t size;
};


static bool alloc_check_config(const char *cfgstring, char **reason)
{
	/* 
	 * We need no cfgstring path to any file
	 * Because we operate with allocated memory inside this handler
	 */

	/*
	 * Or maybe ask for buf size in config?
	 */

	return true;
}

static int alloc_open(struct tcmu_device *dev)
{
	printf(">>> [ALLOC] alloc_open\n");

	struct alloc_state * state;

	state = calloc(1, sizeof(*state));
	if (!state)
		return -ENOMEM;

	tcmu_set_dev_private(dev, state);

	state->buf = malloc(sizeof(char) * 4096); // just for a while
	state->size = 4096;
	state->ptr = 0;

	if (!state->buf)
		return -ENOMEM;

	/*
	 * Need to allocate some memory at start??
	 */

	return 0;
}

static void alloc_close(struct tcmu_device *dev)
{
	printf(">>> [ALLOC] alloc_close\n");

	struct alloc_state *state = tcmu_get_dev_private(dev);

	if (state->buf != NULL)
		free(state->buf); // clear memory
	free(state);
}

static int alloc_read(struct tcmu_device *dev, struct tcmulib_cmd *cmd,
		     struct iovec *iov, size_t iov_cnt, size_t length,
		     off_t offset)
{

	printf(">>> [ALLOC] alloc_read\n");
	printf(">>> [ALLOC] command: ");
	int bytes = tcmu_get_cdb_length(cmd->cdb);
	for (int i = 0; i < bytes; i++) {
		printf("%x ", cmd->cdb[i]);
	}
	printf("\n");

	struct alloc_state *state = tcmu_get_dev_private(dev);

	int amount = 0;
	if (iov->iov_len > state->size) {
		amount = state->size;
	} else {
		amount = iov->iov_len;
	}

	memcpy(iov->iov_base, state->buf, amount);

	ssize_t ret;
	ret = SAM_STAT_GOOD;
	cmd->done(dev, cmd, ret);
	return 0;
}

static int alloc_write(struct tcmu_device *dev, struct tcmulib_cmd *cmd,
		      struct iovec *iov, size_t iov_cnt, size_t length,
		      off_t offset)
{

	printf(">>> [ALLOC] alloc_write\n");
	printf(">>> [ALLOC] command: ");
	int bytes = tcmu_get_cdb_length(cmd->cdb);
	for (int i = 0; i < bytes; i++) {
		printf("%x ", cmd->cdb[i]);
	}
	printf("\n");

	struct alloc_state *state = tcmu_get_dev_private(dev);

	int amount = 0;
	if (iov->iov_len > state->size) {
		amount = state->size;
	} else {
		amount = iov->iov_len;
	}

	memcpy(state->buf, iov->iov_base, amount);

	ssize_t ret;
	ret = SAM_STAT_GOOD;
	cmd->done(dev, cmd, ret);
	return 0;
}

static int alloc_flush(struct tcmu_device *dev, struct tcmulib_cmd *cmd)
{
	printf(">>> [ALLOC] alloc_flush\n");
	printf("	command: 0x%x\n", cmd->cdb[0]);

	printf(">>> [ALLOC] command: ");
	int bytes = tcmu_get_cdb_length(cmd->cdb);
	for (int i = 0; i < bytes; i++) {
		printf("%x ", cmd->cdb[i]);
	}
	printf("\n");

	int ret;
	ret = SAM_STAT_GOOD;
	cmd->done(dev, cmd, ret);
	return 0;
}

static const char alloc_cfg_desc[] =
	"You don't need config for alloc handler";

static struct tcmur_handler alloc_handler = {
	.cfg_desc = alloc_cfg_desc,

	.check_config = alloc_check_config,

	.open = alloc_open,
	.close = alloc_close,
	.read = alloc_read,
	.write = alloc_write,
	.flush = alloc_flush,
	.name = "Handler with allocated memory",
	.subtype = "alloc",
	.nr_threads = 1,
};

/* Entry point must be named "handler_init". */
int handler_init(void)
{
	printf(">>> [ALLOC] handler_init\n");

	return tcmur_register_handler(&alloc_handler);
}
