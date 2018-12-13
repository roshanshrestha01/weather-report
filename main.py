import gi
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from settings import WEATHER_BASE_API, API_KEY


class WeatherForecastWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Weather forecast")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.CITY_NAME = None  # for refresh action
        self.add_to_main(self.setup_city_name_box, 'city_name_gui')

    def setup_city_name_box(self):
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        city_name = Gtk.Label("City name", xalign=0)
        self.city_name = Gtk.Entry()
        self.city_name.set_size_request(400, 20)
        # self.city_name.set_text("Kathmandu")
        self.city_name.set_width_chars(40)

        vbox.pack_start(city_name, False, False, 0)
        vbox.pack_start(self.city_name, False, False, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.check_weather = Gtk.Button.new_with_label("Check weather")
        self.check_weather.connect("clicked", self.get_weather_forecast)
        self.check_weather.set_size_request(200, 20)

        self.update = Gtk.Button.new_with_label("Refresh")
        self.update.set_size_request(200, 20)
        hbox.pack_end(self.check_weather, False, False, 0)
        # hbox.pack_start(self.update, False, False, 0)

        listbox.add(row)
        return box_outer

    def add_to_main(self, box, key):
        box = box()
        setattr(self, key, box)
        self.add(getattr(self, key))

    def remove_from_main(self, key):
        self.remove(getattr(self, key))

    def get_weather_forecast(self, button):
        city_name = self.city_name.get_text()
        if not city_name:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Please enter a city name.")
            dialog.format_secondary_text(
                "You have place empty city name.")
            dialog.run()
            print("INFO dialog closed")

            dialog.destroy()
            return
        self.remove_from_main('city_name_gui')
        self.CITY_NAME = city_name

        url = WEATHER_BASE_API + city_name + '&appid=' + API_KEY
        response = requests.get(url)

        print(response.json())
        print('Getting weather report from google for %s' % self.city_name.get_text())


win = WeatherForecastWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
