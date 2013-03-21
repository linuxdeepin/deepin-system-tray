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
from utils import get_text_size, get_match_parent
from listview_base import type_check
from listview_base import ListViewBase
from listview_base import LARGEICON, DETAILS, SMALLICON, LIST, TITLE
from listview_base import LEFT, RIGHT, MID
import gtk



'''
DrawItem 事件可以针对每个 ListView 项发生。当 View 属性设置为 View = Details 时，
还会发生 DrawSubItem 和 DrawColumnHeader 事件。
在这种情况下，可以处理 DrawItem 事件以绘制所有项共有的元素（如背景），
并处理 DrawSubItem 事件以便为各个子项（例如文本值）绘制元素。
您还可以仅使用这两个事件中的一个事件绘制 ListView 控件中的所有元素，尽管这可能不十分方便。
若要绘制详细信息视图中的列标题，必须处理 DrawColumnHeader 事件。
'''
class ListView(ListViewBase):
    def __init__(self):
        ListViewBase.__init__(self)
        self.__init_settings()
        self.__init_values()
        self.__init_events()

    def __init_settings(self):
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)

    def __init_values(self):
        #
        self.__on_draw_column_heade = self.__on_draw_column_heade_hd
        self.__on_draw_sub_item     = self.__on_draw_sub_item_hd
        self.__on_draw_item         = self.__on_draw_item_hd
        #
        self.__columns_padding_height = 30
        self.__items_padding_height = 40

    def __init_events(self):
        self.connect("motion-notify-event",  self.__listview_motion_notify_event)
        self.connect("button-press-event",   self.__listview_button_press_event)
        self.connect("button-release-event", self.__listview_button_release_event)
        self.connect("enter-notify-event",   self.__listview_enter_notify_event)
        self.connect("leave-notify-event",   self.__listview_leave_notify_event)
        self.connect("expose-event",         self.__listview_expose_event)
    
    def __listview_motion_notify_event(self, widget, event):
        #print "__listview_motion_notify_event..."
        pass

    def __listview_button_press_event(self, widget, event):
        #print "__listview_button_press_event...."
        pass

    def __listview_button_release_event(self, widget, event):
        #print "__listview_button_release_event..."
        pass

    def __listview_enter_notify_event(self, widget, event):
        #print "__listview_enter_enter...notify_event..."
        pass

    def __listview_leave_notify_event(self, widget, event):
        #print "__listview_leave_notify_event...."
        pass

    def __get_offset_coordinate(self, widget):
        rect = widget.allocation
        viewport = get_match_parent(widget, ["Viewport"])
        if viewport:
            coordinate = widget.translate_coordinates(viewport, rect.x, rect.y)
            if len(coordinate) == 2:
                (offset_x, offset_y) = coordinate
                return (-offset_x, -offset_y, viewport)
            else:
                return (0, 0, viewport)
        else:
            return (0, 0, viewport)
        

    def __listview_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        if self.view == DETAILS: # 带标题头的视图, 比如详细信息.
            self.__draw_view_details(cr, rect, widget)
        #
        return True

    def __draw_view_details(self, cr, rect, widget):
        temp_column_w = 0
        for column in self.columns: # 标题头.
            # 保存属性.
            e = ColumnHeaderEventArgs()
            e.cr     = cr
            e.column = column 
            e.text = column.text
            e.x = rect.x + temp_column_w
            e.y = rect.y
            e.w = column.width
            e.h = self.__columns_padding_height
            e.text_color = column.text_color
            #
            temp_column_w += column.width
            self.on_draw_column_heade(e)
        # 
        temp_item_h  = self.__columns_padding_height
        temp_index   = 0
        # 优化listview.
        start_index  = 0
        end_index    = start_index + rect.width / self.__columns_padding_height
        for item in self.items[start_index:end_index]: #每行元素.
            temp_item_w = 0
            # 行中的列元素.
            for column, sub_item in map(lambda s, c:(s, c), 
                                        self.columns,  
                                        item.sub_items):
                if column and sub_item:
                    #
                    e = SubItemEventArgs()
                    e.cr = cr
                    e.text = sub_item.text
                    e.text_color = sub_item.text_color
                    e.x = rect.x + temp_item_w
                    e.y = rect.y + temp_item_h
                    e.w = column.width
                    e.h = self.__items_padding_height 
                    e.sub_item_index = temp_index
                    temp_item_w += column.width
                    #
                    self.on_draw_sub_item(e)
                    self.on_draw_item(e)
            # 保存绘制行的y坐标.
            temp_item_h += self.__items_padding_height
            temp_index  += 1

    ################################################
    ## @ on_draw_column_heade : 连接头的重绘函数.
    def __on_draw_column_heade_hd(self, e):
        #print "on_draw_column_heade_hd......", e.text_color
        text_size = get_text_size(e.text)
        draw_text(e.cr, 
                  e.text,
                  e.x + e.w/2 - text_size[0]/2,
                  e.y + e.h/2 - text_size[1]/2, 
                  text_color=e.text_color)
        e.cr.set_source_rgba(0, 0, 0, 0.1)
        e.cr.rectangle(e.x, e.y, e.w, e.h)
        e.cr.fill()

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
        #print "__on_draw_item_hd..."
        pass

    @property
    def on_draw_item(self, e):
        return self.__on_draw_item

    @on_draw_item.setter
    def on_draw_item(self, hd):
        self.__on_draw_item =  hd
        self.on_queue_draw_area()

    @on_draw_item.getter
    def on_draw_item(self):
        return self.__on_draw_item

    @on_draw_item.deleter
    def on_draw_item(self):
        del self.__on_draw_item

    ################################################
    ## @ on_draw_sub_item : 连.
    def __on_draw_sub_item_hd(self, e):
        #print "__on_draw_sub_item_hd..."
        text_size = get_text_size(e.text)
        if e.text_align == MID:
            x_padding = e.w/2 - text_size[0]/2
        elif e.text_align == LEFT:
            x_padding = 0
        elif e.text_align == RIGHT:
            x_padding = e.w - text_size[0]
        draw_text(e.cr, 
                  e.text, 
                  e.x + x_padding, 
                  e.y + e.h/2 - text_size[1]/2, 
                  text_color=e.text_color)
        if e.sub_item_index in [1, 3, 5]:
            e.cr.set_source_rgba(0, 0, 1, 0.1)
        else:
            e.cr.set_source_rgba(1, 0, 0, 0.1)
        e.cr.rectangle(e.x, e.y, e.w, e.h)
        e.cr.fill()
        
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

class SubItemEventArgs(object):
    def __init__(self):
        self.cr = None
        self.sub_item = None
        self.sub_item_index = None
        self.text = ""
        self.text_color = "#000000"
        self.text_align = MID
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

class ColumnHeaderEventArgs(object):
    def __init__(self):
        self.cr     = None
        self.column = None
        self.text = ""
        self.text_color = "#000000"
        self.text_align = MID
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

if __name__ == "__main__":

    def test_btn_clicked(widget):
        #listview1.items.clear()
        #listview1.columns[3].width += 5
        #listview1.items.add_range([["微软", "男", "程序员", "美国"]])
        #listview1.items[0].sub_items.add("fdjkf")
        #listview1.items[0].sub_items[0].text = "我爱你,精灵..."
        listview1.begin_update()
        for i in range(0, 10000):
            listview1.items.add_insert(0, [["微软", "男", "程序员", "美国"]])
        listview1.end_update()

    def listview1_test_on_draw_column_heade(e):
        print "listview1_test_on_draw_column_heade.... 重绘标题头"

    def listview1_test_on_draw_sub_item(e):
        print "sub item..我来啦...O(∩_∩)O哈哈~..."

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    listview1 = ListView()
    listview1.set_size_request(500, 1500)
    # 重载函数.
    #listview1.on_draw_column_heade =  listview1_test_on_draw_column_heade
    #listview1.on_draw_sub_item     =  listview1_test_on_draw_sub_item
    listview1.columns.add("姓名")
    listview1.columns.add_range(["性别", "职业", "国籍"])
    listview1.items.add("皮卡丘")
    listview1.items[0].sub_items.add("男")
    listview1.items[0].sub_items.add("宠物")
    listview1.items[0].sub_items.add("宠物国")
    listview1.items.add_range([["张飞", "男", "武士", "蜀国"], 
                              ["孙策", "男", "骑士", "吴国"]])
    listview1.items.add_range([["求伯灿", "男", "程序员", "中国"], 
                              ["linus", "男", "内核开发", "荷兰"]])
    #
    scroll_win = gtk.ScrolledWindow()
    scroll_win.add_with_viewport(listview1)
    vbox = gtk.VBox()
    test_btn = gtk.Button("test")
    test_btn.connect("clicked",  test_btn_clicked)
    vbox.pack_start(scroll_win, True, True) 
    vbox.pack_start(test_btn, False, False)
    win.add(vbox)
    win.show_all()
    #
    listview1.columns[0].width = 245
    listview1.columns[2].width = 145
    listview1.columns[2].text = "职位"
    gtk.main()




