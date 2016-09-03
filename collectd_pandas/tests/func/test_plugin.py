# -*- coding: utf-8 -*-

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

from unittest2 import TestCase

import collectd  # pylint: disable=import-error

from collectd_pandas.tests.match import attributes
from collectd_pandas.tests.mocking import patch_logger


class TestPlugin(TestCase):

    @staticmethod
    @patch_logger('collectd_pandas.plugin.LOG')
    def test_dispach_values(logger):
        "test register_callbaks method"

        expected = attributes(
            type='counter',
            plugin='my_plugin',
            host='my_host',
            time=1472890813.3816543,
            interval=10.0,
            values=[10])

        values = collectd.Values(**expected.as_dict())
        values.dispatch()

        logger.assert_has_record(
            "Write: %r", args=(expected,), level=logging.DEBUG)
