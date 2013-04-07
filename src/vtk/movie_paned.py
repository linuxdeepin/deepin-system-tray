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



class Paned(gtk.Bin):
    def __init__(self):
        gtk.Bin.__init__(self)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.__init_values()

    def __init_values(self):
        self.__child1 = None
        self.__child2 = None
        self.__child2_move_width = 150
        self.__child2_min_width  = 1

    def do_realize(self):
        gtk.Bin.do_realize(self)
        print "do_realize:"
        '''
        if self.__child1:
            self.__child1.set_parent_window(self.window)
            self.__child2.set_parent_window(self.window)
        '''
        self.queue_resize()

    def do_unrealize(self):
        gtk.Bin.do_unrealize(self)
        print "do_unrealize..."

    def do_map(self):
        print "do_map..."
        gtk.Bin.do_map(self)
        self.set_flags(gtk.MAPPED)
        self.window.show()

    def do_unmap(self):
        print "do_unmap..."
        gtk.Bin.do_unmap(self)
        
    def do_expose_event(self, e):
        cr = e.window.cairo_create()
        cr.set_source_rgba(0, 0, 1, 0.5)
        cr.rectangle(*self.allocation)
        cr.fill()
        gtk.Bin.do_expose_event(self, e)
        return True

    def do_size_allocate(self, allocation):
        print "allocation:", allocation
        self.allocation = allocation
        # 左边的控件.
        if self.__child1:
            print "allocation child1...."
            child1_allocation = gdk.Rectangle()
            child1_allocation.x = self.allocation.x
            child1_allocation.y = self.allocation.y
            child1_allocation.width = self.allocation.width - self.__child2_move_width
            child1_allocation.height = self.allocation.height
            self.__child1.size_allocate(child1_allocation)
        # 右边的控件.
        if self.__child2:
            print "allocation child1...."
            child2_allocation = gdk.Rectangle()
            child2_allocation.x = self.allocation.x + self.allocation.width - self.__child2_move_width
            child2_allocation.y = self.allocation.y
            child2_allocation.width = self.__child2_move_width
            child2_allocation.height = self.allocation.height
            self.__child2.size_allocate(child2_allocation)

    def do_forall(self, include_internals, callback, data):
        if self.__child1:
            print self.__child1
            callback(self.__child1, data)
        if self.__child2:
            callback(self.__child2, data)

    def do_size_request(self, req):
        print "req:", req
        if self.__child1:
            self.__child1.size_request()
        if self.__child2:
            self.__child2.size_request()

    def do_add(self, widget):
        print "do_add..."
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
    
    def set_min_width(self, width):
        self.__child2_min_width = width

    def set_move_width(self, width):
        self.__child2_move_width = width

    def get_move_width(self):
        return self.__child2_move_width



gobject.type_register(Paned) 



if __name__ == "__main__":
    def btn_clicked_event(widget):
        paned.set_move_width(paned.get_move_width() - 20)
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    paned = Paned()
    btn = gtk.Button("fjdskf")
    btn.connect("clicked", btn_clicked_event)
    paned.add1(btn)
    paned.add2(gtk.Button("f22222"))
    paned.set_move_width(350)
    paned.set_min_width(100)
    win.add(paned)
    win.show_all()
    gtk.main()


