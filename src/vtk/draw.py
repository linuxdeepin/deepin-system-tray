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

from constant import DEFAULT_FONT, DEFAULT_FONT_SIZE
from color import color_hex_to_cairo 
import cairo
import pango
import pangocairo




def draw_pixbuf(cr, pixbuf, x, y, alpha=1.0):
    cr.set_source_pixbuf(pixbuf, x, y)
    cr.paint_with_alpha(1.0)

def draw_text(cr, text, x, y, 
              text_size=DEFAULT_FONT_SIZE,
              text_color="#FFFFFF",
              text_font=DEFAULT_FONT,
              alignment=pango.ALIGN_LEFT,
              pango_list=None):
    cr.set_source_rgb(*color_hex_to_cairo(text_color)) 

    context = pangocairo.CairoContext(cr)
    layout = context.create_layout()
    layout.set_font_description(pango.FontDescription("%s %s" % (text_font, text_size)))
    layout.set_text(text) 
    # add pango list attributes.
    if pango_list:
        layout.set_attributes(pango_list)
    cr.move_to(x, y)
    context.update_layout(layout)
    context.show_layout(layout)

def draw_tray_text(cr, text, x, y, w, h, 
                  text_size=DEFAULT_FONT_SIZE,
                  text_color="#000000",
                  text_font=DEFAULT_FONT):
    context = pangocairo.CairoContext(cr)
    layout = context.create_layout()
    layout.set_font_description(pango.FontDescription("%s %s" % (text_font, text_size)))
   
    cr.set_source_rgb(*color_hex_to_cairo(text_color)) 
    layout.set_text(text)

    cr.move_to(x, y)
    cr.save()       
    cr.layout_path(layout)
    cr.set_line_width(1)   
    cr.stroke_preserve()
    cr.stroke()               
    cr.restore()
    cr.set_source_rgb(1, 1, 1)
    cr.set_operator(cairo.OPERATOR_OVER)               
    #

    cr.save()
    cr.rectangle(x, y, w, h)
    cr.clip()       
    #
    cr.move_to(x, y)       
    context.show_layout(layout)
        
