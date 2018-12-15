from datetime import datetime

import gi
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from settings import WEATHER_BASE_API, WEATHER_SINGLE_BASE_API


class WeatherReportWindow(Gtk.Window):
    def __init__(self, parent, weather_data, city_name):
        Gtk.Window.__init__(self, title="Weather Report")
        self.parent = parent
        self.weather_data = weather_data
        self.city_name = city_name
        self.data = self.parse_data(weather_data)
        print(self.data)
        self.connect("destroy", self.on_destroy)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_size_request(800, 600)
        self.add(Gtk.Label("This is another window"))
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

        refresh = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        refresh.connect("clicked", self.refresh)
        refresh.add(image)
        hb.pack_end(refresh)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        go_back = Gtk.Button()
        go_back.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        go_back.connect("clicked", self.go_back)
        box.add(go_back)
        hb.pack_start(box)
        self.add(Gtk.TextView())
        self.show_all()

    def parse_data(self, weather_data):
        city_name = weather_data.get('city').get('name')
        url = WEATHER_SINGLE_BASE_API + city_name
        response = requests.get(url)
        data = response.json()
        country = weather_data.get('city').get('country')
        timestamp = data.get('dt')

        report = dict(
            city_name=city_name,
            country=country,
            timestamp=timestamp,
            dt_text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            temp=data.get('main').get('temp'),
            pressure=data.get('main').get('pressure'),
            humidity=data.get('main').get('humidity'),
            wind_speed=data.get('wind').get('speed'),
            wind_deg=data.get('wind').get('deg'),
        )
        forecast = []
        for data in weather_data.get('list'):
            forecast.append(dict(
                timestamp=data.get('dt'),
                dt_text=data.get('dt_txt'),
                temp=data.get('main').get('temp'),
                pressure=data.get('main').get('pressure'),
                humidity=data.get('main').get('humidity'),
                wind_speed=data.get('wind').get('speed'),
                wind_deg=data.get('wind').get('deg'),
            ))
        report['forecast'] = forecast
        return report

    def go_back(self, widget):
        self.parent.show_all()
        self.hide()

    def refresh(self, widget):
        pass

    def on_destroy(self, widget):
        widget.hide()


class WeatherForecastWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Weather forecast")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.CITY_NAME = None  # for refresh action
        self.city_name_gui = self.setup_city_name_box()
        self.add(self.city_name_gui)

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
        self.city_name.set_text("Kathmandu")
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

        listbox.add(row)
        return box_outer

    def get_weather_forecast(self, button):
        city_name = self.city_name.get_text()
        self.check_weather.set_label("Fetching data..")
        print(city_name)
        if not city_name:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Please enter a city name.")
            dialog.format_secondary_text(
                "You have not entered any city name.")
            dialog.run()
            dialog.destroy()
            return
        url = WEATHER_BASE_API + city_name
        response = requests.get(url)
        print(url)
        data = response.json()
        self.check_weather.set_label("Check weather")
        self.hide()
        ano = WeatherReportWindow(self, data, city_name)


win = WeatherForecastWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
