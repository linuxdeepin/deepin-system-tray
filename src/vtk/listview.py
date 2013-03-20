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
import gtk

class ListView(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        # 初始化变量.
        self.__init_values()

    def __init_values(self):
        self.__expose_check = True # 防止大量数据加载的闪烁问题.
        self.columns = Columns() # 保存 ColumnHeader
        self.items   = Items()   # 保存 ListViewItem
        # 初始化数据更新事件.
        self.columns.connect("update-data", self.__columns_update_data_event)
        self.items.connect("update-data", self.__items_update_data_event)

    def __columns_update_data_event(self, columns):
        print "columns_update_data_event:", columns

    def __items_update_data_event(self, items):
        print "items_update_date_event:", items

    def start_update(self):
        self.__expose_check = True
        self.on_queue_draw_area()

    def end_update(self):
        self.__expose_check = False
        self.on_queue_draw_area()

    def on_queue_draw_area(self):
        # 重绘区域.
        if self.__expose_check:
            rect = widget.allocation
            self.queue_darw_area(*rect)

class Columns(list):
    def __init__(self):
        list.__init__(self)
        self.__init_values()

    def __init_values(self):
        self.__function_point = None # 函数指针.

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

    def add(self, text):
        if type(text).__name__ == "str":
            header = ColumnHeader(text)
            header.connect("update-data", self.header_update_data_event)
            self.append(header)
            header.text = text

    def add_range(self, header_list):
        pass
        

    def header_update_data_event(self, column_header):
        self.emit()

class ColumnHeader(object):
    def __init__(self, text=""):
        self.__init_values()
        self.text = text


    def __init_values(self):
        self.__text = ""  # 保存文本.
        self.text_align = None # 文本对齐方式.
        self.__width = 0 # ColumnHeader 宽度.
        self.image_key = None # 图片key.
        self.image_index = None # 图片索引.
        self.__function_point = None

    def __type_check(self, type_name, type_str):
        return type(type_name).__name__ == type_str

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.emit()

    @text.getter
    def text(self):
        return self.__text

    @text.deleter
    def text(self):
        del self.__text


class Items(list):
    def __init__(self):
        list.__init__(self)
        # 初始化变量.
        self.__init_values()

    def __init_values(self):
        self.__function_point = None

    def __type_check(self, type_name, type_str):
        return type(type_name).__name__ == type_str

    def connect(self, event_name, function_point): 
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        # 回调函数.
        if self.__function_point:
            self.__function_point(self)

    def add(self, text):
        if self.__type_check(text, "str"): # 判断是否为 ListViewItem 类型.
            listview_item = ListViewItem()
            listview_item.sub_items.add(text)
            listview_item.connect("update-data", self.__listview_item_update_data_event)
            self.append(listview_item)
            # 发送信号.
            self.emit()

    def add_range(self, text_items):
        if self.__type_check(text_items, "list"):
            emit_check = False # 初始化发送信号的标志位.
            for item in text_items:
                if self.__type_check(item, "list"):
                    if not emit_check: # 设置发送信号的标志位.
                        emit_check = True # 设置发送信号的标志位为真.
                    #
                    listview_item = ListViewItem(item)
                    listview_item.connect("update-data", self.__listview_item_update_data_event)
                    self.append(listview_item)

            if emit_check: # 判断是否发送信号.
                # 发送信号.
                self.emit()

    def __listview_item_update_data_event(self, listview_item):
        self.emit()

class ListViewItem(object):
    def __init__(self, item):
        self.__init_values()
        self.sub_items.add_range(item)

    def __init_values(self):
        self.sub_items = SubItems()
        self.sub_items.connect("update-data", self.__sub_items_update_data_event)

    def __sub_items_update_data_event(self, sub_items):
        self.emit()

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

class SubItems(list):
    def __init__(self):
        list.__init__(self)
        self.__init_values()

    def __init_values(self):
        self.__function_point = None

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

    def add(self, text):
        sub_item = SubItem(text)
        sub_item.connect("update-data", self.__sub_item_update_data_event)
        self.append(sub_item)

    def add_range(self, items_text):
        for text in items_text:
            sub_item = SubItem(text)
            sub_item.connect("update-data", self.__sub_item_update_data_event)
            self.append(sub_item)

    def __sub_item_update_data_event(self, sub_item):
        self.emit()
    

class SubItem(object):
    def __init__(self, text=""):
        self.__init_values()
        self.__text = text

    def __init_values(self):
        self.__text = ""
        self.__function_point = None

    def connect(self, event_name, function_point):
        if event_name == "update-data":
            self.__function_point = function_point

    def emit(self):
        if self.__function_point:
            self.__function_point(self)

    @property
    def text(self):
        self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.emit()

    @text.getter
    def text(self):
        return self.__text

    @text.deleter
    def text(self):
        del self.__text



'''
columns[列表] <= ColumnHeader
items[列表]   <= ListViewItem
ColumnHeader---{属性:text, width...}
ListViewItem[列表] <= SubItem---{属性:text...}
'''

if __name__ == "__main__":
    listview1 = ListView()
    listview1.columns.add("姓名")
    listview1.columns.add_range(["性别", "班级"])
    listview1.items.add_range([["齐海龙", "男"], 
                              ["明天把", "看啊"]])
    #listview1.columns[0].text = "真的姓名"
    print listview1.items[0].sub_items[0].text




