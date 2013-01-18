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

from trayicon import TrayIcon
from utils import propagate_expose, new_surface, get_text_size
from utils import pixbuf_check, text_check
from draw import draw_pixbuf, draw_text
import gtk
import atk
import cairo
import gobject


class StatusIcon(TrayIcon):
    def __init__(self):
        TrayIcon.__init__(self)
        self.set_size_request(-1, 16)
        self.init_statusiocn_widgets()
        self.init_statusiocn_values()
        self.init_statusicon_events()

    def init_statusiocn_widgets(self):
        self.__main_hbox = gtk.HBox()
        self.add(self.__main_hbox)
    
    def init_statusiocn_values(self):
        self.draw_function_id = self.draw_function

    def init_statusicon_events(self):
        self.connect("expose-event", self.statusicon_draw_expose_event)

    def draw_function(self, cr, x, y, w, h):
        pass
         
    def statusicon_draw_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        #
        cr.rectangle(*rect)
        cr.set_source_rgba(1, 1, 1, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        #
        cr = widget.window.cairo_create()
        #
        self.draw_function_id(cr, x, y, w, h)
        #
        propagate_expose(widget, event) 
        return True

    ###########################################################
    def get_tray_position(self):
        return self.window.get_position()

    def get_tray_pointer(self):
        return self.window.get_pointer()

    def status_icon_new(self, 
                        text="", 
                        pixbuf=None, 
                        type=gtk.POS_LEFT
                        ):
        widget = Element() 
        self.widget_init(widget, text, pixbuf)
        if type == gtk.POS_LEFT:
            self.__main_hbox.pack_end(widget)
        else:
            self.__main_hbox.pack_start(widget)
        self.__main_hbox.show()
        #
        #print "button pixbuf:", widget.get_pixbuf() 
        #print "button text:", widget.get_text()
        return widget

    def widget_init(self, widget, text, pixbuf):
        widget.set_size_request(-1, 16)
        if text_check(text):
            widget.set_text(text)
        if pixbuf_check(pixbuf):
            widget.set_pixbuf(pixbuf)


TRAY_TEXT_IMAGE_TYPE, TRAY_IMAGE_TEXT_TYPE = 0, 1

class Element(gtk.Button):
    __gsignals__ = {
        "popup-menu-event" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                             (gobject.TYPE_PYOBJECT,)),
        }
    def __init__(self):
        gtk.Button.__init__(self)
        self.__init_element_values()
        self.__init_element_events()

    def __init_element_values(self):
        self.__icon_theme = gtk.IconTheme()
        self.__icon_theme.append_search_path("/home/long/Desktop/source/deepin-system-tray/src/image")
        #
        self.__mode_type = TRAY_IMAGE_TEXT_TYPE
        self.__blinking_check = False
        # init event connect function.
        self.popup_menu = None
        self.expose_event = self.__expose_event_function 
        # init left line pixbuf.
        self.left_line_pixbuf = self.load_icon("Lline", size=22)
        self.left_line_w = self.left_line_pixbuf.get_width()
        self.left_line_h = self.left_line_pixbuf.get_height()
        # init right line pixbuf.
        self.right_lien_pixbuf = self.load_icon("Rline", size=22)
        self.right_line_w = self.left_line_pixbuf.get_width()
        self.right_lien_h = self.right_lien_pixbuf.get_height()

    def __init_element_events(self):
        self.connect("clicked", self.__widget_clicked_event)
        self.connect("button-press-event", self.__widget_button_press_event)
        self.connect("expose-event", self.__widget_expose_event)

    def append_search_path(self, file):
        self.__icon_theme.append_search_path(file)

    def get_pixbuf(self):
        image = self.get_image()
        if image:
            return image.get_pixbuf()
        else:
            return image

    def set_pixbuf(self, pixbuf):
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.set_image(image) 

    def set_icon_theme(self, name):
        try:
            pixbuf = self.load_icon(name)
            if pixbuf:
                self.set_pixbuf(pixbuf)
        except Exception, e:
            print "set_icon_theme[error]:", e

    def load_icon(self, name, size=16):
        return self.__icon_theme.load_icon(name, size, gtk.ICON_LOOKUP_FORCE_SIZE)

    def set_pixbuf_file(self, file_path):
        pixbuf = gtk.gdk.pixbuf_new_from_file(file_path)
        self.set_pixbuf(pixbuf)

    def set_from_file(self, file_path):
        self.set_pixbuf_file(file_path)

    def get_text(self):
        return self.get_label()

    def set_text(self, text):
        self.set_label(text)

    def set_mode_type(self, mode_type): # No
        self.__mode_type = mode_type

    def get_mode_type(self):
        return self.__mode_type

    def get_geometry(self):
        screen = self.get_screen() 
        area   = atk.Rectangle()
        origin = self.window.get_origin() 
        area.x      = origin[0] + self.allocation.x
        area.y      = origin[1] 
        area.width  = self.allocation.width
        area.height = self.allocation.height
        return (screen, area)

    def set_blinking(self, blinking_check):
        self.__blinking_check = blinking_check

    def __widget_clicked_event(self, widget):
        # emit event.
        self.emit("popup-menu-event", self.get_geometry())
        try:
            if self.popup_menu:
                self.popup_menu(widget, self.get_geometry())
        except Exception, e:
            print "widget_clicked_event[error]:", e

    def __widget_button_press_event(self, widget, event):
        if event.button == 3:
            self.emit("popup-menu-event", self.get_geometry())
                
    def __widget_expose_event(self, widget, event):
        return self.expose_event(widget, event)

    def __expose_event_function(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        x, y, w, h = rect
        #
        self.__draw_left_line(widget, cr, x, y, w, h)
        # draw text and pixbuf.
        text = widget.get_text() 
        text_w = 0
        pixbuf = widget.get_pixbuf()
        pixbuf_w = 0
        if pixbuf != None:
            pixbuf_w = pixbuf.get_width() 
            pixbuf_h = pixbuf.get_height()
            draw_pixbuf(cr, pixbuf, x + 5, y + h/2 - pixbuf.get_height()/2)
        if text != "":
            text_w, text_h = get_text_size(text)
            draw_text(cr, text, x + pixbuf_w + self.left_line_w + 5, y + h/2 - text_h/2)
        #
        self.__draw_right_line(widget, cr, x, y, w, h)
        self.__draw_press_rectangle(widget, cr, x, y, w, h)
        #
        w_padding = pixbuf_w + text_w + 8 + self.left_line_w + self.right_line_w
        widget.set_size_request(w_padding, h)
        #
        return True

    def __draw_left_line(self, widget, cr, x, y, w, h):
        # draw left line.
        if widget.get_state() in [gtk.STATE_PRELIGHT, gtk.STATE_ACTIVE]:
            draw_pixbuf(cr, 
                        self.left_line_pixbuf, 
                        x, 
                        y + h/2 - self.left_line_h/2)

    def __draw_right_line(self, widget, cr, x, y, w, h):
        # draw right line.
        if widget.get_state() in [gtk.STATE_PRELIGHT, gtk.STATE_ACTIVE]:
            draw_pixbuf(cr, 
                        self.right_lien_pixbuf, 
                        x + w - self.right_line_w, 
                        y + h/2 - self.right_lien_h/2)

    def __draw_press_rectangle(self, widget, cr, x, y, w, h):
        # draw rectangle.
        if widget.get_state() == gtk.STATE_ACTIVE:
            cr.set_source_rgba(1, 1, 1, 0.1)
            cr.rectangle(x + self.left_line_w, 
                         y, 
                         w - self.left_line_w * 2, 
                         h)
            cr.fill()

gobject.type_register(Element)
gobject.type_register(StatusIcon)

if __name__ == "__main__":
    from tray_time import TrayTime, TRAY_TIME_12_HOUR, TRAY_TIME_24_HOUR
    from tray_time import TRAY_TIME_CN_TYPE, TRAY_TIME_EN_TYPE
    from window import TrayIconWin 
    
    def popup_menu_test_function(widget, geometry):
        print "test_button_press_event" 
        metry = geometry 
        tray_icon_rect = metry[1]        
        x = tray_icon_rect[0]
        pop_win.move(x, 540) 
        pop_win.offset = 80
        pop_win.show_all()

    def tray_time_send(traytime, text, type, language_type):
        time_p = None
        if type == TRAY_TIME_12_HOUR:
            time_p = text[0]
        hour = text[0 + type]
        min = text[1 + type]
        show_str = "%s %s:%s" % (time_p, hour, min)
        if language_type == TRAY_TIME_EN_TYPE:
            show_str = "%s:%s %s" % (hour, min, time_p)
            
        time_tray.set_text(show_str)

    new_trayicon = StatusIcon()
    pop_win = TrayIconWin()
    #
    time_tray = new_trayicon.status_icon_new()
    time_tray.set_icon_theme("time_white")
    time_tray.popup_menu = popup_menu_test_function 
    test_tray = new_trayicon.status_icon_new()
    test_tray.set_icon_theme("sound_white")
    new_trayicon.show_all()
    # time.
    tray_time = TrayTime()
    tray_time.connect("send-time", tray_time_send)
    gtk.main()


