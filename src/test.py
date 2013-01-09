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
import math
from vtk.utils import new_surface
from vtk.utils import cairo_popover 
from dtk_cairo_blur import gaussian_blur

class TrayIcon(gtk.Window):
    def __init__(self):
        #gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        # init values.
        self.surface = None
        self.old_w = 0
        self.old_h = 0
        self.trayicon_x = 10.5
        self.trayicon_y = 10.5
        self.radius = 5
        self.arrow_width = 20
        self.arrow_height = 10
        self.offs = 40 #(350/2)
        self.ali_size = 10
        #    
        self.set_colormap(gtk.gdk.Screen().get_rgba_colormap())
        self.set_modal(True)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_app_paintable(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        #self.set_position(gtk.WINDOW_POSITION_NONE)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        self.set_opacity(0.9)
        self.set_size_request(350, 290)
        self.main_vbox = gtk.VBox()
        self.draw = gtk.EventBox()
        self.ali  = gtk.Alignment(0, 0, 1, 1)
        self.ali.set_padding(self.ali_size + int(self.trayicon_x + self.arrow_height),
                           int(self.ali_size + self.trayicon_x),
                           int(self.ali_size + self.trayicon_x),
                           int(self.ali_size + self.trayicon_x))
        self.add(self.draw)
        self.draw.add(self.ali)
        self.ali.add(self.main_vbox)
        # test.
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        self.main_vbox.pack_start(gtk.Button("test"), True, True)
        #
        self.draw.connect("expose-event", self.draw_expose_event)
        self.connect("size-allocate", self.on_size_allocate)
        self.show_all()
        self.move(300, 300)

    
    def draw_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        cr.rectangle(*rect)
        cr.set_source_rgba(1, 1, 1, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        cr = widget.window.cairo_create()
        x, y, w, h = rect
        self.expose_event_draw(cr)
        #
        widget.propagate_expose(widget.get_child(), event)
        return True

    def on_size_allocate(self, widget, alloc):
        print "on_size_allocate"
        x, y, w, h = self.allocation
        if (self.old_w == w and self.old_h == h):
            return False
        # 
        self.surface, self.surface_cr = new_surface(w, h)
        self.compute_shadow(w, h)
        self.old_w = w
        self.old_h = h

    def compute_shadow(self, w, h):
        print "compute_shadow..."
        #
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x, self.trayicon_y, 
                      w, h,
                      self.radius, self.arrow_width, self.arrow_height, self.offs)
                    
        self.surface_cr.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        self.surface_cr.fill_preserve()
        gaussian_blur(self.surface, 4)
        # outer border.
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x + 2.5, self.trayicon_y + 2.5, 
                      w-5, h-5, self.radius, self.arrow_width, self.arrow_height, self.offs) 
        self.surface_cr.set_source_rgba(1, 1, 1, 1.0)
        self.surface_cr.set_line_width(self.border_width)
        self.surface_cr.fill_preserve()


    def expose_event_draw(self, cr):
        if self.surface:
            cr.set_source_surface(self.surface, 0, 0)
            cr.paint_with_alpha(1.0)
            #cr.paint()
        
if __name__ == "__main__":
    TrayIcon()
    gtk.main()
