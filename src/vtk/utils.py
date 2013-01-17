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
import gtk
import cairo
import pangocairo
import pango
import math
import os



def cairo_popover (widget, 
                   surface_context, 
                   trayicon_x, trayicon_y, 
                   trayicon_w, trayicon_h, 
                   radius,
                   arrow_width, arrow_height, offs=0, pos_type=gtk.POS_TOP):
    cr = surface_context
    x = trayicon_x
    y = trayicon_y
    w = trayicon_w - trayicon_x * 2
    h = trayicon_h - trayicon_x * 2 
    #
    if (offs + 50) > (w + 20):
        offs = (w + 20) - 15 - arrow_width
    if (offs < 17):
        offs = 17
    # set position top, bottom.
    if pos_type == gtk.POS_BOTTOM:
        y = y - arrow_height 
        h -= y  
    # draw.
    cr.arc (x + radius,
            y + arrow_height + radius,
            radius,
            math.pi,
            math.pi * 1.5)

    if pos_type == gtk.POS_TOP:
        y_padding = y + arrow_height
        arrow_height_padding = arrow_height 
        cr.line_to(offs, y_padding) 
        cr.rel_line_to(arrow_width / 2.0, -arrow_height_padding)
        cr.rel_line_to(arrow_width / 2.0, arrow_height_padding)

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
    if pos_type == gtk.POS_BOTTOM:
        y_padding = trayicon_y + h - arrow_height 
        arrow_height_padding = arrow_height
        cr.line_to(offs + arrow_width, y_padding) 
        cr.rel_line_to(-arrow_width / 2.0, arrow_height_padding)
        cr.rel_line_to(-arrow_width / 2.0, -arrow_height_padding)
        
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

def propagate_expose(widget, event):
    if hasattr(widget, "get_child") and widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)
        
def get_text_size(text, text_size=DEFAULT_FONT_SIZE, text_font=DEFAULT_FONT):
    try:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        cr = cairo.Context(surface)
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        temp_font = pango.FontDescription("%s %s" % (text_font, text_size))
        layout.set_font_description(temp_font)
        layout.set_text(text)
        return layout.get_pixel_size()
    except:
        return (0, 0)

def get_home_path():
    return os.path.expandvars("$HOME")

def get_config_path():
    return os.path.join(get_home_path(), ".config/deepin-system-settings/tray")

def get_config_file():
    return os.path.join(get_config_path(), "config.ini")

def config_path_check():
    if os.path.exists(get_config_path()):
        return True
    else:
        return False

def config_file_check():
    if os.path.exists(get_config_file()):
        return True
    else:
        return False

def init_config_path():
    os.makedirs(get_config_path())

def init_config_file():
    fp = open(get_config_file(), "w")
    fp.write("[tray]\n")
    fp.write("PATH = /usr/share/deepin-system-settings,\n")
    fp.close()

def init_config():
    if not config_path_check():
        init_config_path()
    if not config_file_check():
        init_config_file()


def pixbuf_check(element):
    return isinstance(element, gtk.gdk.Pixbuf)

def text_check(element):
    return isinstance(element, str)

def cn_check():
    return os.environ["LANGUAGE"].startswith("zh_")


if __name__ == "__main__":
    print get_home_path()
    print get_config_path()
    if not config_path_check():
        init_config_path()
    if not config_file_check():
        init_config_file()
