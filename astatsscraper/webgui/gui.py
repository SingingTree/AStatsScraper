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
        if steam_id == None:
            app_info = persistor.get_all_apps_info()
        else:
            app_info = persistor.get_owned_app_info(steam_id)
        return render_template('apps.html', apps_info_json=json.dumps(app_info))