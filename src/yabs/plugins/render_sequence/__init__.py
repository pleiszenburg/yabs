# -*- coding: utf-8 -*-

from typing import Any, Dict

from typeguard import typechecked

from .sequence import Sequence

@typechecked
def run(context: Dict, options: Any = None):

    _ = Sequence(context, options)
