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

# view state.
VIEW_LARGEICON =  0
VIEW_SMALLICON =  1
VIEW_LIST      =  2 
VIEW_DETAILS   =  3
VIEW_TILE      =  4 
# header text alignemnt.


class ListView(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.__init_values()
        self.__init_events()

    def __init_values(self):
        self.test_h = 0
        self.__expose_check = True
        self.__view_state   = VIEW_DETAILS
        self.select_items   = [] # 
        self.columns        = [] # add ColumnHeader
        self.items          = [] # add ListViewItem

    def __init_events(self):
        self.connect("expose-event", self.__list_view_expose_event)

    def view(self, state): # view { LargeIcon, SmallIcon, List, Details, Tile }
        self.__view_state = state

    def ensure_visible(self):
        pass

    def start_update(self):
        self.__expose_check = False

    def end_update(self):
        self.__expose_check = True
        self.queue_draw()

    def clear(self):
        self.columns = []
        self.items   = []

    def test_expose(self):
        self.test_h += 30
        if self.__expose_check:
            self.queue_draw()

    def __list_view_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        # 
        e = self.__save_draw_listviewitem_event_args(widget, event, cr, rect)
        #
        cr.rectangle(rect.x, rect.y, 100, self.test_h)
        cr.fill()
        #
        self.on_draw_column_header(e)
        self.on_draw_item(e)
        self.on_draw_subitem(e)
        print "epxo check:", self.__expose_check
        return self.__expose_check

    def __save_draw_listviewitem_event_args(self, widget, event, cr, rect):
        e = DrawListViewItemEventArgs()
        e.widget = widget
        e.event  = event
        e.cr     = cr
        e.rect   = rect
        e.select_items = self.select_items
        return e

    def on_draw_column_header(self, e):
        print "on_draw_column_header:", e

    def on_draw_item(self, e):
        print "on_draw_item:", e

    def on_draw_subitem(self, e):
        print "on_draw_subitem:", e


class ColumnHeader(object):
    def __init__(self):
        self.text = ""
        self.text_align = "left"
        self.width = 0

class ListViewItem(object):
    def __init__(self):
        self.sub_items = []

    def clear(self):
        self.sub_items = []

class SubItem(object):
    def __init__(self, text=""):
        self.text = text


class DrawListViewItemEventArgs(object):
    def __init__(self):
        self.cr     = None
        self.rect   = None
        self.event  = None
        self.widget = None
        self.select_items = None


if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)

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

    def test_btn_clicked(widget):
        list_view1.test_expose()

    list_view1.start_update()
    #list_view1.end_update()
    test_vbox = gtk.VBox()
    test_btn = gtk.Button("click")
    test_btn.connect("clicked", test_btn_clicked)
    test_vbox.pack_start(list_view1, True, True)
    test_vbox.pack_start(test_btn, False, False)
    win.add(test_vbox)
    win.show_all()
    gtk.main()



