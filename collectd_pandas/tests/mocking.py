# -*- coding: utf-8 -*-

# Copyright (c) 2016 Intel Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from time import clock

from mock import mock, patch, ANY
from six.moves import queue

from collectd_pandas.tests import match


mock.__unittest = True  # pylint: disable=protected-access


def patch_logger(target, level=logging.NOTSET, timeout=5.):
    name, _ = target.rsplit('.', 1)

    def new_logger():
        return MockLogger(name, level=level, timeout=timeout)

    return patch(target, new_callable=new_logger)


class MockLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET, timeout=5.):
        super(MockLogger, self).__init__(name=name, level=level)
        self.records = queue.Queue()
        self.timeout = timeout

    def handle(self, record):
        super(MockLogger, self).handle(record)
        self.records.put(record)

    def assert_has_record(self, msg, args=ANY, level=ANY, exc_info=ANY):
        expected = match.attributes(
            name=self.name, msg=msg, levelno=level, args=args,
            exc_info=exc_info)
        timeout = self.timeout
        end = clock() + timeout
        records = []
        while timeout >= 0.:
            try:
                record = self.records.get(timeout=timeout)
            except queue.Empty:
                break
            else:
                if record == expected:
                    return record
                records.append(repr(expected.from_other(record)))
                timeout = end - clock()

        raise AssertionError("Record not found:\n"
                             "  - expected:\n\t{}\n"
                             "  - found:\n\t{}".format(
                                 expected, '\n\t'.join(records)))
