# call trayicon vtk api.
from dtk.ui.utils import cairo_disable_antialias
from vtk.draw import draw_text
from vtk.utils import get_text_size, cairo_disable_antialias
from vtk.color import color_hex_to_cairo
import gtk

class SelectButton(gtk.Button):        
    def __init__(self, 
                 text="", 
                 bg_color="#ebf4fd",
                 line_color="#7da2ce"):
        gtk.Button.__init__(self)
        # init values.
        self.text = text
        self.bg_color = bg_color
        self.line_color = line_color
        self.draw_check = False
        width, height = get_text_size(self.text)
        print "size", width, height
        self.set_size_request(120, 30)        
        # init events.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("button-press-event", self.select_button_button_press_event)
        self.connect("button-release-event", self.select_button_button_release_event)
        self.connect("expose-event", self.select_button_expose_event)        

    def select_button_button_press_event(self, widget, event):
        widget.grab_add()

    def select_button_button_release_event(self, widget, event):
        widget.grab_remove()
        
    def select_button_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        # 
        if widget.state == gtk.STATE_PRELIGHT:
            print "select_button_expose_event........"
            # draw rectangle.
            with cairo_disable_antialias(cr):
                cr.set_source_rgb(*color_hex_to_cairo(self.bg_color))
                cr.rectangle(rect.x, 
                            rect.y, 
                            rect.width, 
                            rect.height)
                cr.fill()
        
                cr.set_line_width(1)
                cr.set_source_rgb(*color_hex_to_cairo(self.line_color))
                cr.rectangle(rect.x + 1,
                             rect.y + 1, 
                             rect.width - 2,
                             rect.height - 2)
                cr.stroke()              
        # draw text.
        draw_text(cr, self.text,
                  rect.x,
                  rect.y + rect.height/2 - get_text_size(self.text)[1]/2,
                  text_size=8, 
                  text_color="#000000")        
        return True
