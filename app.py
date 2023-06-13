import datetime
import pandas as pd
import json
import plotly
import plotly.express as px 
from flask import Flask, render_template, request, redirect, url_for, session
from api.api import ActualGeneration

app = Flask(__name__)
app.config["SECRET_KEY"] = "blabla"

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        session["start_date"] = start_date
        session["end_date"] = end_date
        return redirect(url_for("show_prod_per_unit"))

    else:
        return render_template("index.html")

@app.route("/graph")
def show_prod_per_unit():
    if session.get(start_date) is None or session.get(end_date) is None:
        return redirect(url_for("home"))
        
    start_date = datetime.datetime.strptime(session.get("start_date") + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(session.get("end_date") + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    api = ActualGeneration()
    data = api.get_mean_hour_by_hour(start_date=start_date, end_date=end_date)
    if data is None:
        return redirect(url_for("home"))

    data = pd.DataFrame(data)
    print(data.head())

    figure = px.bar(data)
    figure.update_layout(
        title="Production",
        xaxis_title="Heures de la journée",
        yaxis_title="Production par heure",
        legend_title="Date"
    )

    graph = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph.html", graph=graph)


if __name__ == '__main__':
    app.run(debug=True)