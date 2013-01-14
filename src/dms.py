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



import gobject
import gio


class Dms(gobject.GObject):
    __gsignals__ = {
         "changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
         }
    def __init__(self, dms_service):
        gobject.GObject.__init__(self)
        self.dms_service = dms_service
        # create dms service.
        self.create_service()
        # connect dms service. 
        self.connect_service()

    def create_service(self):
        fp = open(self.dms_service, "w")
        fp.close()

    def connect_service(self):
        gfile = gio.File(self.dms_service)
        gmonitor = gfile.monitor(gio.FILE_MONITOR_NONE, None)
        gmonitor.connect("changed", self.gfile_changed)

    def gfile_changed(self, monitor, file, other, evt_type):
        CREATE_FLAGS = gio.FILE_MONITOR_EVENT_CREATED
        if evt_type == CREATE_FLAGS:
            fp = open(self.dms_service, "r") 
            commandline = fp.readline()
            fp.close()
            commandline = commandline.replace("\n", "")
            emit_cmd = commandline.split(";")
            self.emit("changed", emit_cmd)


if __name__ == "__main__":
    import gtk
    def dms_changed(dms, emit_list):
        print "emit:", emit_list

    dms = Dms("/tmp/msg.tmp")
    dms.connect("changed", dms_changed)
    gtk.main()


