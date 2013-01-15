#!coding:utf-8


import gtk
import struct
from Xlib import display


class WinStruct(object):
    def __init__(self):
        self.plug = None       # /*gtk.Plug*/
        self.image_icon = None # /*gtk.Image*/
        self.tray_icon = None  # /*pixbuf*/
        self.plug_xlib = None  # /*plug get_id*/
        self.root_gdk = None
        self.manager_window = None # /**/
        self.manager_window_gdk = None

def NEW_GET_DISPLAY():
    xdisplay = display.Display()
    return xdisplay

class NewTrayIcon(object):
    def __init__(self):
        self.selection_atom = None # Atom
        self.system_tray_opcode_atom = None # Atom
        win_struct = WinStruct()
        #
        self.get_manager_window()
        # selection_atom = XInternAtom(

    def tray_done(self, win):
        win.root_gdk.remove_filter(manager_filter, win)
        win.manager_window_gdk.remove_filter(manager_filter)

        if win.plug:
            win.plug.destroy()

    def get_manager_window(self):
        manager_window = None
        gtk.gdk.error_trap_push()
        xdisplay = NEW_GET_DISPLAY()
        xdisplay.grab_server()
        #xdisplay.get_selection_owner(selection_atom)
        xdisplay.ungrab_server()
        xdisplay.flush()
        if gtk.gdk.error_trap_pop():
            return False
        #
        return manager_window

    def create_tray_and_dock(self, win):
        # 
        if win.manager_window == None:
            win.manager_window = self.get_manager_window()
        if win.manager_window == None:
            return None;
        win.manager_window_gdk = None
        win.manager_window_gdk = 
        win.manager_window_gdk.set_events
        win.manager_window_gdk.add_filter(manager_filter, win)
        if (win.plug):
            win.plug.destroy()
        # init widgets.
        win.plug = gtk.Plug(0)
        win.image_icon = gtk.Image()
        win.plug.add(win.image_icon)
        win.image_icon.show()
        win.plug.show()
        win.plug.realize()
        win.plug_xlib = win.plug.get_id()

        win.plug.add_events(gtk.gdk.ALL_EVENTS_MASK)
        #
        '''win.plug.connect("motion-notify-event",
        win.plug.connect("button-press-event",
        win.plug.connect("configure-event",
        '''
        # 
        self.dock_window(win.manager_window, win.plug_xlib)

    def update_tray_icon(self, win):
        '''更新图标'''
        temp = None
        req_h, req_w = 0, 0
        gtk.gdk.error_trap_push()
        if gtk.gdk.error_trap_pop():
            return False;
        
    def dock_window(self, manager_window, window):
        # XClientMessageEvent ev;
        ev.type = ClientMessage
        ev.window = manager_window
        ev.message_type = system_tray_opcode_atom
        ev.format = 32
        # 需要使用struct转换. 
        ev.data.l[0] = CurrentTime
        ev.data.l[1] = SYSTEM_TRAY_REQUEST_DOCK
        ev.data.l[2] = window;
        ev.data.l[3] = 0
        ev.data.l[4] = 0
        #
        gtk.gdk.error_trap_push()
        # 发送给dock event.
        xdisplay = NEW_GET_DISPLAY()
        xdisplay.send_event(manager_window, False, NoEventMask, ev)
        xdisplay.sync()
        gtk.gdk.error_trap_pop()

    def tray_init(self, win):
        win.manager_window = get_manager_window()

        win.root_gdk.add_filter(self.manager_filter, win)

    def manager_filter(self, xevent, event, win):
        xdisplay = NEW_GET_DISPLAY()
        #xdisplay. XGetWindowAttributes

        if (xev.xany.type == ClientMessage
            and xev.xclient.message_type == manager_atom
            and xev.xclient.data.l[1] == selection_atom):
            if :
                self.create_tray_and_dock(win)
        elif xev.xany.window == win.manager_window:
            if xev.xany.type == DestroyNotify:
                if ....print..
                gtk.gdk.error_trap_push()
                # xGetWindowAttributes
        if gtk.gdk.error_trap_push():
            win.manager_window_gdk.remove_filter(manager_filter)

            if win.plug:
                win.plug.destroy()
            win.plug = None

if __name__ == "__main__":
    NewTrayIcon()
    gtk.main()
