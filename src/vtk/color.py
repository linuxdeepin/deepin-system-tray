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

import gtk
import cairo
import pango

def alpha_color_hex_to_cairo((color, alpha)):
    '''
    Convert alpha color (color, alpha) to cairo color (r, g, b, alpha).
    
    @param color: Hex color.
    @param alpha: Alpha value.
    @return: Return cairo value (red, green, blue, alpha).
    '''
    (r, g, b) = color_hex_to_cairo(color)
    return (r, g, b, alpha)
    
def color_hex_to_cairo(color):
    """ 
    Convert a html (hex) RGB value to cairo color. 
     
    @param color: The color to convert. 
    @return: A color in cairo format, (red, green, blue). 
    """ 
    gdk_color = gtk.gdk.color_parse(color)
    return (gdk_color.red / 65535.0, gdk_color.green / 65535.0, gdk_color.blue / 65535.0)
