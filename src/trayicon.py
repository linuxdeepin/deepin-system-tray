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
#from trayicon_plugin_manage import PluginManage
import gtk

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
        #self.plugin_manage = PluginManage()
        self.width, self.height = 100,-1
        self.tray_icon_to_screen_width = tray_icon_to_screen_width
        self.align_size = align_size
        self.menu_to_icon_y_padding = menu_to_icon_y_padding
        # Init trayicon position.
        self.metry = None
        # Init event.
        self.connect("configure-event", self.menu_configure_event)
        self.connect("button-press-event", self.menu_grab_window_button_press)
        # Init root scrren.
        root = self.get_root_window()
        self.screen = root.get_screen()
        # Init event window.
        #self.init_event_window()
        # create trayicon.
        '''
        for plug in self.plugin_manage.keywords:
            self.trayicon_list.append(self.create_tray_icon(plug))
        '''
        
    def menu_configure_event(self, widget, event):
        self.resize(1, 1)
        self.move_menu() 

    def menu_grab_window_button_press(self, widget, event):        
        if not ((widget.allocation.x <= event.x <= widget.allocation.width) 
           and (widget.allocation.y <= event.y <= widget.allocation.height)):
            self.hide_menu()
     
    def show_menu(self):
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
                   
    def set_max_show_menu(self, x):        
        screen_w = self.screen.get_width()        
        screen_rect_width = x + self.get_size_request()[0]
        if (screen_rect_width) > screen_w:
            return screen_rect_width - screen_w + self.tray_icon_to_screen_width
        else:
            return 0

    def create_tray_icon(self, plug=None):
        tray_icon = gtk.StatusIcon()
        tray_icon.set_visible(True)
        tray_icon.set_from_file(plug.icon_path)
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
        # save plug.
        #self.save_trayicon = plug
        # remove child widget.
        width = 30
        # add child widgets plugs.
        
        # get tray icon metry.
        self.metry = statusicon.get_geometry()
        self.resize(1, 1)
        self.set_size_request(width, -1)
        self.show_menu()

    def plugs_add_event(self, socket):
        print "add .. add ..."
        
    def plugs_remove_event(self, socket):
        print "remove...remove..."

if __name__ == "__main__":
    '''
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.show_all()
    '''
    TrayIcon()
    gtk.main()

