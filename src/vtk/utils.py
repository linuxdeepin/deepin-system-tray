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


import cairo
import math



def cairo_popover (widget, 
                   surface_context, 
                   trayicon_x, trayicon_y, 
                   w, h, 
                   radius,
                   arrow_width, arrow_height, offs=0):
    cr = surface_context
    x = trayicon_x
    y = trayicon_y
    w = w - trayicon_x * 2
    h = h - trayicon_x * 2 
    #
    if (offs + 50) > (w + 20):
        offs = (w + 20) - 15 - arrow_width
    if (offs < 17):
        offs = 17
    # draw.
    cr.arc (x + radius,
            y + arrow_height + radius,
            radius,
            math.pi,
            math.pi * 1.5)
    cr.line_to(offs, y + arrow_height)
    cr.rel_line_to(arrow_width / 2.0, -arrow_height)
    cr.rel_line_to(arrow_width / 2.0, arrow_height)
    cr.arc (x + w - radius,
            y + arrow_height + radius,
            radius,
            math.pi * 1.5,
            math.pi * 2.0)
    cr.arc(x + w - radius,
           y + h - radius,
           radius,
           0,
           math.pi * 0.5)
    cr.arc(x + radius,
           y + h - radius,
           radius,
           math.pi * 0.5,
           math.pi)
    
    cr.close_path()
    
    
    
def new_surface(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    surface_context = cairo.Context(surface)
    return  surface, surface_context
    
