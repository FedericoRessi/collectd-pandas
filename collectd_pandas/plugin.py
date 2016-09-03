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
"Main plugin entry point."

import logging

try:
    import collectd
except ImportError:
    collectd = None

from collectd_pandas.logger import CollectdLogHandler


LOG = logging.getLogger(__name__)
LOG_FORMAT = '%(levelname)-7s | %(name)s | %(message)s'


class Plugin(object):

    config = None

    @classmethod
    def register(cls):
        assert collectd is not None

        LOG.info("Register plugin: %s", cls)

        log_handler = CollectdLogHandler(collectd=collectd)
        log_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logging.getLogger('collectd_pandas').addHandler(log_handler)

        instance = cls()
        collectd.register_config(instance.configure)
        collectd.register_init(instance.initialize)
        collectd.register_write(instance.write)
        LOG.info("Plugin registered as: %r.", instance)
        return instance

    def configure(self, config):
        # pylint: disable=import-error,no-self-use
        LOG.debug("Configure plugin: %r", config)

    @staticmethod
    def initialize():
        LOG.debug("Initialize plugin.")

    @staticmethod
    def write(values):
        LOG.debug("Write: %r", values)


if collectd is not None:
    PLUGIN = Plugin.register()
