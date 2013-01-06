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
from dtk.ui.utils import get_parent_dir
from dtk.ui.config import Config

PATH = os.path.join(get_parent_dir(__file__, 2), "modules")
sys.path.append(PATH)

class PluginManage(object):
    def __init__(self):
        self.keywords = []
        scan_dir_list = os.listdir(PATH)
        for path in scan_dir_list:
            scan_dir_path = os.path.join(PATH, path)
            if os.path.exists(scan_dir_path):
                config_path = os.path.join(scan_dir_path, "config.ini") 
                if os.path.exists(config_path):
                    #print "scan_dir_path:", config_path 
                    config = Config(config_path, "")
                    config.load()
                    icon_path = None
                    # get modual icon.
                    if config.has_option("main", "menu_icon"):
                        icon_path = config.get("main", "menu_icon", "")

                    if config.has_option("trayicon", "include"):
                        include_name = config.get("trayicon", "include", "")
                        #print "include_name:", include_name
                        modual = __import__(include_name, fromlist=["keywords"])
                        class_init = modual.return_trayicon()
                        class_run = class_init()
                        if icon_path:
                            class_run.icon_path = os.path.join(scan_dir_path, icon_path) 

                        self.keywords.append(class_run)


if __name__ == "__main__":
    PluginManage()

                
