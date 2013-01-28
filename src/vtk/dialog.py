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

from window import Window
import gtk

class Dialog(Window):
    def __init__(self):
        Window.__init__(self)
        self.fixed = gtk.Fixed()
        self.fixed.put(gtk.Button("-"), 255, 0)
        self.fixed.put(gtk.Button("O"), 275, 0)
        self.fixed.put(gtk.Button("x"), 300, 0)
        self.fixed.put(gtk.TextView(), 100, 100)
        self.add_widget(self.fixed)
        self.set_opacity(0.5)
        self.show_all()

if __name__ == "__main__":
    dialog = Dialog()
    dialog.resize(300, 300)
    gtk.main()

