#!coding:utf-8
import pygtk
pygtk.require('2.0')
import gobject
import gtk
from gtk import gdk
  
  
'''
'''
  
class CodeEdit(gtk.Bin):
    def __init__(self):
        gtk.Bin.__init__(self)
        self.__min_width = 100
        self.__min_height = 100
        self.set_can_focus(True)
        self.set_has_window(False)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        #
        self.__children = []
  
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
            y=self.allocation.height - 30,
            width=130,
            height=30,
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
            x=self.allocation.width - 30,
            y=0,
            width=30,
            height=100,
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
            width=50,
            height=1000,
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
        # 设置窗口背景. 
        self.style.set_background(self.__bin_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__h_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__v_window, gtk.STATE_NORMAL)
        self.style.set_background(self.__line_num_window, gtk.STATE_NORMAL)
        # 设置子控件的父窗口为bin_window.
        for child in self.__children:
            child.widget.set_parent_window(self.__bin_window)
        #
        self.queue_resize()
        
    # 事件.
    def do_scroll_event(self, e):
        print "do_scroll_event"

    def do_motion_notify_event(self, e):
        if e.window == self.__h_window:
            print "h_wnidow..do_motion_notify_event..", e.x, e.y
            return True
        elif e.window == self.__v_window:
            print "v_window motion....", e.x
        elif e.window == self.__line_num_window:
            print "line num..motion.......", e.x
        else:
            return False

    def do_button_press_event(self, e):
        if e.window == self.__h_window:
            print "button press event..hhh window......"
            return True
        elif e.window == self.__v_window:
            print "do _button pres v_window..."
            return True
        elif e.window == self.__line_num_window:
            print "press line_num_window..."
            return True
        else:
            return False

    def do_button_release_event(self, e):
        if e.window == self.__h_window:
            print "release->h_window:", e.x
            return True
        elif e.window == self.__v_window:
            print "release->v_window:", e.x
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
        gtk.Bin.do_unrealize(self)
  
  
    def do_expose_event(self, event):
        if event.window == self.__line_num_window:
            self.__draw_line_num(event)
        elif event.window == self.__h_window:
            self.__draw_h_scroll_bar(event)
        elif event.window == self.__v_window:
            self.__draw_v_scroll_bar(event)
        else:
            gtk.Container.do_expose_event(self, event)
            return False

    def __draw_line_num(self, event):
        gdk_win = self.get_parent_window()
        g_size = gdk_win.get_size()
        line_size = self.__line_num_window.get_size()
        cr = self.__line_num_window.cairo_create()
        cr.set_source_rgba(0, 0, 1, 0.1)
        cr.rectangle(0, 0, line_size[0], g_size[1])
        cr.fill()
        return True

    def __draw_h_scroll_bar(self, event):
        h_size = self.__h_window.get_size()
        cr = self.__h_window.cairo_create()
        cr.set_source_rgba(1, 0, 0, 0.2)
        cr.rectangle(0, 0, h_size[0], h_size[1])
        cr.stroke()
        return True

    def __draw_v_scroll_bar(self, event):
        v_size = self.__v_window.get_size()
        cr = self.__v_window.cairo_create()
        cr.set_source_rgba(1, 0, 0, 0.2)
        cr.rectangle(0, 0, v_size[0], v_size[1])
        cr.stroke()
        # 画纵向移动块.
        cr.set_source_rgba(0, 0, 1, 0.2)
        cr.rectangle(0, 0 + 30, v_size[0], 150)
        cr.fill()
        return True

    def do_map(self):
        gtk.Bin.do_map(self)
        self.set_flags(gtk.MAPPED)
        self.__line_num_window.show()
        self.__bin_window.show()
        self.__h_window.show()
        self.__v_window.show()

    def do_unmap(self):
        self.__bin_window.hide()
        self.__h_window.hide()
        self.__v_window.hide()
        self.__line_num_window.hide()
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
            # 纵向滚动条.
            v_allocation   = gdk.Rectangle()
            v_size         = self.__v_window.get_size()
            v_allocation.x = b_size[0] - self.__v_window.get_size()[0]
            v_allocation.y = 0
            v_allocation.width  = v_size[0]
            v_allocation.height = b_size[1] - 30
            self.__v_window.move_resize(*v_allocation)
            # 横向滚动条.
            h_allocation   = gdk.Rectangle()
            h_size         = self.__h_window.get_size()
            h_allocation.x = 0
            h_allocation.y = b_size[1] -  self.__h_window.get_size()[1]
            h_allocation.width  = b_size[0] - 30
            h_allocation.height = h_size[1]
            self.__h_window.move_resize(*h_allocation)
            #

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
            widget.set_parent_window(self.__bin_window)
        child.set_parent(self)
 
    def do_forall(self, include_internals, callback, data):
        for child in self.__children:
            callback(child.widget, data)
  
gobject.type_register(CodeEdit) 

class WidgetList:
    def __init__(self):
        self.widget = None
        self.x = 0
        self.y = 0


if __name__ == '__main__':
    window = gtk.Window()
    window.set_size_request(300, 300)
    window.connect('delete-event', gtk.main_quit)
    code_edit = CodeEdit()
    code_edit.put(gtk.Button("test测试呢"), 5, 30)
    code_edit.put(gtk.Button("test测试呢"), 130, 130)
    code_edit.put(gtk.Button("test测试呢"), 120, 110)
    code_edit.put(gtk.Button("test测试呢"), 30, 30)
    code_edit.put(gtk.Button("test测试呢"), 50, 20)
    window.add(code_edit)
    window.show_all()
    gtk.main()



