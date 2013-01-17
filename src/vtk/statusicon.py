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

from trayicon import TrayIcon
from utils import propagate_expose, new_surface, get_text_size
from utils import pixbuf_check, text_check
from draw import draw_pixbuf, draw_text
import gtk
import cairo
import gobject


class StatusIcon(TrayIcon):
    def __init__(self):
        TrayIcon.__init__(self)
        self.set_size_request(-1, 16)
        self.init_statusiocn_widgets()
        self.init_statusiocn_values()
        self.init_statusicon_events()

    def init_statusiocn_widgets(self):
        self.__main_hbox = gtk.HBox()
        self.add(self.__main_hbox)
    
    def init_statusiocn_values(self):
        self.draw_function_id = self.draw_function
        # init left line pixbuf.
        self.left_line_pixbuf = gtk.gdk.pixbuf_new_from_file("image/Lline.png") 
        self.left_line_w = self.left_line_pixbuf.get_width()
        self.left_line_h = self.left_line_pixbuf.get_height()
        # init right line pixbuf.
        self.right_lien_pixbuf = gtk.gdk.pixbuf_new_from_file("image/Rline.png")
        self.right_line_w = self.left_line_pixbuf.get_width()
        self.right_lien_h = self.right_lien_pixbuf.get_height()

    def init_statusicon_events(self):
        self.connect("expose-event", self.statusicon_draw_expose_event)

    def draw_function(self, cr, x, y, w, h):
        pass
         
    def statusicon_draw_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        #
        cr.rectangle(*rect)
        cr.set_source_rgba(1, 1, 1, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        #
        cr = widget.window.cairo_create()
        #
        self.draw_function_id(cr, x, y, w, h)
        #
        propagate_expose(widget, event) 
        return True

    ###########################################################
    def get_tray_position(self):
        return self.window.get_position()

    def get_tray_pointer(self):
        return self.window.get_pointer()

    def status_icon_new(self, text="", pixbuf=None):
        widget = Element() 
        self.widget_init(widget, text, pixbuf)
        self.__main_hbox.pack_start(widget)
        self.__main_hbox.show_all()
        #
        print "button pixbuf:", self.get_pixbuf(widget) 
        print "button text:", self.get_text(widget)
        return widget

    def widget_init(self, widget, text, pixbuf):
        widget.set_size_request(-1, 16)
        if text_check(text):
            self.set_text(widget, text)
        if pixbuf_check(pixbuf):
            self.set_pixbuf(widget, pixbuf)
        # connect event.
        widget.connect("expose-event", self.widget_expose_event)

    def widget_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        # draw left line.
        if widget.get_state() == gtk.STATE_PRELIGHT:
            draw_pixbuf(cr, 
                        self.left_line_pixbuf, 
                        x, 
                        y + h/2 - self.left_line_h/2)
        # draw text and pixbuf.
        text = self.get_text(widget) 
        text_w = 0
        pixbuf = self.get_pixbuf(widget)
        pixbuf_w = 0
        if pixbuf != None:
            pixbuf_w = pixbuf.get_width() 
            pixbuf_h = pixbuf.get_height()
            draw_pixbuf(cr, pixbuf, x + 5, y + h/2 - pixbuf.get_height()/2)
        if text != "":
            text_w, text_h = get_text_size(text)
            draw_text(cr, text, x + pixbuf_w + 5, y + h/2 - text_h/2)
        # draw right line.
        if widget.get_state() == gtk.STATE_PRELIGHT:
            draw_pixbuf(cr, 
                        self.right_lien_pixbuf, 
                        x + w - self.right_line_w, 
                        y + h/2 - self.right_lien_h/2)
        #
        w_padding = pixbuf_w + text_w + 5 + self.left_line_w + self.right_line_w
        widget.set_size_request(w_padding, h)
        print widget.get_state()
        #
        return True

    def get_pixbuf(self, widget):
        image = widget.get_image()
        if image:
            return image.get_pixbuf()
        else:
            return image

    def set_pixbuf(self, widget, pixbuf):
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        widget.set_image(image) 

    def get_text(self, widget):
        return widget.get_label()

    def set_text(self, widget, text):
        widget.set_label(text)


class Element(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)

    def set_type(self, type):
        print "image text..."


gobject.type_register(StatusIcon)

if __name__ == "__main__":
    from tray_time import TrayTime, TRAY_TIME_12_HOUR, TRAY_TIME_24_HOUR
    
    def test_button_press_event(widget, event):
        print "fjdsklfjdsklfj"

    def tray_time_send(traytime, text, type):
        time_p = None
        if type == TRAY_TIME_12_HOUR:
            time_p = text[0]
        hour = text[0 + type]
        min = text[1 + type]
        show_str = "%s %s:%s" % (time_p, hour, min)
        time_tray.set_label(show_str)

    new_trayicon = StatusIcon()
    pixbuf = gtk.gdk.pixbuf_new_from_file("image/time_white.png")
    time_tray = new_trayicon.status_icon_new(text="fdsf", pixbuf=pixbuf)
    time_tray.connect("button-press-event", test_button_press_event)
    new_trayicon.show_all()
    tray_time = TrayTime()
    tray_time.connect("send-time", tray_time_send)
    gtk.main()


