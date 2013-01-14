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

import sys
import os
from vtk.utils import init_config, get_config_file, get_config_path
from vtk.ini import Config


class ModulesInfo(object):
    def __init__(self):
        self.id      = ""
        self.include = ""
        self.menu_icon = ""
        self.main_icon = ""

def save_modules_info(config, path):
    include = config.get("main", "include")
    if include:
        menu_icon = config.get("main", "menu_icon")
        main_icon = config.get("main", "icon")
        id        = config.get("main", "id")
        # save mofules info.   
        modules_info           = ModulesInfo()
        modules_info.id        = id
        modules_info.include   = include
        modules_info.menu_icon = os.path.join(path, menu_icon)
        modules_info.main_icon = os.path.join(path, main_icon)
        return modules_info
    else:
        return None

def add_sys_path(path):
    '''add path to sys path'''
    sys.path.append(path)
    
class PluginManage(object):
    def __init__(self):
        # init config.
        init_config()
        #
        self.key_dict = {}
        self.keywords = []
        self.config = Config(get_config_file())
        tray_path_list = self.config.get("tray", "PATH").split(",")
        for tray_path in tray_path_list:
            if tray_path != "":
                if os.path.exists(tray_path):
                    if os.path.isdir(tray_path):
                        self.scan_tray_path_modules(tray_path)

    def scan_tray_path_modules(self, scan_path):
        scan_modules_path_list = os.listdir(scan_path)
        # add path to sys path.
        add_sys_path(scan_path)
        #
        for modules_path in scan_modules_path_list:
            modules_path_name = os.path.join(scan_path, modules_path)
            if os.path.isdir(modules_path_name):
                #print "modules_path_name:", modules_path_name
                modules_path_config = os.path.join(modules_path_name, "config.ini")
                if os.path.exists(modules_path_config):
                    modules_ini = Config(modules_path_config)
                    modules_info = save_modules_info(modules_ini, modules_path_name)
                    if modules_info:
                        try:
                            #print "include:", modules_info.include
                            #print "menu_icon:", modules_info.menu_icon
                            #print "main_icon:", modules_info.main_icon
                            modual = __import__("%s.%s" % (modules_info.id, modules_info.include), fromlist=["keywords"])
                            class_init = modual.return_plugin()
                            class_run = class_init()
                            class_run.menu_icon = modules_info.menu_icon
                            class_run.main_icon = modules_info.main_icon
                            self.keywords.append(class_run)
                            self.key_dict[class_run.id()] = class_run
                        except Exception, e:
                            print "tray plugin error:", e


if __name__ == "__main__":
    PluginManage()

                
