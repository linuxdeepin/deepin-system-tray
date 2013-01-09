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
        self.old_w = 0
        self.old_h = 0
        self.trayicon_x = 10.5
        self.trayicon_y = 10.5
        self.radius = 5
        self.arrow_width = 20
        self.arrow_height = 10
        self.offs = 40 #(350/2)
        #
        self.set_modal(True)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_app_paintable(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        #self.set_position(gtk.WINDOW_POSITION_NONE)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        self.set_opacity(0.9)
        self.set_size_request(350, 90)
        self.draw = gtk.EventBox()
        self.add(self.draw)
        self.draw.connect("expose-event", self.draw_expose_event)
        self.connect("size-allocate", self.on_size_allocate)
        self.show_all()
        self.move(500, 500)
        self.draw.add(gtk.Button("测试"))
    
    def draw_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        self.expose_event_draw(cr)
        #
        cairo_popover(self, cr, 
                      self.trayicon_x + 2.5, self.trayicon_y + 2.5, 
                      w-5, h-5, self.radius, self.arrow_width, self.arrow_height, self.offs) 
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_line_width(self.border_width)
        cr.fill_preserve()
        return True

    def on_size_allocate(self, widget, alloc):
        print "on_size_allocate"
        x, y, w, h = self.allocation
        bitmap = gtk.gdk.Pixmap(None, w, h, 1) 
        cr = bitmap.cairo_create()
        if (self.old_w == w and self.old_h == h):
            return False
        # 
        cr.set_source_rgb(0, 0, 0)
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_source_rgb(0, 0, 0)
        cr.set_operator(cairo.OPERATOR_OVER)
        #
        self.surface, self.surface_cr = new_surface(350, 90)
        self.compute_shadow(w, h)
        self.old_w = w
        self.old_h = h
        #
        self.on_size_draw(cr, x, y, w, h)
        #widget.shape_combine_mask(bitmap, 0, 0)

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
        print "oter border..."
        self.surface_cr.reset_clip()
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x, self.trayicon_y, 
                      w, h, self.radius, self.arrow_width, self.arrow_height, self.offs) 
        self.surface_cr.set_operator(cairo.OPERATOR_SOURCE)
        self.surface_cr.set_source_rgba(0, 0, 1, 0.5)
        self.surface_cr.set_line_width(self.border_width)
        self.surface_cr.stroke()

    def expose_event_draw(self, cr):
        cr.set_source_surface(self.surface, 0, 0)
        cr.paint()
        
    def on_size_draw(self, cr, x, y, w, h):
        pass
if __name__ == "__main__":
    TrayIcon()
    gtk.main()
