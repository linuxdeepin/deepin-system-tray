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



from draw import draw_text, draw_pixbuf
from utils import get_text_size
from listview_base import type_check
from listview_base import ListViewBase
import gtk



class ListView(ListViewBase):
    def __init__(self):
        ListViewBase.__init__(self)
        self.__init_settings()
        self.__init_values()
        self.__init_events()

    def __init_settings(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)

    def __init_values(self):
        self.__on_draw_column_heade = self.__on_draw_column_heade_hd
        self.__on_draw_sub_item     = self.__on_draw_sub_item_hd

    def __init_events(self):
        self.connect("motion-notify-event", self.__listview_motion_notify_event)
        self.connect("button-press-event",  self.__listview_button_press_event)
        self.connect("button-release-event", self.__listview_button_release_event)
        self.connect("enter-notify-event",   self.__listview_enter_notify_event)
        self.connect("leave-notify-event",   self.__listview_leave_notify_event)
        self.connect("expose-event",        self.__listview_expose_event)
    
    def __listview_motion_notify_event(self, widget, event):
        print "__listview_motion_notify_event..."

    def __listview_button_press_event(self, widget, event):
        print "__listview_button_press_event...."

    def __listview_button_release_event(self, widget, event):
        print "__listview_button_release_event..."

    def __listview_enter_notify_event(self, widget, event):
        print "__listview_enter_enter...notify_event..."

    def __listview_leave_notify_event(self, widget, event):
        print "__listview_leave_notify_event...."

    def __listview_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        self.on_draw_column_heade(self)
        self.on_draw_sub_item(self)
        return True

    ################################################
    ## @ on_draw_column_heade : 连接头的重绘函数.
    def __on_draw_column_heade_hd(self, e):
        print "on_draw_column_heade_hd......"

    @property
    def on_draw_column_heade(self):
        return self.__on_draw_column_heade

    @on_draw_column_heade.setter
    def on_draw_column_heade(self, hd):
        self.__on_draw_column_heade = hd
        self.on_queue_draw_area()

    @on_draw_column_heade.getter
    def on_draw_column_heade(self):
        return self.__on_draw_column_heade

    @on_draw_column_heade.deleter
    def on_draw_column_heade(self):
        del self.__on_draw_column_heade

    ################################################
    ## @ on_draw_item : 连.
    def __on_draw_item_hd(self, e):
        print "__on_draw_item_hd..."

    ################################################
    ## @ on_draw_sub_item : 连.
    def __on_draw_sub_item_hd(self, e):
        print "__on_draw_sub_item_hd..."
        
    @property
    def on_draw_sub_item(self, e):
        return self.__on_draw_sub_item

    @on_draw_sub_item.setter
    def on_draw_sub_item(self, hd):
        self.__on_draw_sub_item =  hd
        self.on_queue_draw_area()

    @on_draw_sub_item.getter
    def on_draw_sub_item(self):
        return self.__on_draw_sub_item

    @on_draw_sub_item.deleter
    def on_draw_sub_item(self):
        del self.__on_draw_sub_item

if __name__ == "__main__":
    def listview1_test_on_draw_column_heade(e):
        print "我俩接了哦..."
        print "listview1_test_on_draw_column_heade...."

    def listview1_test_on_draw_sub_item(e):
        print "sub item..我来啦...O(∩_∩)O哈哈~..."

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    listview1 = ListView()
    # 重载函数.
    listview1.on_draw_column_heade =  listview1_test_on_draw_column_heade
    listview1.on_draw_sub_item     =  listview1_test_on_draw_sub_item
    listview1.columns.add("姓名")
    listview1.columns.add_range(["性别", "班级"])
    listview1.items.add("皮卡丘")
    listview1.items.add_range([["齐海龙", "男", "让我"], 
                              ["明天把", "看啊", "listview"]])
    listview1.items.add_range([["齐海龙", "男", "看看"], 
                              ["明天把", "看啊", "你知道"]])
    #listview1.columns[0].text = "真的姓名"
    listview1.items[0].sub_items.add("男")
    listview1.items[0].sub_items.add("宠物")
    listview1.columns[2].text = "职位"
    listview1.columns.clear()
    listview1.columns.add_range(["name", "sex", "work"])
    ######################################################################
    print "======%s======%s======%s==" % (listview1.columns[0].text,
                              listview1.columns[1].text,
                              listview1.columns[2].text)
    for item in listview1.items:
        print "姓名:", item.sub_items[0].text, " ", 
        print "性别:", item.sub_items[1].text, " ", 
        print "职位:", item.sub_items[2].text, " " 
    listview1.items.clear()
    print listview1.items

    win.add(listview1)
    win.show_all()
    gtk.main()




