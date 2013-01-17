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
from color import alpha_color_hex_to_cairo, color_hex_to_cairo
from utils import new_surface
from utils import cairo_popover 
from blur.vtk_cairo_blur import gaussian_blur

SAHOW_VALUE = 2 
ARROW_WIDTH = 10

class TrayIconWin(gtk.Window):
    def __init__(self):
        #gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        # init values.
        self.init_values()
        self.init_trayicon_settings()
        self.init_trayicon_events()
        self.hide_all() 

    def init_values(self):
        self.surface = None
        self.old_w = 0
        self.old_h = 0
        self.old_offset = 0
        self.trayicon_x = SAHOW_VALUE * 2  
        self.trayicon_y = SAHOW_VALUE * 2
        self.trayicon_border = 2.5
        self.radius = 5
        self.arrow_width = ARROW_WIDTH
        self.arrow_height = ARROW_WIDTH/2 
        self.tray_pos_type = gtk.POS_BOTTOM
        self.offset = 30 
        self.ali_size = 10
        self.alpha = 0.95
        # colors.
        self.sahow_color = ("#000000", 0.15)
        self.border_out_color = ("#000000", 1.0)

    def init_trayicon_settings(self):
        self.set_colormap(gtk.gdk.Screen().get_rgba_colormap())
        #self.set_modal(True)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_position(gtk.WIN_POS_NONE)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_MENU)
        self.set_opacity(self.alpha)
        #
        self.draw = gtk.EventBox()
        self.main_ali  = gtk.Alignment(0, 0, 1, 1)
        # set main_ali padding size.
        self.set_pos_type(self.tray_pos_type)
        self.add(self.draw)
        self.draw.add(self.main_ali)
        self.hide_all()

    def add_plugin(self, widget):
        self.main_ali.add(widget)

    def remove_plugin(self, widget):
        if self.main_ali.get_children() != []:
            self.main_ali.remove(widget)
        else:
            print "main_ali no widgets"

    def plugs_add_event(self, socket):
        pass 

    def plugs_remove_event(self, socket):
        pass

    def get_id(self):
        return self.socket.get_id()

    def init_trayicon_events(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("configure-event", self.menu_configure_event)
        self.connect("button-press-event", self.tray_icon_button_press) 
        self.connect("size-allocate", self.on_size_allocate)
        self.draw.connect("expose-event", self.draw_expose_event)
        self.connect("show", self.trayicon_show_event)
        self.connect("destroy", lambda w : gtk.main_quit())
        
    def menu_configure_event(self, widget, event):
        pass

    def tray_icon_button_press(self, widget, event):        
        if self.in_window_check(widget, event):
            self.hide_all()
            self.grab_remove()

    def in_window_check(self, widget, event):
        toplevel = widget.get_toplevel()
        window_x, window_y = toplevel.get_position()
        x_root = event.x_root
        y_root = event.y_root
        if not ((x_root >= window_x and x_root < window_x + widget.allocation.width) 
            and (y_root >= window_y and y_root < window_y + widget.allocation.height)):
            return True
        '''
        return (not ((widget.allocation.x <= event.x <= widget.allocation.width) 
               and (widget.allocation.y <= event.y <= widget.allocation.height)))
        '''
        
    def trayicon_show_event(self, widget):
        gtk.gdk.pointer_grab(
            self.window,
            True,
            gtk.gdk.POINTER_MOTION_MASK
            | gtk.gdk.BUTTON_PRESS_MASK
            | gtk.gdk.BUTTON_RELEASE_MASK
            | gtk.gdk.ENTER_NOTIFY_MASK
            | gtk.gdk.LEAVE_NOTIFY_MASK,
            None,
            None,
            gtk.gdk.CURRENT_TIME)
        gtk.gdk.keyboard_grab(
                self.window, 
                owner_events=False, 
                time=gtk.gdk.CURRENT_TIME)
        self.grab_add()        

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
        try:
            widget.propagate_expose(widget.get_child(), event)
        except:
            pass
        return True

    def on_size_allocate(self, widget, alloc):
        x, y, w, h = self.allocation
        # !! no expose and blur.
        if ((self.old_w == w and self.old_h == h) 
            and self.offset == self.old_offset):
            return False
        # 
        self.surface, self.surface_cr = new_surface(w, h)
        self.compute_shadow(w, h)
        self.old_w = w
        self.old_h = h
        self.old_offset = self.offset

    def compute_shadow(self, w, h):
        # sahow.
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x, self.trayicon_y, 
                      w, h,
                      self.radius, 
                      self.arrow_width, self.arrow_height, self.offset,
                      pos_type=self.tray_pos_type)
        gaussian_blur(self.surface, SAHOW_VALUE)
        self.surface_cr.set_source_rgba( # set sahow color.
                *alpha_color_hex_to_cairo((self.sahow_color)))
        self.surface_cr.fill_preserve()
        gaussian_blur(self.surface, SAHOW_VALUE)
        # border.
        # out border.
        self.surface_cr.clip()
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x + 3, 
                      self.trayicon_y + 3, 
                      w, h + 1.5, 
                      self.radius, 
                      self.arrow_width, self.arrow_height, self.offset,
                      pos_type=self.tray_pos_type)
        self.surface_cr.set_source_rgba( # set out border color.
                *alpha_color_hex_to_cairo(self.border_out_color))
        self.surface_cr.set_line_width(self.border_width)
        self.surface_cr.fill()
        # in border.
        self.surface_cr.reset_clip()
        padding_h = 2
        cairo_popover(self, self.surface_cr, 
                      self.trayicon_x + self.trayicon_border + 1, 
                      self.trayicon_y + self.trayicon_border + 1, 
                      w, h + padding_h, 
                      self.radius, 
                      self.arrow_width, self.arrow_height, self.offset,
                      self.tray_pos_type) 
        self.surface_cr.set_source_rgba(1, 1, 1, 1.0) # set in border color.
        self.surface_cr.set_line_width(self.border_width)
        self.surface_cr.fill()

    def expose_event_draw(self, cr):
        if self.surface:
            cr.set_source_surface(self.surface, 0, 0)
            cr.paint()
        
    def set_pos_type(self, pos_type):
        self.tray_pos_type = pos_type
        padding_top, padding_bottom = 0, 0
        #
        if pos_type == gtk.POS_TOP:
            padding_top = self.arrow_height
        else:
            padding_bottom = self.arrow_height 
        #
        self.main_ali.set_padding(
                self.ali_size + int(self.trayicon_x + padding_top),
                int(self.ali_size + self.trayicon_x + padding_bottom),
                int(self.ali_size + self.trayicon_x),
                int(self.ali_size + self.trayicon_x))

if __name__ == "__main__":
    test = TrayIconWin()
    #test.set_pos_type(gtk.POS_TOP)
    #test.set_pos_type(gtk.POS_BOTTOM)
    test.resize(300, 300)
    test.move(300, 300)
    test.show_all()
    gtk.main()
