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
from dms import Dms
import gtk
import gio

FILE_TMP = "/tmp/msg.tmp"

class TrayIcon(TrayIconWin):
    def __init__(self,
                 menu_to_icon_y_padding=0,
                 tray_icon_to_screen_width=10,
                 align_size=10
                ):
        TrayIconWin.__init__(self)
        # Init values.
        self.save_trayicon = None
        self.trayicon_list = []
        self.plugin_manage = PluginManage()
        self.dms = Dms(FILE_TMP)
        self.dms.connect("changed", self.dms_changed)
        self.tray_icon_to_screen_width = tray_icon_to_screen_width
        self.menu_to_icon_y_padding = menu_to_icon_y_padding
        # Init trayicon position.
        self.metry = None
        # Init root scrren.
        root = self.get_root_window()
        self.screen = root.get_screen()
        # create trayicon.
        for plug in self.plugin_manage.keywords:
            self.trayicon_list.append(self.create_tray_icon(plug))
        
    def menu_configure_event(self, widget, event):
        self.resize(1, 1)
        self.move_menu() 

    def tray_icon_button_press(self, widget, event):        
        if self.in_window_check(widget, event):
            self.hide_menu()
     
    def show_menu(self):
        self.move_menu()
        self.show_all()
        # run plug show menu function.
        if self.save_trayicon:
            self.save_trayicon.show_menu()
    
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
            y_padding_to_creen = self.allocation.height
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
        tray_icon = gtk.StatusIcon()
        tray_icon.set_visible(plug.run())
        tray_icon.set_from_file(plug.menu_icon)
        plug.init_values([self, tray_icon])
        # init events.
        tray_icon.connect("activate", self.tray_icon_activate, plug)
        tray_icon.connect('popup-menu', self.tray_icon_popup_menu, plug)
        return tray_icon 

    def tray_icon_activate(self, statusicon, plug):
        self.init_popup_menu(statusicon, plug)

    def tray_icon_popup_menu(self, 
                             statusicon, 
                             button, 
                             activate_time,
                             plug
                             ):
        self.init_popup_menu(statusicon, plug)

    def init_popup_menu(self, statusicon, plug):
        # remove child widget.
        if self.save_trayicon:
            self.remove_plugin(self.save_trayicon.plugin_widget())
        # save plug.
        self.save_trayicon = plug
        # add child widgets plugs.
        self.add_plugin(self.save_trayicon.plugin_widget())
        try:
            width = plug.width
        except:
            width = 150
        try:
            height = plug.height
        except:
            height = -1
        print "width:", width
        # get tray icon metry.
        self.metry = statusicon.get_geometry()
        self.resize(1, 1)
        self.set_size_request(width, height)
        self.show_menu()

    def dms_changed(self, dms, argv):        
        if self.plugin_manage.key_dict.has_key(argv[0]):
            try:
                plug = self.plugin_manage.key_dict[argv[0]]
                if argv[1] == "Quit":
                    plug.this_list[1].set_visible(False)
                elif argv[1] == "Start":
                    plug.this_list[1].set_visible(True)
                
                eval(argv[2])(eval(argv[3]))            
            except Exception, e:
                print "dms_changed[error]:", e
                 


if __name__ == "__main__":
    test = TrayIcon()
    test.set_size_request(50, -1)
    gtk.main()

