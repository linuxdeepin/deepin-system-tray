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



import gtk

class ListView(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)

        self.__expose_check = True
        self.select_items = [] # 
        self.columns = [] # add ColumnHeader
        self.items = [] # add ListViewItem

        self.connect("expose-event", self.list_view_expose_event)

    def view(self): # view { LargeIcon, Smallcon, List, Details, Tile }
        pass

    def ensure_visible(self):
        pass

    def start_update(self):
        self.__expose_check = False

    def end_update(self):
        self.__expose_check = True
        self.queue_draw()

    def clear(self):
        pass

    def list_view_expose_event(self, expose, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        return self.__expose_check

class ColumnHeader(object):
    def __init__(self):
        self.text = ""
        self.text_align = "left"
        self.width = 0

class ListViewItem(object):
    def __init__(self):
        self.sub_items = []

    def clear(self):
        pass

class SubItem(object):
    def __init__(self, text=""):
        self.text = text


if __name__ == "__main__":
    list_view1 = ListView()
    # column header.
    column_header1 = ColumnHeader()
    column_header2 = ColumnHeader()
    column_header3 = ColumnHeader()
    column_header1.text = "姓名"
    column_header2.text = "班级"
    column_header3.text = "座位"
    # list view item.
    listview_item1 = ListViewItem()
    listview_item2 = ListViewItem()

    listview_item1.sub_items.append(SubItem("学生"))
    listview_item1.sub_items.append(SubItem("高中"))
    listview_item1.sub_items.append(SubItem("42"))
    
    listview_item2.sub_items.append(SubItem("精灵"))
    listview_item2.sub_items.append(SubItem("初三"))
    listview_item2.sub_items.append(SubItem("19"))

    list_view1.columns.extend([column_header1, column_header2])
    list_view1.columns.append(column_header3)
    list_view1.items.extend([listview_item1, listview_item2])

    #print list_view1.items[0].sub_items[0].text

    for i in range(0, 10):
        lvi = ListViewItem()
        lvi.sub_items.append(SubItem("欧燕 item" + str(i)))
        lvi.sub_items.append(SubItem("高" + str(i)))
        lvi.sub_items.append(SubItem("1" + str(i)))
        list_view1.items.append(lvi)

    for header in list_view1.columns:
        print header.text

    for item in list_view1.items:
        print item
        for i in range(0, len(item.sub_items)):
            print "item:", item.sub_items[i].text

'''
可以进行重载的函数，任意画自己想要的东西.
OnDrawSubItem :
OnDrawItem :
OnDrawColumnHeader : 
'''


