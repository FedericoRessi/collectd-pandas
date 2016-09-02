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


LOGGER = logging.getLogger(__name__)


class Plugin(object):

    config = None

    @classmethod
    def register(cls):
        assert collectd is not None

        # pylint: disable=import-error
        collectd.info("Register plugin: %{}".format(cls))

        instance = cls()
        collectd.register_config(instance.configure)
        collectd.register_init(instance.initialize)
        collectd.register_write(instance.write)
        collectd.register_flush(instance.flush)
        collectd.info("Plugin registered.")
        return instance

    def configure(self, config):
        # pylint: disable=import-error,no-self-use
        LOGGER.debug("Configure plugin: %r", config)

    @staticmethod
    def initialize():
        LOGGER.debug("Initialize plugin.")

    @staticmethod
    def write(values):
        LOGGER.debug("Write: %r", values)

    @staticmethod
    def flush(*args, **kwargs):
        LOGGER.debug("Flush: %r, %r", args, kwargs)


if collectd is not None:
    PLUGIN = Plugin.register()
