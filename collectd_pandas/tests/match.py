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

import fnmatch
from json import loads
import re

import six

__unittest = True  # pylint: disable=invalid-name


def json(obj):
    return MatchJson(obj)


class MatchJson(object):

    def __init__(self, obj):
        self._obj = obj

    def __eq__(self, json_text):
        return self._obj == loads(json_text)

    def __repr__(self):
        return "MatchJson({})".format(repr(self._obj))


def wildcard(text):
    return MatchWildcard(text)


class MatchWildcard(object):

    def __init__(self, obj):
        self._text = text = str(obj)
        self._reg = re.compile(fnmatch.translate(text))

    def __eq__(self, obj):
        return self._reg.match(str(obj))

    def __repr__(self):
        return "MatchWildcard({})".format(self._text)


def attributes(**attribs):
    return MatchAttributes(**attribs)


class MatchAttributes(object):

    def __init__(self, **attribs):
        self._attribs = sorted(six.iteritems(attribs))

    def __eq__(self, obj):
        for name, expected in self._attribs:
            if expected != getattr(obj, name):
                return False
        return True

    def __repr__(self):
        attribs = ", ".join("{}={}".format(name, repr(expected))
                            for name, expected in self._attribs)
        return "MatchAttributes({})".format(attribs)

    def from_other(self, obj):
        return MatchAttributes(
            **{name: getattr(obj, name) for name, _ in self._attribs})

    def as_dict(self):
        return dict(self._attribs)
