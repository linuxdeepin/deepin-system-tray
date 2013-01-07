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
import gtk
from vtk.utils import new_surface
from vtk.utils import cairo_popover 
from vtk.color import exponential_blue


class TrayIcon(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        # init values.
        self.trayicon_x = 10.5
        self.trayicon_y = 10.5
        self.radius = 5
        self.arrow_width = 20
        self.arrow_height = 10
        #
        self.set_size_request(150, 250)
        self.connect("expose-event", self.tray_icon_expose_event)
        self.show_all()
        
    def tray_icon_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        # create surface.
        surface, surface_context = new_surface(w, h)
        #
        cairo_popover(widget, 
                      surface_context, 
                      self.trayicon_x, self.trayicon_y, 
                      w, h,
                      self.radius, 
                      self.arrow_width, self.arrow_height)
        # shadow.
        surface_context.set_source_rgba(0, 0, 0, 0.9)
        surface_context.fill_preserve()
        exponential_blue(surface, 
                         6, 
                         w, h)
        surface_context.clip()
        # background.
        # border.
        cairo_popover(widget,
                      surface_context,
                      self.trayicon_x, self.trayicon_y,
                      w, h,
                      self.radius,
                      self.arrow_width, self.arrow_height)
        surface_context.set_operator(cairo.OPERATOR_SOURCE)
        surface_context.set_line_width(1)
        surface_context.set_source_rgb(0, 0, 1)
        surface_context.rectangle(x, y, w, h)
        surface_context.stroke()
        #
        cr.set_source_surface(surface, 0, 0)
        cr.paint()
        return False

    #def cairo_

if __name__ == "__main__":
    TrayIcon()
    gtk.main()
