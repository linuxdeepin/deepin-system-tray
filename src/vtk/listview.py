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



from draw import draw_text
import gtk

# view state.
VIEW_LARGEICON =  0
VIEW_SMALLICON =  1
VIEW_LIST      =  2 
VIEW_DETAILS   =  3
VIEW_TILE      =  4 
# header text alignemnt.


#class ListView(gtk.DrawingArea):
class ListView(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        self.__init_values()
        self.__init_events()

    def __init_values(self):
        self.test_h = 0
        self.__expose_check = True
        self.__grid_lines   = False
        self.__view_state   = VIEW_DETAILS
        self.__drag_columns_check = False
        self.__drag_columns_index = 0
        self.__drag_columns_start_x = 0
        self.__item_padding_height = 20
        # 重绘连接事件.
        self.on_draw_column_header = self.__on_draw_column_header
        self.on_draw_subitem       = self.__on_draw_subitem
        self.select_items   = [] # 
        self.columns        = [] # add ColumnHeader
        self.items          = [] # add ListViewItem

    def __init_events(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("button-press-event", self.__list_view_button_press_event)
        self.connect("button-release-event", self.__list_view_button_release_event)
        self.connect("motion-notify-event", self.__list_view_motion_notify_event)
        self.connect("expose-event", self.__list_view_expose_event)

    def view(self, state): # view { LargeIcon, SmallIcon, List, Details, Tile }
        self.__view_state = state

    def grid_lines(self, check):
        self.__grid_lines = check

    def columns_add(self, column):
        self.columns.append(column)
        self.__list_view_queue_draw()

    def columns_addrange(self, columns_list):
        self.columns.extend(columns_list)
        self.__list_view_queue_draw()

    def items_add(self, item):
        self.items.append(item)
        self.__list_view_queue_draw()

    def items_addrange(self, items_list):
        self.items.extend(items_list)
        self.__list_view_queue_draw()

    def ensure_visible(self):
        pass

    def start_update(self):
        self.__expose_check = False

    def end_update(self):
        self.__expose_check = True
        self.__list_view_queue_draw()

    def clear(self):
        self.columns = []
        self.items   = []

    def __list_view_queue_draw(self):
        if self.__expose_check:
            # 重绘可见的区域.
            rect = self.allocation
            self.queue_draw_area(rect.x, rect.y, rect.width, rect.height)

    def __list_view_button_press_event(self, widget, event):
        event_width = 0
        event_x = int(event.x)
        for column in self.columns:
            event_width += column.width
            if event_width <= event_x <= event_width + 2: # 按下的在这个区域内.
                self.__drag_columns_check = True # 保存可拖动标志位.
                self.__drag_columns_start_x = event_x # 保存这次的 event.x
                break
            self.__drag_columns_index = self.__drag_columns_index + 1 # columns的索引值.

    def __list_view_button_release_event(self, widget, event):
        # 重置拖动ColumnHeader的参数.
        self.__drag_columns_check = False
        self.__drag_columns_index = 0
        self.__drag_columns_start_x = 0

    def __list_view_motion_notify_event(self, widget, event):
        if self.__drag_columns_check:
            event_x = int(event.x)
            drag_move_width = event_x - self.__drag_columns_start_x
            self.__drag_columns_start_x = event_x # 保存这次的 event.x
            self.columns[self.__drag_columns_index].width += int(drag_move_width)
            self.__list_view_queue_draw()

    def __list_view_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        # 
        e = self.__save_draw_listviewitem_event_args(widget, event, cr, rect)
        #
        for i in range(0, int(rect.height/self.__item_padding_height) + 1):
            cr.rectangle(rect.x, 
                         rect.y + i * self.__item_padding_height, 
                         rect.width, 
                         self.__item_padding_height)
            cr.stroke()
        # 画.
        text_width = 0
        for column in self.columns:
            print "column:", column.text
            e.text = column.text
            e.x    = rect.x + text_width
            e.y    = rect.y
            e.width = column.width
            e.height = self.__item_padding_height
            self.on_draw_column_header(e) # 画列头columns.
            text_width += column.width
        self.on_draw_item(e)
        # 画子.
        text_height = 0
        for item in self.items:
            text_width  = 0
            text_height += self.__item_padding_height
            for sub, column in map(lambda x, y:(x,y), item.sub_items, self.columns):
                if sub:
                    e.text = sub.text
                else:
                    item.sub_items.append(SubItem(""))
                    e.text = ""
                e.x    = rect.x + text_width 
                e.y    = rect.y + text_height
                e.width  = column.width
                e.height = self.__item_padding_height
                e.sub_item_index = int(text_height / self.__item_padding_height)
                self.on_draw_subitem(e) # 画子列.
                text_width += column.width
        #
        return self.__expose_check

    def __save_draw_listviewitem_event_args(self, widget, event, cr, rect):
        e = DrawListViewItemEventArgs()
        e.widget = widget
        e.event  = event
        e.cr     = cr
        e.rect   = rect
        e.select_items = self.select_items
        return e

    def __on_draw_column_header(self, e):
        draw_text(e.cr, e.text, e.x , e.y, text_color="#000000")
        e.cr.rectangle(e.rect.x + e.x + e.width, e.y, 1, e.rect.height)
        e.cr.fill()

    def on_draw_item(self, e):
        print "on_draw_item:", e

    def __on_draw_subitem(self, e):
        draw_text(e.cr, e.text, e.x,e.y, text_color="#000000")

class ColumnHeader(object):
    def __init__(self):
        self.text = ""
        self.text_align = "left"
        self.width = 30 

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
        self.text   = ""
        self.x      = 0
        self.y      = 0
        self.rect   = None
        self.event  = None
        self.widget = None
        self.select_items = None
        self.sub_item_index = 0
        

if __name__ == "__main__":
    def test_on_subitem(e):
        if e.sub_item_index in [1, 3, 5, 7]:
            draw_text(e.cr, e.text, e.x,e.y, text_color="#0000FF")
        else:
            draw_text(e.cr, e.text, e.x,e.y, text_color="#000000")

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)

    list_view1 = ListView()
    list_view1.on_draw_subitem = test_on_subitem
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
    listview_item3 = ListViewItem()

    listview_item1.sub_items.append(SubItem("学生"))
    listview_item1.sub_items.append(SubItem("高中"))
    listview_item1.sub_items.append(SubItem("42"))
    
    listview_item2.sub_items.append(SubItem("精灵"))
    listview_item2.sub_items.append(SubItem("初三"))
    listview_item2.sub_items.append(SubItem("19"))

    listview_item3.sub_items.append(SubItem("惊吓"))
    listview_item3.sub_items.append(SubItem("初二"))
    listview_item3.sub_items.append(SubItem("29"))

    # append ...
    list_view1.columns_addrange([column_header1, column_header2])
    list_view1.columns_add(column_header3)
    list_view1.items_addrange([listview_item1, listview_item2])
    list_view1.items_add(listview_item3)

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
        column_header = ColumnHeader()
        column_header.text = "性别"
        list_view1.columns_add(column_header)

        list_view1.columns[0].width += 10
        list_view1.items[0].sub_items[0].text = "可爱的LD"
        list_view1.items[1].sub_items[2].text = "深度Linux"
        list_view1.queue_draw()

    #list_view1.start_update()
    #list_view1.end_update()
    list_view1.grid_lines(True)
    test_vbox = gtk.VBox()
    test_btn = gtk.Button("click")
    test_btn.connect("clicked", test_btn_clicked)
    test_vbox.pack_start(list_view1, True, True)
    test_vbox.pack_start(test_btn, False, False)
    win.add(test_vbox)
    win.show_all()
    gtk.main()



