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
from utils import propagate_expose, new_surface
from draw import draw_pixbuf, draw_text
import gtk
import cairo



class StatusIcon(TrayIcon):
    def __init__(self):
        TrayIcon.__init__(self)
        self.init_statusiocn_values()
        self.init_statusicon()
    
    def init_statusiocn_values(self):
        self.surface = None
        self.test_time = ""
        self.draw_function_id = self.draw_function

    def init_statusicon(self):
        self.connect("expose-event", self.statusicon_draw_expose_event)
        self.connect("button-release-event", self.statusicon_button_release_event)
        self.connect("motion-notify-event", self.statusicon_motion_notify_event)

    def draw_function(self, cr, x, y, w, h):
        lan_pixbuf = gtk.gdk.pixbuf_new_from_file("image/lan_white.png")
        draw_pixbuf(cr, lan_pixbuf, x, y + h/2 -  lan_pixbuf.get_height()/2) 

        draw_text(cr, self.test_time, x + 50, y + h/2 - lan_pixbuf.get_height()/2)

    def statusicon_button_release_event(self, widget, event):
        print "statusicon_button_release_event...."

    def statusicon_motion_notify_event(self, widget, event):
        print "statusicon_motion_notify_event...."

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

if __name__ == "__main__":
    from tray_time import TrayTime, TRAY_TIME_12_HOUR, TRAY_TIME_24_HOUR
    def tray_time_send(traytime, text, type):
        time_p = None
        if type == TRAY_TIME_12_HOUR:
            time_p = text[0]
        hour = text[0 + type]
        min = text[1 + type]
        show_str = "%s %s:%s" % (time_p, hour, min)
        new_trayicon.test_time = show_str
        new_trayicon.queue_draw()

    new_trayicon = StatusIcon()
    tray_time = TrayTime()
    new_trayicon.show_all()
    tray_time.connect("send-time", tray_time_send)
    gtk.main()


