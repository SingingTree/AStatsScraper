from flask import Flask, render_template, request
import json
from astatsscraper.persistence import Persistor
app =  Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apps')
def all_games():
    steam_id = request.args.get('steam_id')
    with Persistor() as persistor:
        if steam_id is None:
            apps_info = persistor.get_all_apps_info()
        else:
            apps_info = persistor.get_owned_app_info(steam_id)
        app_info_unicode = [app_info.to_unicode_list() for app_info in apps_info]
        return render_template('apps.html', apps_info_json=json.dumps(app_info_unicode))

if __name__ == '__main__':
    app.run()
