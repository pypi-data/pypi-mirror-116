#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Afshin T. Darian.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..life import LifeWidget


def test_life_creation_blank():
    w = LifeWidget()
    assert w.value == 'Hello World'
