import gi 
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

builder = Gtk.builder()

builder.add_from_file('Dashboard.glade')

class Handler(object):

        def __init__(self, **kwargs):
            super(Handler, self).__init__ (**kwargs)

        self.lable-texto = builder.get_object('lable-texto')
        self.lable-texto.set_text('teste')

        def on_principal_destroy(self, window):
              Gtk.main_quit()

builder.connect_signals(Handler())
window = builder.get_object('principal')
window.show_all()

if __name__ == '__main__':
      Gtk.main()