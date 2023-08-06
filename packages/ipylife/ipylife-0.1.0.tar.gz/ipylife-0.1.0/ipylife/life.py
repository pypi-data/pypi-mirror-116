#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Afshin T. Darian.
# Distributed under the terms of the Modified BSD License.

"""
A Jupyter Widget for Conway's Game of Life
"""

from ipywidgets import DOMWidget
from traitlets import Unicode
from ._frontend import module_name, module_version


class LifeWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('LifeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('LifeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
