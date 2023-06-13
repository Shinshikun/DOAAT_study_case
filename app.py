from flask import Flask, render_template
import datetime
import pandas as pd
import json
import plotly
import plotly.express as px 
from api.api import ActualGeneration

app = Flask(__name__)

@app.route('/')
def show_prod_per_unit():
    start = datetime.datetime(2022, 12, 1, 0, 0)
    end = datetime.datetime(2022, 12, 3, 0, 0)

    api = ActualGeneration()
    data = pd.DataFrame(api.get_mean_hour_by_hour(start_date=start, end_date=end))

    figure = px.bar(data)

    graph = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graph)


if __name__ == '__main__':
    app.run(debug=True)