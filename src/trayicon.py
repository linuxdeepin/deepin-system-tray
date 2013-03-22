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

from vtk.window import TrayIconWin
from trayicon_plugin_manage import PluginManage
from vtk.statusicon import StatusIcon
from vtk.utils import app_check, clear_app_bind
from vtk.unique_service import UniqueService, is_exists
from vtk.constant import print_msg
#from dms import Dms
import gtk
import sys
import dbus

FILE_TMP = "/tmp/msg.tmp"
APP_DBUS_NAME = "com.deepin.trayicon"
APP_OBJECT_NAME = "/com/deepin/trayicon"

class TrayIcon(TrayIconWin):
    def __init__(self,
                 menu_to_icon_y_padding=0,
                 tray_icon_to_screen_width=10,
                 align_size=10
                ):
        TrayIconWin.__init__(self)
        print_msg("trayicon start run....")
        #
        if len(sys.argv) >= 2:
            if sys.argv[1] == "debug":
                self.debug = True
        if is_exists(APP_DBUS_NAME, APP_OBJECT_NAME): 
            sys.exit()
        app_bus_name = dbus.service.BusName(APP_DBUS_NAME, bus=dbus.SessionBus())
        UniqueService(app_bus_name, APP_DBUS_NAME, APP_OBJECT_NAME)
        # Init values.
        self.save_trayicon = None
        self.trayicon_list = []
        self.status_icon = StatusIcon()
        self.plugin_manage = PluginManage()
        #self.dms = Dms(FILE_TMP)
        #self.dms.connect("changed", self.dms_changed)
        self.tray_icon_to_screen_width = tray_icon_to_screen_width
        self.menu_to_icon_y_padding = menu_to_icon_y_padding
        # Init trayicon position.
        self.metry = None
        # Init root scrren.
        root = self.get_root_window()
        self.screen = root.get_screen()
        # create trayicon.
        for plug in self.plugin_manage.keywords:
            if plug != None:
                self.trayicon_list.append(self.create_tray_icon(plug()))

    def quit_destroy(self, widget):
        gtk.main_quit()

    def menu_configure_event(self, widget, event):
        self.resize(1, 1)
        self.move_menu() 

    def tray_icon_button_press(self, widget, event):        
        if self.in_window_check(widget, event):
            self.hide_menu()
     
    def show_menu(self):
        # run plug show menu function.
        if self.save_trayicon:
            self.save_trayicon.show_menu()
        self.move_menu()
        self.show_all()
    
    def hide_menu(self):
        self.hide_all()        
        self.grab_remove()
        # run plug hide menu function.
        if self.save_trayicon:
            self.save_trayicon.hide_menu()

    def move_menu(self):        
        if self.metry:
            metry = self.metry  
            # tray_icon_rect[0]: x tray_icon_rect[1]: y t...t[2]: width t...t[3]: height
            tray_icon_rect = metry[1]        
            # get screen height and width. 
            screen_h = self.screen.get_height()
            screen_w = self.screen.get_width()       
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
        screen_w = self.screen.get_width()        
        screen_rect_width = x + self.get_size_request()[0]
        if (screen_rect_width) > screen_w:
            return screen_rect_width - screen_w + self.tray_icon_to_screen_width
        else:
            return 0

    def create_tray_icon(self, plug=None):
        tray_icon = self.status_icon.status_icon_new()
        try:
            tray_icon.set_visible(plug.run())
            plug.init_values([self, tray_icon])
            # init events.
            tray_icon.connect('popup-menu-event', self.tray_icon_popup_menu, plug)
        except Exception, e:
            print_msg("create_tray_icon[error]:%s"%(e))

        return tray_icon 

    def tray_icon_activate(self, statusicon, plug):
        self.init_popup_menu(statusicon, plug)

    def tray_icon_popup_menu(self, 
                             statusicon, 
                             geometry,
                             plug
                             ):
        self.init_popup_menu(statusicon, plug)

    def container_remove_all(self, container):
        container.foreach(lambda widget: container.remove(widget))

    def init_popup_menu(self, statusicon, plug):
        error_check = False
        # remove child widget.
        self.container_remove_all(self.main_ali)
        # save plug.
        self.save_trayicon = plug
        try:
        # add child widgets plugs.
            widget = self.save_trayicon.plugin_widget()
            self.add_plugin(widget)
        except Exception, e:
            print_msg("init_popup_menu[error]:%s"%(e))
            error_check = True
        # get tray icon metry.
        self.metry = statusicon.get_geometry()
        if not error_check:
            self.show_menu()
                 


if __name__ == "__main__":
    TrayIcon()
    gtk.main()
