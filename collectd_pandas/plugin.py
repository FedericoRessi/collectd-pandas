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


LOGGER = logging.getLogger(__name__)


class Plugin(object):

    config = None

    @classmethod
    def register(cls):
        # pylint: disable=import-error
        LOGGER.debug("Register plugin: %r", cls)

        import collectd

        plugin = cls(collectd=collectd)
        collectd.register_config(plugin.configure)
        collectd.register_init(plugin.initialize)
        collectd.register_init(plugin.write)
        LOGGER.debug("Plugin registered.")

    def configure(self, config):
        # pylint: disable=import-error,no-self-use
        LOGGER.debug("Configure plugin: %r", config)

    def initialize(self):
        if self.config:
            raise RuntimeError("Missing plugin configurarion.")

    def write(self, *args):
        # pylint: disable=unused-argument, no-self-use
        LOGGER.error("Plugin not initialized.")

    def __init__(self, collectd):
        self.collectd = collectd
