from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class AStatsGameTable(GridLayout):
    def __init__(self, **kwargs):
        super(AStatsGameTable, self).__init__(**kwargs)
        self.cols = 9
        self.col_headers = [
            Label(text="App Id"),
            Label(text="Title"),
            Label(text="Time to 100%"),
            Label(text="Total Points"),
            Label(text="Points Per Time"),
            Label(text="# Players"),
            Label(text="# Player to 100%"),
            Label(text="% of Players to 100%"),
            Label(text="Last Updated"),
        ]

        for label in self.col_headers:
            label.size = label.texture_size
            self.add_widget(label)


class AStatsScraperApp(App):
    def build(self):
        return AStatsGameTable()


if __name__ == '__main__':
    AStatsScraperApp().run()
