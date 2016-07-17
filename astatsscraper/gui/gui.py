from kivy.app import App
from kivy.uix.widget import Widget


class AStatsScraperGui(Widget):
    pass


class AStatsScraperApp(App):
    def build(self):
        return AStatsScraperGui()


if __name__ == '__main__':
    AStatsScraperApp().run()