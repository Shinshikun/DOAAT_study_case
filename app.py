import datetime
import pandas as pd
import json
import plotly
import plotly.express as px 
from flask import Flask, render_template, request, redirect, url_for, session
from api.api import ActualGeneration

app = Flask(__name__)
app.config["SECRET_KEY"] = "blabla"

# L'index permet de rentrer les dates à chercher
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

# On affiche le barplot ici
@app.route("/graph")
def show_prod_per_unit():
    if session.get("start_date") is None or session.get("end_date") is None:
        return redirect(url_for("home"))

    start_date = datetime.datetime.strptime(session.get("start_date") + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(session.get("end_date") + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    api = ActualGeneration()
    data = api.get_mean_hour_by_hour(start_date=start_date, end_date=end_date)
    if data is None:
        return redirect(url_for("home"))

    days = {}
    key: datetime.date
    for key in data:
        idx = key.isoformat()
        if idx not in days:
            days[idx] = {idx : data[key].sum()}
    days=pd.DataFrame(days)
    print(days)

    figure = px.bar(data)
    figure2 = px.bar(days)
    figure.update_layout(
        title="Production par heure",
        xaxis_title="Heures de la journée",
        yaxis_title="Production par heure en MW",
        legend_title="Date"
    )
    figure2.update_layout(
        title="Production par jour",
        xaxis_title="Jour",
        yaxis_title="Production par jour en MW",
        legend_title="Date"
    )

    graph = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    graph2 = json.dumps(figure2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graph.html", graph=graph, graph2=graph2)


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')