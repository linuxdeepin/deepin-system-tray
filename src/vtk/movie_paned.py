#! /usr/bin/ python
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


import gtk
from gtk import gdk
import gobject
from movie_window import MovieWindow
from listview import ListView



class Paned(gtk.Bin):
    def __init__(self):
        gtk.Bin.__init__(self)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.__init_values()

    def __init_values(self):
        #
        self.__child1 = None
        self.__child2 = None
        self.__child2_move_width = 250
        self.__child2_min_width  = 220
        #
        self.__handle = None
        self.__handle_pos_x = self.__child2_move_width
        self.__handle_pos_y = 0
        self.__handle_pos_w = 8
        self.__handle_pos_h = 0
        #self.__show_handle  = False
        self.__show_handle  = True
        self.__end_pixbuf =  gtk.gdk.pixbuf_new_from_file("test.png")
        self.__out_pixbuf =  gtk.gdk.pixbuf_new_from_file("test2.png")

    def do_realize(self):
        gtk.Bin.do_realize(self)
        self.set_realized(True)
        self.allocation.x = 0
        self.allocation.y = 0
        self.window = gdk.Window(
            self.get_parent_window(),
            window_type=gdk.WINDOW_CHILD,
            x=self.allocation.x,
            y=self.allocation.y,
            width=self.allocation.width,
            height=self.allocation.height,
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            visual=self.get_visual(),
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.window.set_user_data(self)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.__init_handle_window()
        if self.__child1:
            self.__child1.set_parent_window(self.window)
        if self.__child2:
            self.__child2.set_parent_window(self.window)
        self.queue_resize()

    def __init_handle_window(self):
        self.__handle = gdk.Window(
            self.window,
            window_type=gdk.WINDOW_CHILD,
            #wclass=gdk.INPUT_ONLY,
            wclass=gdk.INPUT_OUTPUT,
            x=self.__handle_pos_x,
            y=self.__handle_pos_y,
            width=self.__handle_pos_w, 
            height=self.allocation.height,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_PRESS_MASK
                      | gdk.BUTTON_RELEASE_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      ))
        self.__handle.set_user_data(self)
        self.style.set_background(self.__handle, gtk.STATE_NORMAL)
        if (self.__child1 and self.__child1.get_visible() and 
            self.__child2 and self.__child2.get_visible()):
            self.__handle.show()

    def do_unrealize(self):
        gtk.Bin.do_unrealize(self)

    def do_map(self):
        gtk.Bin.do_map(self)
        self.set_flags(gtk.MAPPED)

        self.__handle.show()
        self.window.show()

    def do_unmap(self):
        gtk.Bin.do_unmap(self)
        self.__handle.hide()
        
    def do_expose_event(self, e):
        gtk.Bin.do_expose_event(self, e)
        #print e.window, self.__handle
        self.__paint_handle(e)
        return False

    def __paint_handle(self, e):
        cr = self.__handle.cairo_create()
        if self.__show_handle:
            if self.get_move_width() == 0:
                pixbuf = self.__out_pixbuf
            else:
                pixbuf = self.__end_pixbuf
            #pixbuf = gtk.gdk.pixbuf_new_from_file("test.png")
            self.__handle_pos_w = pixbuf.get_width()
            self.__handle_pos_h = pixbuf.get_height()
            y = self.allocation.y + self.allocation.height/2 - self.__handle_pos_h/2
            cr.set_source_pixbuf(pixbuf, 0, y) 
            cr.paint_with_alpha(1.0)
        else:
            pass

    def do_motion_notify_event(self, e):
        print "event.x:", e.x
        return False

    def do_button_press_event(self, e):
        print "do_button_press_event...", e.window
        if e.window == self.__handle:
            if self.get_move_width() == 0:
                self.set_move_width(100)
                self.__set_all_size()
            else:
                self.set_jmp_end()
                self.__set_all_size()

        return False

    def do_size_allocate(self, allocation):
        self.allocation = allocation
        save_x = self.allocation.x
        self.allocation.x = 0
        self.allocation.y = 0
        # 
        self.__set_all_size()

    def __set_all_size(self):
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*self.allocation)
        # 左边的控件.
        if self.__child1:
            child1_allocation = gdk.Rectangle()
            child1_allocation.x = 0 
            child1_allocation.y = 0 
            child1_allocation.width = self.allocation.width - self.__child2_move_width
            child1_allocation.height = self.allocation.height
            self.__child1.size_allocate(child1_allocation)
        # 右边的控件.
        if self.__child2:
            child2_allocation = gdk.Rectangle()
            child2_allocation.width = self.__child2_move_width
            child2_allocation.height = self.allocation.height
            child2_allocation.x = child1_allocation.width 
            child2_allocation.y = 0
            self.__child2.size_allocate(child2_allocation)
        self.__handle_pos_x = child2_allocation.x
        self.__handle_pos_y = child2_allocation.y
        if self.__handle:
            self.__handle.move_resize(
                    self.__handle_pos_x - self.__handle_pos_w,
                    #self.__handle_pos_x,
                    self.__handle_pos_y,
                    self.__handle_pos_w,
                    self.allocation.height
                    )

    def do_forall(self, include_internals, callback, data):
        if self.__child1:
            callback(self.__child1, data)
        if self.__child2:
            callback(self.__child2, data)

    def do_size_request(self, req):
        if self.__child1:
            self.__child1.size_request()
        if self.__child2:
            self.__child2.size_request()

    def do_add(self, widget):
        gtk.Bin.do_add(self, widget)

    def do_remove(self, widget):
        widget.unparent()

    ####################################
    def add1(self, widget):
        self.__child1 = widget
        self.__child1.set_parent(self)

    def add2(self, widget):
        self.__child2 = widget
        self.__child2.set_parent(self)
    
    def add_image(self, widget):
        self.__image = widget
        self.__image.set_parent(self)

    def set_min_width(self, width=150):
        self.__child2_min_width = width

    def set_move_width(self, width):
        self.__child2_move_width = max(width, self.__child2_min_width)

    def get_move_width(self):
        return self.__child2_move_width

    def set_jmp_end(self):
        self.__child2_move_width = 0

    def set_show_handle(self, show_check=True):
        self.__show_handle = show_check

    def get_show_handle(self):
        return self.__show_handle

gobject.type_register(Paned) 



if __name__ == "__main__":
    def movie_screen_clicked(widget):
        #paned.set_move_width(0)
        if not paned.get_show_handle():
            #paned.set_move_width(100)
            paned.set_show_handle()
            paned.queue_draw()
        else:
            #paned.set_jmp_end()
            paned.set_show_handle(False)
            paned.queue_draw()

    def top_btn_clicked(widget):
        print "********"
        if paned.get_move_width() == 0:
            paned.set_move_width(100)
        else:
            paned.set_jmp_end()

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    paned = Paned()
    #
    movie_window = MovieWindow()
    scroll_win = gtk.ScrolledWindow()
    listview1    = ListView()
    listview1.columns.add_range(["性别", "职业", "国籍", "企业", "前景", "背景",
                                 "性别", "职业", "国籍", "企业", "前景", "背景",
                                 "性别", "职业", "国籍", "企业", "前景", "背景",
                                ])
    for i in range(1, 100):
        listview1.items.add_range([["求伯灿" + str(i), "男", "程序员", "中国"], 
                                  ["linus", "男", "内核开发", "荷兰"]])
    scroll_win.add_with_viewport(listview1)
    #
    paned.add1(movie_window)
    paned.add2(scroll_win)
    movie_screen = gtk.DrawingArea()
    #
    #movie_window.add(movie_screen)
    bottom_btn = gtk.Button("bottom..........")
    movie_window.bottom_add_widget(bottom_btn)
    top_btn = gtk.Button("top....top....")
    top_btn.connect("clicked", top_btn_clicked)
    bottom_btn.connect("clicked", movie_screen_clicked)
    movie_window.top_add_widget(top_btn)
    #
    win.add(paned)
    win.show_all()
    #print movie_screen.window.xid
    gtk.main()


