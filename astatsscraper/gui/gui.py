from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.listadapter import ListAdapter
# ListViews are deprecated, but their replacement doesn't seem mature or in the kivy package yet
from kivy.uix.listview import ListView, ListItemLabel, CompositeListItem
from kivy.uix.gridlayout import GridLayout
import astatsscraper.persistence

def app_info_args_converter(row_index, app_info):
    return {
     'text': 'butts?',
     'size_hint_y': None,
     'height': 25,
     'cls_dicts': [{'cls': ListItemLabel,
                    'kwargs': {'text': unicode(app_info[0])}
                    },
                   {'cls': ListItemLabel,
                    'kwargs': {'text': unicode(app_info[1])}
                    },
                   {'cls': ListItemLabel,
                    'kwargs': {'text': unicode(app_info[2])}
                    }]
    }

class AStatsGameTable(GridLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(AStatsGameTable, self).__init__(**kwargs)
        with astatsscraper.persistence.Persistor() as persistor:
            items = persistor.get_all_apps_info()

        dict_adapter = ListAdapter(data=items,
                                   args_converter=app_info_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=CompositeListItem)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)




class AStatsScraperApp(App):
    def build(self):
        return AStatsGameTable()


if __name__ == '__main__':
    AStatsScraperApp().run()
