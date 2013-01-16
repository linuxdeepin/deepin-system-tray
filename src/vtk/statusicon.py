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
from draw import draw_pixbuf, draw_text
import gtk
import cairo



class StatusIcon(TrayIcon):
    def __init__(self):
        TrayIcon.__init__(self)
        self.init_statusiocn_values()
        self.init_statusicon()
    
    def init_statusiocn_values(self):
        self.id = -1
        self.status_icon_list = []
        self.test_time = ""
        self.draw_function_id = self.draw_function

    def init_statusicon(self):
        self.connect("expose-event", self.statusicon_draw_expose_event)
        self.connect("button-release-event", self.statusicon_button_release_event)
        self.connect("motion-notify-event", self.statusicon_motion_notify_event)

    def draw_function(self, cr, x, y, w, h):
        for element_struct in self.status_icon_list:
            # left line.
            left_line_pixbuf = gtk.gdk.pixbuf_new_from_file("image/Lline.png")
            draw_pixbuf(cr, 
                        left_line_pixbuf, 
                        element_struct.x, 
                        y + h/2 - left_line_pixbuf.get_height()/2)
            w_padding = 5
            end_padding = element_struct.w - 5 
            for element in element_struct.element:
                if self.pixbuf_check(element):
                    draw_pixbuf(cr, 
                                element, 
                                element_struct.x + w_padding, 
                                y + h/2 - element.get_height()/2)
                    w_padding = element.get_width() + 5
                elif self.str_check(element):
                    draw_text(cr, 
                              element, 
                              element_struct.x + w_padding, 
                              y + h/2 - get_text_size(element)[1]/2)
                    w_padding = get_text_size(element)[0] + 5
            # right line.
            right_line_pixbuf = gtk.gdk.pixbuf_new_from_file("image/Rline.png")
            draw_pixbuf(cr, 
                        left_line_pixbuf, 
                        end_padding, 
                        y + h/2 - left_line_pixbuf.get_height()/2)

    def statusicon_button_release_event(self, widget, event):
        rect = widget.allocation
        print "position:", widget.window.get_root_origin()
        print "position:", widget.window.get_position()
        print "statusicon_button_release_event....", event.x_root, event.y_root, rect.width, rect.height

    def statusicon_motion_notify_event(self, widget, event):
        print "statusicon_motion_notify_event...."
        for element_struct in self.status_icon_list:
            print element_struct

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

    def get_start_pointer(self):
        w = 0
        for status in self.status_icon_list:
            w += status.w 
            self.set_size_request(w, 24)
        return w

    def status_icon_new(self, element_list):
        try:
            self.status_element = StatusElement()
            save_w, save_h = 0, 0
            for element in element_list:
                if self.pixbuf_check(element): # pixbuf type.
                    w = element.get_width()
                    h = element.get_height()
                elif self.str_check(element): # text type. 
                    w,h = get_text_size(element)

                save_w += w + 5 
                save_h += h
            
            self.status_element.element = element_list
            self.status_element.x = self.get_start_pointer()
            self.status_element.w = save_w + 5
            self.status_element.h = save_h 
            self.id += 1
            self.status_element.id = self.id
            self.status_icon_list.append(self.status_element) 
            self.resize_status_icon(self.status_element.x + self.status_element.w)
            return self.status_element
        except Exception, e:
            print "add_status_icon[error]:", e
            return None

    def pixbuf_check(self, element):
        return isinstance(element, gtk.gdk.Pixbuf)

    def str_check(self, element):
        return isinstance(element, str)

    def resize_status_icon(self, w):
        self.set_size_request(w, 24)
        

class StatusElement(object):
    def __init__(self):
        self.id = 0
        self.x = 0 
        self.w = 0
        self.h = 0
        self.element = None



if __name__ == "__main__":
    from tray_time import TrayTime, TRAY_TIME_12_HOUR, TRAY_TIME_24_HOUR
    def tray_time_send(traytime, text, type):
        time_p = None
        if type == TRAY_TIME_12_HOUR:
            time_p = text[0]
        hour = text[0 + type]
        min = text[1 + type]
        show_str = "%s %s:%s" % (time_p, hour, min)
        
        time_element.element[1] = show_str
        new_trayicon.queue_draw()

    new_trayicon = StatusIcon()
    tray_time = TrayTime()
    new_trayicon.show_all()
    tray_time.connect("send-time", tray_time_send)
    pixbuf = gtk.gdk.pixbuf_new_from_file("image/time_white.png")
    time_element = new_trayicon.status_icon_new([pixbuf,
                                                 "上午 12:12"])
   # pixbuf = gtk.gdk.pixbuf_new_from_file("image/sound_white.png")
   # pixbuf_element = new_trayicon.status_icon_new([pixbuf])
   # name_element = new_trayicon.status_icon_new(["我是邱海龙..."])
    

    gtk.main()


