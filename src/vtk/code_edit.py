#!coding:utf-8
import pygtk
pygtk.require('2.0')
import gobject
import gtk
from gtk import gdk
  
  
'''
'''
  
class ScrolBar(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.save_x_padding = 0
        self.save_y_padding = 0
        self.move_check = False

class CodeEdit(gtk.Bin):
    def __init__(self):
        gtk.Bin.__init__(self)
        self.__init_values()
        self.set_can_focus(True)
        self.set_has_window(False)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        #

    def __init_values(self):
        self.__children = []
        self.__width = 0 # 保存宽度.
        self.__height = 0 # 保存高度.
        self.__min_width = 100 # 最小宽度.
        self.__min_height = 100 # 最小高度.
        self.__scrol_bar_size = 15 # 滚动条的大小.
        self.__line_win_width = 80 # 显示行号的宽度.
        self.__v_bar = ScrolBar()
        self.__h_bar = ScrolBar()
  
    def do_realize(self):
        gtk.Bin.do_realize(self)
        self.set_flags(gtk.REALIZED)
        # 
        self.__bin_window = gdk.Window(
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
                      | gdk.VISIBILITY_NOTIFY_MASK
                      ))
        self.__bin_window.set_user_data(self)
        # 下面滚动条.
        self.__h_window = gdk.Window(
            self.__bin_window,
            window_type=gdk.WINDOW_CHILD,
            x=0,
            y=self.allocation.height - self.__scrol_bar_size,
            width=130,
            height=self.__scrol_bar_size,
            visual=self.get_visual(),
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.__h_window.set_user_data(self)
        # 右边的滚动条.
        self.__v_window = gdk.Window(
            self.__bin_window,
            window_type=gdk.WINDOW_CHILD,
            x=self.allocation.width - self.__scrol_bar_size,
            y=0,
            width=self.__scrol_bar_size,
            height=self.allocation.height,
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.__v_window.set_user_data(self)
        # 显示行号.
        self.__line_num_window = gdk.Window(
            self.__bin_window,
            window_type=gdk.WINDOW_CHILD,
            x=0,
            y=0,
            width=self.__line_win_width,
            height=self.allocation.height,
            visual=self.get_visual(),
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.__line_num_window.set_user_data(self)
        # 布局窗口.
        self.__viewport_window = gdk.Window(
            self.__bin_window,
            window_type=gdk.WINDOW_CHILD,
            x=self.__line_win_width,
            y=0,
            width=max(self.__width, self.allocation.width),
            height=max(self.__height, self.allocation.height),
            visual=self.get_visual(),
            colormap=self.get_colormap(),
            wclass=gdk.INPUT_OUTPUT,
            event_mask=(self.get_events() 
                      | gdk.EXPOSURE_MASK
                      | gdk.BUTTON_MOTION_MASK
                      | gdk.ENTER_NOTIFY_MASK
                      | gdk.LEAVE_NOTIFY_MASK
                      | gdk.POINTER_MOTION_HINT_MASK
                      | gdk.BUTTON_PRESS_MASK
                      ))
        self.__viewport_window.set_user_data(self)
        # 设置窗口背景. 
        self.style.set_background(self.__bin_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__h_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__v_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__line_num_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__viewport_window, gtk.STATE_NORMAL)
        # 设置子控件的父窗口为bin_window.
        for child in self.__children:
            child.widget.set_parent_window(self.__viewport_window)
        #
        self.queue_resize()
        
    # 事件.
    def do_scroll_event(self, e):
        print "do_scroll_event"

    def do_motion_notify_event(self, e):
        if e.window == self.__h_window:
            if self.__h_bar.move_check:
                h_size = self.__h_window.get_size()
                self.__h_bar.x += (e.x - self.__h_bar.x) - self.__h_bar.save_x_padding
                self.__h_bar.x = min(max(self.__h_bar.x, 0), h_size[0] - self.__h_bar.w)
                self.window.process_updates(True)
                self.queue_draw()
            return True
        elif e.window == self.__v_window:
            if self.__v_bar.move_check:
                v_size = self.__v_window.get_size()
                self.__v_bar.y += (e.y - self.__v_bar.y) - self.__v_bar.save_y_padding
                self.__v_bar.y = min(max(self.__v_bar.y, 0), v_size[1] - self.__v_bar.h)
                print "v_bar.y:", self.__v_bar.y
                self.window.process_updates(True)
                self.queue_draw()
            print "v_window motion....", e.x
        elif e.window == self.__line_num_window:
            print "line num..motion.......", e.x
        else:
            return False

    def do_button_press_event(self, e):
        if e.window == self.__h_window:
            print "button press event..hhh window......"
            if self.__width > self.__get_parent_win_size()[0]:
                if self.__h_bar.x <= e.x <= (self.__h_bar.x + self.__h_bar.w):
                    self.__h_bar.move_check = True
                    self.__h_bar.save_x_padding = e.x - self.__h_bar.x
                else:
                    h_size = self.__h_window.get_size()
                    if (e.x - self.__h_bar.x) > 0:
                        self.__h_bar.x += self.__h_bar.w
                    else:
                        self.__h_bar.x -= self.__h_bar.w
                    self.__h_bar.x = min(max(self.__h_bar.x, 0), h_size[0] - self.__h_bar.w)
                    #
                    self.__set_viewport_win(self.__line_win_width - self.__h_bar.x, 
                                            -self.__v_bar.y, 
                                            self.__width, 
                                            self.__height)
                    self.queue_draw()
            return True
        elif e.window == self.__v_window:
            if self.__height > self.__get_parent_win_size()[1]:
                if self.__v_bar.y <= e.y <= (self.__v_bar.y + self.__v_bar.h):
                    self.__v_bar.move_check = True
                    self.__v_bar.save_y_padding = e.y - self.__v_bar.y
                else:
                    v_size = self.__v_window.get_size()
                    if (e.y - self.__v_bar.y) > 0:
                        self.__v_bar.y += self.__v_bar.h
                    else:
                        self.__v_bar.y -= self.__v_bar.h
                    self.__v_bar.y = min(max(self.__v_bar.y, 0), v_size[1] - self.__v_bar.h)
                    #
                    self.__set_viewport_win(self.__line_win_width - self.__h_bar.x, 
                                            -self.__v_bar.y, 
                                            self.__width, 
                                            self.__height)
                    #
                    self.queue_draw()
            return True
        elif e.window == self.__line_num_window:
            print "press line_num_window..."
            return True
        else:
            return False

    def do_button_release_event(self, e):
        if e.window == self.__h_window:
            self.__h_bar.move_check = False
            return True
        elif e.window == self.__v_window:
            self.__v_bar.move_check = False
            print "release->v_window:", e.y
            return True
        elif e.window == self.__line_num_window:
            print "release->line_num_window:", e.x
            return True
        else:
            return False

    def do_enter_notify_event(self, e):
        if e.window == self.__h_window:
            print "h window..do_button_enter_event..."
            return True
        elif e.window == self.__v_window:
            print "v window.... enter notify..."
            return True
        elif e.window == self.__line_num_window:
            print "line num window. enter notify..."
            return True
        else:
            return False
        
    def do_leave_notify_event(self, e):
        if e.window == self.__h_window:
            print "h window..do_button_leave_event..."
            return True
        elif e.window == self.__v_window:
            print "v window.... leave notify..."
            return True
        elif e.window == self.__line_num_window:
            print "line num window. leave notify..."
            return True
        else:
            return False
        
    def do_unrealize(self):
        self.__bin_window.set_user_data(None)
        self.__bin_window.destroy()
        self.__bin_window = None
        self.__h_window.set_user_data(None)
        self.__h_window.destroy()
        self.__h_window = None
        self.__v_window.set_user_data(None)
        self.__v_window.destroy()
        self.__v_window = None
        self.__line_num_window.set_user_data(None)
        self.__line_num_window.destroy()
        self.__line_num_window = None
        self.__viewport_window.set_user_data(None)
        self.__viewport_window.destroy()
        self.__viewport_window = None
        gtk.Bin.do_unrealize(self)
  
    def do_expose_event(self, event):
        if event.window == self.__line_num_window:
            self.__draw_line_num(event)
        elif event.window == self.__h_window:
            self.__draw_h_scroll_bar(event)
        elif event.window == self.__v_window:
            self.__draw_v_scroll_bar(event)
        elif event.window == self.__viewport_window:
            cr = self.__viewport_window.cairo_create()
            size = self.__viewport_window.get_size()
            cr.set_source_rgba(0, 1, 0, 0.5)
            cr.rectangle(0, 0, size[0], size[1])
            cr.fill()
            gtk.Container.do_expose_event(self, event)
            return True
        else:
            return False

    def __draw_line_num(self, event):
        gdk_win = self.get_parent_window()
        g_size = gdk_win.get_size()
        line_size = self.__line_num_window.get_size()
        cr = self.__line_num_window.cairo_create()
        cr.set_source_rgba(0, 0, 1, 0.1)
        cr.rectangle(0, 0, self.__line_win_width, g_size[1])
        cr.fill()
        return True

    def __draw_h_scroll_bar(self, event):
        h_size = self.__h_window.get_size()
        cr = self.__h_window.cairo_create()
        cr.set_source_rgba(1, 0, 0, 0.2)
        cr.rectangle(0, 0, h_size[0], h_size[1])
        cr.stroke()
        # 画横向移动块.
        cr.set_source_rgba(0, 0, 1, 0.2)
        cr.rectangle(self.__h_bar.x, 
                     self.__h_bar.y, 
                     self.__h_bar.w,
                     self.__h_bar.h)
        cr.fill()
        return True

    def __draw_v_scroll_bar(self, event):
        v_size = self.__v_window.get_size()
        cr = self.__v_window.cairo_create()
        cr.set_source_rgba(1, 0, 0, 0.2)
        cr.rectangle(0, 0, v_size[0], v_size[1])
        cr.stroke()
        # 画纵向移动块.
        cr.set_source_rgba(0, 0, 1, 0.2)
        cr.rectangle(self.__v_bar.x, 
                     self.__v_bar.y,
                     self.__v_bar.w, 
                     self.__v_bar.h)
        cr.fill()
        return True

    def do_map(self):
        gtk.Bin.do_map(self)
        self.set_flags(gtk.MAPPED)
        self.__bin_window.show()
        self.__viewport_window.show()
        self.__line_num_window.show()
        self.__h_window.show()
        self.__v_window.show()

    def do_unmap(self):
        self.__bin_window.hide()
        self.__h_window.hide()
        self.__v_window.hide()
        self.__line_num_window.hide()
        self.__viewport_window.hide()
        gtk.Bin.do_unmap(self)
  
    def do_size_request(self, req):
        req.width = 0
        req.height = 0
        # 设置子控件.
        for child in self.__children:
            child.widget.size_request()
  
    def do_size_allocate(self, allocation):
        self.allocation = allocation
        # 设置子控件.
        for child in self.__children:
            allocation = gdk.Rectangle()
            allocation.x = child.x
            allocation.y = child.y
            req = child.widget.get_child_requisition()
            allocation.width = req[0]
            allocation.height = req[1]
            child.widget.size_allocate(allocation)

        if self.flags() & gtk.REALIZED:
            gdk_win = self.get_parent_window()
            b_size = gdk_win.get_size()
            self.__bin_window.resize(max(b_size[0], self.__min_width), 
                                     max(b_size[1], self.__min_height))
            # 布局窗口.
            self.__set_viewport_win(self.__line_win_width - self.__h_bar.x, 
                                    -self.__v_bar.y, 
                                    self.__width, 
                                    self.__height)
            # 纵向滚动条.
            v_allocation   = gdk.Rectangle()
            v_size         = self.__v_window.get_size()
            v_allocation.x = b_size[0] - self.__v_window.get_size()[0]
            v_allocation.y = 0
            v_allocation.width  = v_size[0]
            v_allocation.height = b_size[1] - self.__scrol_bar_size
            self.__v_window.move_resize(*v_allocation)
            self.__v_bar.w = self.__scrol_bar_size
            self.__v_bar.h = 100 
            # 横向滚动条.
            h_allocation   = gdk.Rectangle()
            h_size         = self.__h_window.get_size()
            h_allocation.x = 0
            h_allocation.y = b_size[1] -  self.__h_window.get_size()[1]
            h_allocation.width  = b_size[0] - self.__scrol_bar_size
            h_allocation.height = h_size[1]
            self.__h_window.move_resize(*h_allocation)
            self.__h_bar.w = 100
            self.__h_bar.h = self.__scrol_bar_size
            # 行号显示窗口.
            line_allocation = gdk.Rectangle()
            line_size       = self.__line_num_window.get_size()
            line_allocation.x = 0
            line_allocation.y = 0
            line_allocation.width  = self.__line_win_width
            line_allocation.height = b_size[1]
            self.__line_num_window.move_resize(*line_allocation)

    def __set_viewport_win(self, x, y, w, h):
        g_size = self.__get_parent_win_size()
        viewport_allocation = gdk.Rectangle()
        viewport_size       = self.__viewport_window.get_size()
        viewport_allocation.x = x 
        viewport_allocation.y = y
        viewport_allocation.width  = max(w, g_size[0])
        viewport_allocation.height = max(h, g_size[1])
        self.__viewport_window.move_resize(*viewport_allocation)

    def __get_parent_win_size(self):
        gdk_win = self.get_parent_window()
        b_size = gdk_win.get_size()
        return b_size

    def do_add(self, widget):
        self.put(widget)
        gtk.Bin.do_add(self, widget)
  
    def do_remove(self, widget):
        child = self.__get_child_from_widget(widget)
        self.__children.remove(child)
        widget.unparent()
        #gtk.Bin.do_remove(self, widget)

    def __get_child_from_widget(self, widget):
        for child in self.__children:
            if child.widget == widget:
                return child

    def put(self, child, x, y):
        child1 = WidgetList()
        child1.widget = child
        child1.x = x
        child1.y = y
        self.__children.append(child1)
        if self.flags() & gtk.REALIZED:
            widget.set_parent_window(self.__viewport_window)
        child.set_parent(self)
 
    def do_forall(self, include_internals, callback, data):
        for child in self.__children:
            callback(child.widget, data)
  
    def set_size_request(self, w, h):
        if self.flags() & gtk.REALIZED:
            self.__viewport_window.size(w, h)
        else:
            self.__width = w
            self.__height = h

gobject.type_register(CodeEdit) 

class WidgetList:
    def __init__(self):
        self.widget = None
        self.x = 0
        self.y = 0


if __name__ == '__main__':
    window = gtk.Window()
    window.connect('delete-event', gtk.main_quit)
    code_edit = CodeEdit()
    code_edit.set_size_request(1000, 1000)
    code_edit.put(gtk.Button("test测试呢"), 5, 30)
    code_edit.put(gtk.Button("test测试呢"), 130, 130)
    code_edit.put(gtk.Button("test测试呢"), 120, 110)
    code_edit.put(gtk.Button("test测试呢"), 30, 30)
    code_edit.put(gtk.Button("test测试呢"), 50, 20)
    code_edit.put(gtk.Button("test测试呢让我告诉你吧"), 50, 20)
    code_edit.put(gtk.Button("test测试呢你是知道的 1500, 1500"), 1500, 120)
    code_edit.put(gtk.Button("test测试呢我来看看吧"), 50, 120)
    window.add(code_edit)
    window.show_all()
    gtk.main()



