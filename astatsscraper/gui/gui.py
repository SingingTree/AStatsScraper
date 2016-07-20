from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import astatsscraper.persistence


class AStatsGameTable(GridLayout):
    def __init__(self, **kwargs):
        super(AStatsGameTable, self).__init__(**kwargs)
        self.cols = 9
        self.col_headers = [
            Label(text='App Id'),
            Label(text='Title'),
            Label(text='Time to 100%'),
            Label(text='Total Points'),
            Label(text='Points Per Time'),
            Label(text='# Players'),
            Label(text='# Player to 100%'),
            Label(text='% of Players to 100%'),
            Label(text='Last Updated'),
        ]

        for label in self.col_headers:
            label.size = label.texture_size
            self.add_widget(label)

        with astatsscraper.persistence.Persistor() as persistor:
            apps_info = persistor.get_all_apps_info()

        for i, app_info in enumerate(apps_info):
            row = []
            try:
                for item in app_info:
                    row.append(Label(text=unicode(item)))
            except UnicodeEncodeError:
                    continue
            # If no error creating row, stick it in the table
            for label in row:
                self.add_widget(label)
            if i > 5:
                break





class AStatsScraperApp(App):
    def build(self):
        return AStatsGameTable()


if __name__ == '__main__':
    AStatsScraperApp().run()
