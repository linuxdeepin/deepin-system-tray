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
from utils import get_text_size, get_match_parent, get_offset_coordinate
from utils import is_single_click, is_double_click
from listview_base import type_check
from listview_base import ListViewBase
from listview_base import View, Text
import pango
import gtk



'''
!!再也不用写item了.那是一件幸福的事情.
DrawItem 事件可以针对每个 ListView 项发生。
当 View 属性设置为 View = Details 时，
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
        self.__init_values_events()
        self.__init_values_columns()
        self.__init_values_items()

    def __init_values_events(self):
        self.__on_draw_column_heade = self.__on_draw_column_heade_hd
        self.__on_draw_sub_item     = self.__on_draw_sub_item_hd
        self.__on_draw_item         = self.__on_draw_item_hd
        # 保存双击的事件.
        self.__double_click_hd = None

    def __init_values_columns(self):
        self.__columns_padding_height = 30

    def __init_values_items(self):
        self.__items_padding_height = 30
        # 保存双击items.
        self.__double_items = None

    def __init_events(self):
        self.connect("realize",              self.__listview_realize_event)
        self.connect("motion-notify-event",  self.__listview_motion_notify_event)
        self.connect("button-press-event",   self.__listview_button_press_event)
        self.connect("button-release-event", self.__listview_button_release_event)
        self.connect("enter-notify-event",   self.__listview_enter_notify_event)
        self.connect("leave-notify-event",   self.__listview_leave_notify_event)
        self.connect("expose-event",         self.__listview_expose_event)

    def __listview_realize_event(self, widget):
        widget.set_realized(True)

        scroll_win = get_match_parent(widget, "ScrolledWindow")
        if scroll_win:
            scroll_win.get_vadjustment().connect("value-changed",
                                    self.__scroll_win_vajustment_changed)
            scroll_win.get_hadjustment().connect("value-changed",
                                    self.__scroll_win_hajustment_changed)
            scroll_win.connect("scroll-event", self.__scroll_win_scroll_event)

    def __scroll_win_scroll_event(self, widget, event):
        self.__scroll_win_event()

    def __scroll_win_vajustment_changed(self, adjustment):
        self.__scroll_win_event()

    def __scroll_win_hajustment_changed(self, adjustment):
        self.__scroll_win_event()

    def __scroll_win_event(self):
        self.on_queue_draw_area()
        self.window.process_updates(True)
        self.window.process_updates(True)
        self.on_queue_draw_area()

    def __listview_motion_notify_event(self, widget, event):
        #print "__listview_motion_notify_event..."
        row_index, col_index = self.__get_items_mouse_data(event)
        '''
        if not (None in [row_index, col_index]):
            print self.items[row_index].sub_items[col_index].text
        else:
            print "motion..==========================="
        pass
        '''

    def __listview_button_press_event(self, widget, event):
        # 判断双击的区域.
        if is_double_click(event):
            row_index, col_index = self.__get_items_mouse_data(event)
            if not (None in [row_index]):
                self.__double_items = self.items[row_index]
                if self.__double_click_hd:
                    self.__double_click_hd(self, self.__double_items, row_index, col_index)
                self.on_queue_draw_area()

    def __listview_button_release_event(self, widget, event):
        #print "__listview_button_release_event..."
        # 获取标题头触发的release事件返回的x索引.
        col_index =  self.__get_columns_mouse_data(event)
        if col_index != None:
            print self.columns[col_index].text
        else:
            # 获取items触发的release事件返回的x,y索引.
            row_index, col_index = self.__get_items_mouse_data(event)
            if not (None in [row_index, col_index]):
                print self.items[row_index].sub_items[col_index].text

    def __listview_enter_notify_event(self, widget, event):
        #print "__listview_enter_enter...notify_event..."
        pass

    def __listview_leave_notify_event(self, widget, event):
        #print "__listview_leave_notify_event...."
        pass

    def connect_event(self, event_name, function_point):
        if event_name == "double-click":
            self.__double_click_hd = function_point

    def __listview_expose_event(self, widget, event):
        #print "__listview_expose_event.."
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        if self.view == View.DETAILS: # 带标题头的视图, 比如详细信息.
            self.__draw_view_details(cr, rect, widget)
        #elif self.view == 
        #
        # 设置窗体的高度和宽度.
        self.__set_listview_size()
        return True

    def __draw_view_details(self, cr, rect, widget):
        #self.on_draw_item(e)
        temp_column_w = 0
        offset_x, offset_y, viewport = get_offset_coordinate(widget)
        for index, column in enumerate(self.columns): # 绘制标题头.
            # 保存属性.
            e = ColumnHeaderEventArgs()
            e.cr     = cr
            e.column = column 
            e.column_index = index
            e.text = column.text
            e.x = rect.x + temp_column_w
            e.y = offset_y + rect.y
            e.w = column.width
            e.h = self.__columns_padding_height + 1
            e.text_color = column.text_color
            #
            temp_column_w += column.width
            self.on_draw_column_heade(e)
        # 
        temp_item_h  = self.__columns_padding_height
        # 优化listview.
        # 获取滚动窗口.
        scroll_win = get_match_parent(self, "ScrolledWindow")
        scroll_rect_h = rect.height
        if scroll_win: # 如果没有滚动窗口,直接获取listview的高度.
            scroll_rect_h = scroll_win.allocation.height
        # dtk.ui.listview ===>>>
        start_y = offset_y - self.__columns_padding_height
        end_y   = offset_y + viewport.allocation.height - self.__columns_padding_height
        start_index  = max(start_y / self.__items_padding_height, 0)
        end_index    = (start_index + (scroll_rect_h + self.__columns_padding_height)/ self.__items_padding_height) + 1
        # 
        # 剪切出绘制items的区域,防止绘制到标题头上.
        cr.save()
        cr.rectangle(rect.x + offset_x, 
                     rect.y + offset_y + self.__columns_padding_height, 
                     scroll_win.allocation.width, 
                     scroll_win.allocation.height)
        cr.clip()
        #
        for row, item in enumerate(self.items[start_index:end_index]):
            temp_item_w = 0
            # 行中的列元素.
            for column, sub_item in map(lambda s, c:(s, c), 
                                        self.columns,  
                                        item.sub_items):
                if column and sub_item:
                    # 保存subitem的所有信息.
                    e = SubItemEventArgs()
                    e.cr = cr
                    e.sub_item = sub_item
                    e.double_items = self.__double_items
                    e.item     = item
                    e.text = sub_item.text
                    e.text_color = sub_item.text_color
                    e.x = rect.x + temp_item_w
                    e.y = rect.y + ((row + start_index) * self.__items_padding_height) + self.__columns_padding_height
                    e.w = column.width
                    e.h = self.__items_padding_height 
                    e.sub_item_index = row + start_index
                    temp_item_w += column.width
                    #
                    self.on_draw_sub_item(e)
            # 保存绘制行的y坐标.
            temp_item_h += self.__items_padding_height
        cr.restore()

    ################################################
    ## @ on_draw_column_heade : 连接头的重绘函数.
    def __on_draw_column_heade_hd(self, e):
        e.cr.set_source_rgba(0, 0, 0, 0.1)
        e.cr.rectangle(e.x, e.y, e.w, e.h)
        e.cr.fill()
        if self.columns[len(self.columns)-1] == e.column:
            e.cr.rectangle(e.x + e.w, e.y, self.allocation.width - e.x, e.h)
            e.cr.fill()
        # 画标题栏文本.
        draw_text(e.cr, 
                  e.text,
                  e.x, e.y, e.w, e.h,
                  text_color=e.text_color,
                  alignment=Text.CENTER)
        #

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
    ## @ on_draw_item : 连. 当 owner_draw 设置为真的时候发生.
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
        if e.double_items == e.item:
            e.text_color = "#0000ff"
        e.draw_text(e.cr, 
                  e.text, 
                  e.x, e.y, e.w, e.h,
                  text_color=e.text_color, 
                  alignment=Text.CENTER)
        
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

    def __set_listview_size(self):
        # 设置listview的高度和宽度.
        rect = self.allocation
        listview_height =  (len(self.items)) * self.__items_padding_height + self.__columns_padding_height
        listview_width  =  188 # 额外添加 188 的宽度.
        for column in self.columns:
            listview_width += column.width 
        if (rect.height != listview_height) or (rect.width != listview_width):
            self.set_size_request(listview_width, listview_height)

    def __get_items_mouse_data(self, event):
        offset_x, offset_y, viewport = get_offset_coordinate(self)
        if self.__in_items_check(offset_y, event):
            event_x = event.x # 获取鼠标x.
            # 获取行号.
            event_y_padding = int(event.y - self.__columns_padding_height)
            row_index = event_y_padding / self.__items_padding_height
            x_padding = 0
            col_index = 0
            # 获取行item,列的sub_items.
            for column in self.columns:
                if x_padding <= int(event.x) <= x_padding + column.width:
                    break
                x_padding += column.width
                col_index += 1
            # 判断是否在可显示的列内.
            if ((row_index < len(self.items)) and 
                (col_index < len(self.items[row_index].sub_items))):
                return row_index, col_index
            else:
                return row_index, None
        else: # 鼠标点击不在区域内.
            return None, None

    def __in_items_check(self, offset_y, event):
        start_y = (offset_y) + self.__columns_padding_height
        end_y   = start_y + ((len(self.items)) * self.__items_padding_height)
        return (start_y < event.y < end_y)

    def __get_columns_mouse_data(self, event):
        offset_x, offset_y, viewport = get_offset_coordinate(self)
        if self.__in_columns_check(offset_y, event):
            # 获取行item,列的sub_items.
            x_padding = 0
            col_index = 0
            for column in self.columns:
                if x_padding <= int(event.x) <= x_padding + column.width:
                    return col_index
                x_padding += column.width
                col_index += 1
            return None

    def __in_columns_check(self, offset_y, event):
        start_y = offset_y
        end_y   = start_y + self.__columns_padding_height
        return (start_y < event.y < end_y)

    # 设置每行的高度.
    @property
    def items_height(self):
        return self.__items_padding_height
    
    @items_height.setter
    def items_height(self, height):
        self.__items_padding_height = height
        self.on_queue_draw_area()

    @items_height.getter
    def items_height(self):
        return self.__items_padding_height

    @items_height.deleter
    def items_height(self):
        del self.__items_padding_height

    # 设置标题头的高度.
    @property
    def columns_height(slef):
        return self.__columns_padding_height

    @columns_height.setter
    def columns_height(self, height):
        self.__columns_padding_height = height
        self.on_queue_draw_area()

    @columns_height.getter
    def  columns_height(self):
        return self.__columns_padding_height

    @columns_height.deleter
    def columns_height(self):
        del self.__columns_padding_height

class ItemEventArgs(object):
    def __init__(self):
        self.cr = None
        self.select_items = []
        # 鼠标的起点和结束点.
        self.start_x = 0
        self.start_y = 0
        self.end_x   = 0
        self.end_y   = 0
        self.state   = 0 # 状态.
        # item.
        self.item    = None
        # Bounds
        self.x =  0
        self.y =  0
        self.w =  0
        self.h =  0


class SubItemEventArgs(object):
    def __init__(self):
        self.cr = None
        self.item = None
        self.sub_item = None
        self.sub_item_index = None
        self.double_items = None
        self.text = ""
        self.text_color = "#000000"
        self.text_align = Text.LEFT
        self.draw_text = draw_text
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

class ColumnHeaderEventArgs(object):
    def __init__(self):
        self.cr     = None
        self.column = None
        self.column_index = 0
        self.text = ""
        self.text_color = "#000000"
        self.text_align = Text.LEFT
        self.draw_text = draw_text
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
        for i in range(0, 20000):
            #listview1.items.add_insert(0, [[str(i), "男", "程序员", "美国" + str(i)]])
            listview1.items.add_range([[str(i), 
                                        "男", 
                                        "程序员", 
                                        "美国" + str(i), 
                                        "你是" + str(i), 
                                        "#FFFFFF" + str(i),
                                        "#EDEDED" + str(i)]])
        listview1.end_update()
        
    def listview1_test_on_draw_column_heade(e):
        print "listview1_test_on_draw_column_heade.... 重绘标题头"

    def listview1_test_on_draw_sub_item(e):
        print "sub item..我来啦...O(∩_∩)O哈哈~..."

    def test_listview_double_click(listview, double_items, row, col):
        print double_items.sub_items[0], row, col
        #listview.items[row].sub_items[0].text = "明天"
        listview.items.remove(double_items)

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.connect("destroy", lambda w : gtk.main_quit())
    win.set_size_request(500, 500)
    listview1 = ListView()
    listview1.connect_event("double-click", test_listview_double_click) 
    #listview1.connect_event("
    #listview1.items_height = 30
    #listview1.columns_height = 50
    listview1.set_size_request(500, 1500)
    # 连接主要绘制函数.
    #listview1.on_draw_column_heade =  listview1_test_on_draw_column_heade
    #listview1.on_draw_sub_item     =  listview1_test_on_draw_sub_item
    listview1.columns.add("姓名")
    listview1.columns.add_range(["性别", "职业", "国籍", "企业", "前景", "背景",
                                 "性别", "职业", "国籍", "企业", "前景", "背景",
                                 "性别", "职业", "国籍", "企业", "前景", "背景",
                                ])
    listview1.items.add("皮卡丘")
    listview1.items[0].sub_items.add("男")
    listview1.items[0].sub_items.add("宠物")
    listview1.items[0].sub_items.add("宠物国")
    listview1.items.add_range([["张飞", "男", "武士", "蜀国"], 
                              ["孙策", "男", "骑士", "吴国", "aaa", "b", "c", "d", "f"]])
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




