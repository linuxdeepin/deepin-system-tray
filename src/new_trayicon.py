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

import sys
from Xlib import X, display, error, Xatom, Xutil
from Xlib.ext import shape
import Xlib.protocol.event
import gtk
from gtk import gdk
import gobject 
import select
import random
import cairo

(TRAY_ICON_TEXT, TRAY_ICON_IMAGE) = range(0, 2)

class NewTrayIcon(gtk.Plug):
    def __init__(self, type=TRAY_ICON_IMAGE):
        gtk.Plug.__init__(self, 0)
        self.init_values()
        self.init_widgets()
        self.start()

    def init_values(self):
        self.xdisplay = display.Display()
        self.screen = self.xdisplay.screen()
        self.root = self.screen.root
        # init atom.
        self.opcode_atom = self.xdisplay.intern_atom("_NET_SYSTEM_TRAY_OPCODE")
        self.visual_atom = self.xdisplay.intern_atom("_NET_SYSTEM_TRAY_VISUAL")
        atom = "_NET_SYSTEM_TRAY_S%d" % (self.xdisplay.get_default_screen())
        self.manager_atom = self.xdisplay.intern_atom(atom) 
        #self.desktop_atom = self.xdisplay.intern_atom("_NET_WM_DESKTOP")
        #self.xembed_info_atom = self.xdisplay.intern_atom("_XEMBED_INFO")
        # manager.
        self.manager_win = self.xdisplay.get_selection_owner(self.manager_atom)
        #
        self.tray_win = self.xdisplay.create_resource_object("window", self.manager_win.id)
        self.tray_win.get_full_property(self.visual_atom, Xatom.VISUALID)

    def init_widgets(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.set_size_request(120, 24)
        self.show()
        self.plug_xid = self.window.xid
        self.tray_widget_wind = self.xdisplay.create_resource_object("window", self.plug_xid)
        #self.icon_image = gtk.Image()
        #self.icon_image.set_from_file("icon.png")
        #self.icon_image = gtk.Label("猥琐斌:12:12:12,超级无敌..")
        self.icon_image = gtk.Button("fjdsklf")
        self.icon_image.show()
        self.add(self.icon_image)
        #
        self.connect("motion-notify-event", self.trayicon_motion_notify_evnet)
        self.connect("button-press-event", self.trayicon_button_press_event)

    def trayicon_motion_notify_evnet(self, widget, event):
        print "trayicon_motion_notify_evnet....."

    def trayicon_button_press_event(self, widget, event):
        print "trayicon_button_press_event......"

    def start(self):
        self.send_event_to_dock(
                        self.tray_win,
                        self.opcode_atom,
                        [X.CurrentTime, 0L, self.tray_widget_wind.id, 0L, 0L],
                        X.NoEventMask)
        self.xdisplay.flush()

    def send_event_to_dock(self,
                           manager_win, 
                           type, 
                           data, 
                           mask):
        data = (data + [0] * (5 - len(data)))[:5]
        # send client message.
        new_event = Xlib.protocol.event.ClientMessage(
                        window = manager_win.id,
                        client_type = type,
                        data = (32, (data)),
                        type = X.ClientMessage
                        )
        manager_win.send_event(new_event, event_mask = mask)

    ########################################################################
    # @ gtk API.
    def set_from_file(self, filename):
        pass

    def set_from_pixbuf(self, pixbuf):
        pass

    def set_has_tooltip(self, has_tooltip):
        pass

    def get_has_tooltip(self):
        pass

    def set_blinking(self, blinking):
        pass

    def get_size(self):
        pass 
        
            

if __name__ == "__main__":
    import time
    def time_show():
        time_str = time.localtime(time.time())
        new_trayicon.icon_image.set_label("%s-%s-%s" % (time_str.tm_hour, time_str.tm_min, time_str.tm_sec))
        return True

    new_trayicon = NewTrayIcon()
    gtk.timeout_add(500, time_show)
    gtk.main()




