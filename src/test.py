import gtk
from vtk.window import TrayIconWin

def test_win_press(widget, event):
    screen = widget.get_screen()
    test.set_screen(screen)
    test.move(100, 100)
    test.show_all()
    
def test_win_motion(widget, event):
    print "fjdsklfjdklf"
    
test = TrayIconWin()
win = gtk.Window(gtk.WINDOW_TOPLEVEL)
btn = gtk.Button("fjdsklfjsdklfjk")
win.add(btn)
btn.add_events(gtk.gdk.ALL_EVENTS_MASK)
btn.connect("button-press-event", test_win_press)
btn.connect("motion-notify-event", test_win_motion)
win.show_all()
gtk.main()

