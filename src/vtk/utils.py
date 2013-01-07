#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import math

def cairo_rounded_rectangle(cr, x, y, width, height, radius):
    cr.move_to (x + radius, y)
    cr.arc (x + width - radius, 
            y + radius, 
            radius, 
            math.pi * 1.5,
            math.pi * 2)
    cr.arc (x + width - radius,
            y + radius,
            radius,
            0,
            math.pi * 0.5)
    cr.arc (x + radius,
            y + height - radius,
            radius,
            math.pi * 0.5,
            math.pi)
    cr.arc (x + radius,
            y + radius,
            radius,
            math.pi,
            math.pi * 1.5)
    cr.close_path()

