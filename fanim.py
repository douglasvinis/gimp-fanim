#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Vinicius
  douglvini@gmail.com

  Distributed under the terms of GNU GPL v3 (or lesser GPL) license.

FAnim:
This module register the FAnim modules into GIMP.

"""
from gimpfu import register, main
from fanim_timeline import timeline_main

AUTHOR = "Douglas Vinicius <douglvini@gmail.com"
COPYRIGHT = "Douglas Vinicius"
YEAR = "2016"

# register the timeline.
register(
        "python_foo_fanim_timeline",
        "Window to manage frames and playback of animations",
        "Window to manage frames and playback of animations",
        AUTHOR,
        COPYRIGHT,
        YEAR,
        "<Image>/FAnim/Image Timeline",
        "*",
        [],[],timeline_main
)
main()
