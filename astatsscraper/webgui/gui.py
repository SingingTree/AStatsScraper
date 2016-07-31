from flask import Flask, render_template
import json
from astatsscraper.persistence import Persistor
app =  Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allgames')
def all_games():
    with Persistor() as persistor:
        return render_template('allgames.html',
                               apps_info_json=json.dumps(persistor.get_all_apps_info(order_by="points_per_time")))