# call trayicon vtk api.
from dtk.ui.utils import cairo_disable_antialias
from vtk.draw import draw_text
from vtk.utils import get_text_size, cairo_disable_antialias
from vtk.color import color_hex_to_cairo
import gtk

class SelectButton(gtk.Button):        
    def __init__(self, 
                 text="", 
                 ali_padding=5,
                 font_size=8,
                 bg_color="#ebf4fd",
                 line_color="#7da2ce"):
        gtk.Button.__init__(self)
        # init values.
        self.text = text
        self.font_size=font_size 
        self.ali_padding = ali_padding
        self.bg_color = bg_color
        self.line_color = line_color
        self.draw_check = False
        width, height = get_text_size(self.text, font_size)
        self.set_size_request(width, height)
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
        # get font width/height.
        font_w, font_h = get_text_size(self.text, text_size=self.font_size)
        # draw text.
        draw_text(cr, self.text,
                  rect.x + self.ali_padding,
                  rect.y + rect.height/2 - font_h/2,
                  text_size=self.font_size, 
                  text_color="#000000")        
        # set size.
        if font_h > rect.height:
            widget.set_size_request(rect.width, font_h)
        return True
