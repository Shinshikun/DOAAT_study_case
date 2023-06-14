import datetime
import pandas as pd
import json
import plotly
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import join_room, leave_room, send, SocketIO
from api.api import ActualGeneration

app = Flask(__name__)
app.config["SECRET_KEY"] = "blabla"
socketio = SocketIO(app)



def create_graph(data, title, xaxis_title, yaxis_title, legend_title):
    figure = px.bar(data)
    figure.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title
    )  
    graph = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
    return graph

# La route Index permet de rentrer les dates à chercher
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


# La route graph permet d'afficher les barplots
@app.route("/graph")
def show_prod_per_unit():
    if session.get("start_date") is None or session.get("end_date") is None:
        return redirect(url_for("home"))

    start_date = datetime.datetime.strptime(
        session.get("start_date") + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(
        session.get("end_date") + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")

    api = ActualGeneration()
    data = api.get_mean_hour_by_hour(start_date=start_date, end_date=end_date)
    if data is None:
        return redirect(url_for("home"))

    # On va faire la somme jour par jour pour un 2nd graphique
    days = {}
    key: datetime.date
    for key in data:
        idx = key.isoformat()
        if idx not in days:
            days[idx] = {idx: data[key].sum()}
    days = pd.DataFrame(days)

    graph = create_graph(data, title="Production par heure",
        xaxis_title="Heures de la journée",
        yaxis_title="Production par heure en MW",
        legend_title="Date")

    graph2 = create_graph(days, title="Production par jour",
        xaxis_title="Jour",
        yaxis_title="Production par jour en MW",
        legend_title="Date")

    return render_template("graph.html", graph=graph, graph2=graph2, start_date=session.get("start_date"), end_date=session.get("end_date"))

@socketio.on('update_graph')
def update_graph(data):
    print(data)

    start_date = datetime.datetime.strptime(
        data["start_date"] + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(
        data['end_date'] + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")

    api = ActualGeneration()
    data = api.get_mean_hour_by_hour(start_date=start_date, end_date=end_date)
    if data is None:
        return redirect(url_for("home"))

    # On va faire la somme jour par jour pour un 2nd graphique
    days = {}
    key: datetime.date
    for key in data:
        idx = key.isoformat()
        if idx not in days:
            days[idx] = {idx: data[key].sum()}
    days = pd.DataFrame(days)

    graph = create_graph(data, title="Production par heure",
        xaxis_title="Heures de la journée",
        yaxis_title="Production par heure en MW",
        legend_title="Date")

    graph2 = create_graph(days, title="Production par jour",
        xaxis_title="Jour",
        yaxis_title="Production par jour en MW",
        legend_title="Date")

    content = {
        "graph": graph,
        "graph2": graph2
    }
    socketio.emit("update", content)



if __name__ == '__main__':
    socketio.run(app, debug=True, port=3000, host='0.0.0.0')
