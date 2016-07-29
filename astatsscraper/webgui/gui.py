from flask import Flask, render_template
import json
from astatsscraper.persistence import Persistor
app =  Flask(__name__)

@app.route('/')
def hello_world():
    with Persistor() as persistor:
        return render_template('GamesByPointsPerTime.html', apps_info_json=json.dumps(persistor.get_all_apps_info(order_by="points_per_time")))
