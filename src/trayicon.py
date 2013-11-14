#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Deepin, Inc.
#               2013 Hailong Qiu
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


import os
import sys
import gtk
import dbus
import cairo
import subprocess

from Xlib import display, Xatom, X
import Xlib.protocol.event
from trayicon_plugin_manage import PluginManage
from vtk.statusicon import Element
from vtk.utils import propagate_expose
from vtk.window import TrayIconWin
from vtk.unique_service import UniqueService, is_exists
from deepin_utils.file import get_parent_dir

APP_DBUS_NAME = "com.deepin.trayicon"
APP_OBJECT_NAME = "/com/deepin/trayicon"

TRAY_HEIGHT = 16
plugin_ids = ["date_time",
              "shutdown",
              "sound",
              "network",
              "mount_media",
              "power",
              "bluetooth"
              ]

class TrayIcon(TrayIconWin):
    def __init__(self):
        TrayIconWin.__init__(self)
        if is_exists(APP_DBUS_NAME, APP_OBJECT_NAME): 
            sys.exit()
        app_bus_name = dbus.service.BusName(APP_DBUS_NAME, bus=dbus.SessionBus())
        UniqueService(app_bus_name, APP_DBUS_NAME, APP_OBJECT_NAME)
        self.__save_trayicon = None
        self.__found_dock = False
        self.metry = None
        self.__save_width = 0
        self.tray_icon_to_screen_width=10
        root = self.get_root_window()
        self.menu_screen = root.get_screen()

        self.plugin_manage = PluginManage()

        self.display = display.Display()
        self.screen   = self.display.screen()

        self.opcode_atom = self.display.intern_atom("_NET_SYSTEM_TRAY_OPCODE")
        self.visual_atom = self.display.intern_atom("_NET_SYSTEM_TRAY_VISUAL")
        self.dock_atom = self.display.intern_atom("_NET_SYSTEM_TRAY_S%d" % (self.display.get_default_screen()))
        self.tray_window = None

        self.__tray_find_dock()
        gtk.timeout_add(2000, self.__tray_find_dock)

    def __build_tray_window(self):
        self.__main_hbox = gtk.HBox()

        for i in xrange(len(plugin_ids)):
            p = plugin_ids[i]
            if  self.plugin_manage.key_dict.has_key(p):
                p_class = self.plugin_manage.key_dict[p]
                print p_class
                gtk.timeout_add(100 * i, self.__load_plugin_timeout, p_class)

        tray_window   = gtk.Window(gtk.WINDOW_TOPLEVEL)
        tray_window.add(self.__main_hbox)
        tray_window.connect("expose-event", self.__window_expose_event)
        tray_window.set_decorated(False)
        tray_window.set_wmclass("deepintrayicon", "DeepinTrayIcon")
        tray_window.connect("destroy", self.lost_dock)
        tray_window.set_colormap(gtk.gdk.Screen().get_rgba_colormap())
        tray_window.set_skip_pager_hint(True)
        tray_window.set_skip_taskbar_hint(True)
        tray_window.show_all()
        return tray_window

    def lost_dock(self, w):
        w.destroy()
        self.__found_dock = False
        self.__tray_find_dock()

    def __load_plugin_timeout(self, p_class):
        _class = p_class()
        widget = Element()
        widget.set_size_request(-1, TRAY_HEIGHT)
        _class.init_values([self, widget])
        widget.set_text("")
        widget.connect('popup-menu-event', self.__tray_icon_popup_menu, _class)
        widget.connect("hide",             self.widget_hide_modify_statusicon_size)
        widget.connect("size-allocate",    self.widget_realize_event)

        self.__main_hbox.pack_end(widget)
        self.__main_hbox.show_all()
        return False

    def __tray_icon_popup_menu(self, 
                             statusicon, 
                             geometry,
                             plug
                             ):
        self.init_popup_menu(statusicon, plug)

    def container_remove_all(self, container):
        container.foreach(lambda widget: container.remove(widget))

    def init_popup_menu(self, statusicon, plug):
        self.container_remove_all(self.main_ali)
        widget = plug.plugin_widget()
        self.__save_trayicon = plug
        plug.show_menu()
        self.add_plugin(widget)
        self.metry = statusicon.get_geometry()
        self.show_menu()

    def menu_configure_event(self, widget, event):
        self.resize(1, 1)
        self.move_menu() 

    def show_menu(self):
        '''
        # run plug show menu function.
        if self.save_trayicon:
            self.save_trayicon.show_menu()
        '''
        self.move_menu()
        self.show_all()

    def tray_icon_button_press(self, widget, event):        
        if self.in_window_check(widget, event):
            self.hide_menu()

    def hide_menu(self):
        if self.__save_trayicon:
            self.__save_trayicon.hide_menu()
        self.hide_all()        
        self.grab_remove()

    def move_menu(self):        
        if self.metry:
            metry = self.metry  
            # tray_icon_rect[0]: x tray_icon_rect[1]: y t...t[2]: width t...t[3]: height
            tray_icon_rect = metry[1]        
            # get screen height and width. 
            screen_h = self.menu_screen.get_height()
            #screen_w = self.menu_screen.get_width()       
            # get x.
            x = tray_icon_rect[0] + tray_icon_rect[2]/2 - self.get_size_request()[0]/2
            x -= self.set_max_show_menu(x)
            # get y.
            y_padding_to_creen = self.get_size_request()[1]#self.allocation.height
            if self.allocation.height <= 1:
                y_padding_to_creen = self.get_size_request()[1]
            # 
            if (screen_h / 2) <= tray_icon_rect[1] <= screen_h: # bottom trayicon show.
                y = tray_icon_rect[1]
                self.move(x, y - y_padding_to_creen)
            else: # top trayicon show.
                y = tray_icon_rect[1]
                self.move(x, y + tray_icon_rect[3])
            #
            self.offset = (tray_icon_rect[0] - self.get_position()[0] 
                        - (self.arrow_width / 2) + (tray_icon_rect[2]/2))

    def set_max_show_menu(self, x):        
        screen_w = self.menu_screen.get_width()        
        screen_rect_width = x + self.get_size_request()[0]
        if (screen_rect_width) > screen_w:
            return screen_rect_width - screen_w + self.tray_icon_to_screen_width
        else:
            return 0

    def __window_expose_event(self, widget, event):
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
        propagate_expose(widget, event) 
        return True

    def __tray_find_dock(self, w=None):
        if not self.__found_dock:
            print "tray_find_dock..."

            dock_selection  = self.display.get_selection_owner(self.dock_atom)
            if dock_selection:
                self.tray_win = self.display.create_resource_object("window", dock_selection.id)
                self.tray_win.get_full_property(self.visual_atom, Xatom.VISUALID)

                if not self.tray_window or not self.tray_window.get_realized():
                    self.tray_window = self.__build_tray_window()
                self.__tray_send_opcode(
                        self.tray_win,
                        self.opcode_atom,
                        [X.CurrentTime, 0L, self.tray_window.window.xid, 0L, 0L],
                        X.NoEventMask
                        )
                self.display.flush()
                self.__found_dock = True
            else:
                self.__found_dock = False
        return True

    def __tray_send_opcode(self,
                         dock_win,
                         type,
                         data,
                         mask
                         ):
        data = (data + [0] * (5 - len(data)))[:5]
        new_event = Xlib.protocol.event.ClientMessage(
                    window      = dock_win.id,
                    client_type = type,
                    data        = (32, (data)),
                    type        = X.ClientMessage
                    )
        dock_win.send_event(new_event, event_mask=mask)


    def widget_realize_event(self, widget, allocation):
        self.statusicon_modify_size()

    def widget_hide_modify_statusicon_size(self, widget):
        self.statusicon_modify_size()

    def statusicon_modify_size(self):
        width = 0
        for child in self.__main_hbox.get_children():
            if child.get_visible():
                width += child.get_size_request()[0]

        if self.__save_width != width:
            self.__save_width = width 
            self.tray_window.set_geometry_hints(None, 
                                           width, 
                                           TRAY_HEIGHT, 
                                           width, 
                                           TRAY_HEIGHT, 
                                           -1, -1, -1, -1, -1, -1)


    #############################################
    def get_tray_position(self):
        return self.tray_window.get_position()

    def get_tray_pointer(self):
        return self.tray_window.get_pointer()

def check_is_in_virtual_pc():
    '''just check vmware and virtualbox'''
    cmd = ['lspci', '-b']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    s = p.communicate()[0]
    s = s.lower()
    path = os.path.join(get_parent_dir(__file__, 3), 'deepin-system-settings/modules/power/src/tray_shutdown_plugin.py')
    if len(s.split("vmware")) > 1 or len(s.split("virtualbox")) > 1:
        subprocess.Popen(['python', path, 'vpc'])

if __name__ == "__main__":
    tray_icon = TrayIcon()
    check_is_in_virtual_pc()
    gtk.main()
