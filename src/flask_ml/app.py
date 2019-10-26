# -*- coding: utf-8 -*-
import pygal
import pygal.maps.fr
import random
from random import *

import numpy as np
import pandas as pd
import json

import pymongo
from pymongo import MongoClient
from pandas.io.json import json_normalize

#datapoints = list(db.collection_name.find({})

#nba = json_normalize(datapoints)
from flask import Flask,render_template,Response
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)  # type: Api

"""
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nba_DB"]
mycol = mydb["nba_collection"]
#x = mycol.find_one()
#print(x)
datapoints = list(mycol.find({}))

nba = json_normalize(datapoints)
#print(nba.head())
#nba = pd.read_json('/Users/arnaudbaleh/Desktop/DATA_IA_Simplon/flask_ml_gr3/nba_machine_learning.json', lines=True)
#nba = pd.read_csv('nba_salary.csv')
# Make a query to the specific DB and Collection
#cursor = mycol.find(query)
# Expand the cursor and construct the DataFrame
#nba =  pd.DataFrame(list(cursor))
def raccourcir(liste1,liste2,t = 25):
    list_short = []
    list_short2 = []
    i = 0
    n = 0
    taille = len(liste1) - 1
    while i < t:
        n = randint(1, taille)
        list_short.append(liste1[n])
        list_short2.append(liste2[n])
        i += 1
    return list_short, list_short2

salaire_list = nba.groupby('Player').Salary.sum()
#liste salaires nba
salaire_list_short = salaire_list.tolist()
salaire_list_short = [int(i) for i in salaire_list_short]
#salaire = raccourcir(salaire_list_short,30)

age_list = nba.groupby('Player').Age.sum()
age_list_short = age_list.tolist()
salaire, age = raccourcir(salaire_list_short, age_list_short,30)

player_list = nba.groupby('Age').Player.sum()
player_list_short = player_list.tolist()
players, salaire = raccourcir(player_list_short, salaire_list_short,30)

#[int(i) for i in age_list]
#map(int, results)
"""


# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('x', type=int, default=False, required=False)
parser.add_argument('y', type=int, default=False, required=False)

class Multiply(Resource):
    def get(self, x):
        result = x * x
        return {'result': result}

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/Paris_Vs_Ville/')
def dashboard():
    return render_template("ParisVsVille.html")

#Les graphes de base affichés en iframe
@app.route('/dashboard/menu_graph_bar/')
def menu_graph_bar():
    line_chart = pygal.Bar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.render()
    return Response(response=line_chart.render())

@app.route('/dashboard/menu_graph_scatter/')
def menu_graph_scatter():
    """ render svg graph """
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = 'Correlation'
    xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
    xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
    xy_chart.add('C',
                 [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23),
                  (2.3, 1.98)])
    xy_chart.render()
    return Response(response=xy_chart.render())

@app.route('/dashboard/menu_graph_stacked/')
def menu_graph_StackedBar():
    """ render svg graph """
    line_chart = pygal.StackedBar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.render()
    return Response(response=line_chart.render())

@app.route('/dashboard/menu_graph_pie/')
def menu_graph_pie():
    """ render svg graph """
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage by version in February 2012 (in %)'
    pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
    pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
    pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    pie_chart.add('Safari', [4.4, .1])
    pie_chart.add('Opera', [.1, 1.6, .1, .5])
    pie_chart.render()
    return Response(response=pie_chart.render())

@app.route('/dashboard/menu_graph_ring/')
def menu_graph_ring():
    """ render svg graph """
    pie_chart = pygal.Pie(inner_radius=.75)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render()
    return Response(response=pie_chart.render())

@app.route('/dashboard/menu_graph_radar/')
def menu_graph_radar():
    radar_chart = pygal.Radar()
    radar_chart.title = 'V8 benchmark results'
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                            'NavierStokes']
    radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    radar_chart.render()
    return Response(response=radar_chart.render())

@app.route('/dashboard/menu_graph_box/')
def menu_graph_box():
    box_plot = pygal.Box()
    box_plot.title = 'V8 benchmark results'
    box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    box_plot.render()
    return Response(response=box_plot.render())

@app.route('/dashboard/menu_graph_dot/')
def menu_graph_dot():
    dot_chart = pygal.Dot(x_label_rotation=30)
    dot_chart.title = 'V8 benchmark results'
    dot_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                          'NavierStokes']
    dot_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    dot_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    dot_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    dot_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
    dot_chart.render()
    return Response(response=dot_chart.render())

@app.route('/dashboard/menu_graph_gauge/')
def menu_graph_gauge():
    gauge = pygal.SolidGauge(inner_radius=0.70)
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter

    gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
              formatter=dollar_formatter)
    gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
    gauge.add('Series 3', [{'value': 3}])
    gauge.add(
        'Series 4', [
            {'value': 51, 'max_value': 100},
            {'value': 12, 'max_value': 100}])
    gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
    gauge.add('Series 6', 99)
    gauge.add('Series 7', [{'value': 100, 'max_value': 100}])
    gauge.render()
    return Response(response=gauge.render())

@app.route('/dashboard/menu_graph_line/')
def menu_graph_line():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.render()
    return Response(response=line_chart.render())

@app.route('/dashboard/menu_graph_treemap/')
def menu_graph_treemap():
    treemap = pygal.Treemap()
    treemap.title = 'Binary TreeMap'
    treemap.add('A', [2, 1, 12, 4, 2, 1, 1, 3, 12, 3, 4, None, 9])
    treemap.add('B', [4, 2, 5, 10, 3, 4, 2, 7, 4, -10, None, 8, 3, 1])
    treemap.add('C', [3, 8, 3, 3, 5, 3, 3, 5, 4, 12])
    treemap.add('D', [23, 18])
    treemap.add('E', [1, 2, 1, 2, 3, 3, 1, 2, 3,
                      4, 3, 1, 2, 1, 1, 1, 1, 1])
    treemap.add('F', [31])
    treemap.add('G', [5, 9.3, 8.1, 12, 4, 3, 2])
    treemap.add('H', [12, 3, 3])
    treemap.render()
    return Response(response=treemap.render())

@app.route('/dashboard/menu_graph_map/')
def menu_graph_map():
    fr_chart = pygal.maps.fr.Departments()
    fr_chart.title = 'Some departments'
    fr_chart.add('Métropole', ['69', '92', '13'])
    fr_chart.add('Corse', ['2A', '2B'])
    fr_chart.add('DOM COM', ['971', '972', '973', '974'])
    fr_chart.render()
    return Response(response=fr_chart.render())
#******************************************************************************************************************

#******************************************************

#******************************************************

#Les graphes du dataset affichés en iframe
@app.route('/dashboard/graph_bar/', methods = ["POST"])
def graph_bar():

    if request.method == 'POST':
        salaire_form = request.form['salaire']
        age_form = request.form['age']

        #salaire = flask(salaire_form )
        #age = flask(age_form )
    if salaire_form:
        if age_form:
            line_chart = pygal.Bar()
            line_chart.title = 'Salaire nba en fonction de l\'âge'
            line_chart.x_labels = age
            line_chart.add('Salaire', salaire)
            chart = line_chart.render_data_uri()
            return render_template("rendu.html",chart=chart)


@app.route('/dashboard/graph_scatter/')
def graph_scatter():
    """ render svg graph """
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = 'Correlation'
    xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
    xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
    xy_chart.add('C',
                 [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23),
                  (2.3, 1.98)])
    chart = xy_chart.render_data_uri()
    return render_template("rendu.html",chart=chart)

@app.route('/dashboard/graph_stacked/')
def graph_StackedBar():
    """ render svg graph """
    line_chart = pygal.StackedBar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.render()
    chart = line_chart.render_data_uri()
    return render_template("rendu.html",chart=chart)

@app.route('/dashboard/graph_pie/')
def graph_pie():
    """ render svg graph """
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage by version in February 2012 (in %)'
    pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
    pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
    pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    pie_chart.add('Safari', [4.4, .1])
    pie_chart.add('Opera', [.1, 1.6, .1, .5])

    chart = pie_chart.render_data_uri()
    return render_template("rendu.html",chart=chart)

@app.route('/dashboard/graph_ring/')
def graph_ring():
    """ render svg graph """
    pie_chart = pygal.Pie(inner_radius=.75)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)

    chart = pie_chart.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_radar/')
def graph_radar():
    radar_chart = pygal.Radar()
    radar_chart.title = 'V8 benchmark results'
    radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                            'NavierStokes']
    radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

    chart = radar_chart.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_box/')
def graph_box():
    box_plot = pygal.Box()
    box_plot.title = 'V8 benchmark results'
    box_plot.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    box_plot.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    box_plot.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    box_plot.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

    chart =  box_plot.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_dot/')
def graph_dot():
    dot_chart = pygal.Dot(x_label_rotation=30)
    dot_chart.title = 'V8 benchmark results'
    dot_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay',
                          'NavierStokes']
    dot_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
    dot_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
    dot_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
    dot_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])

    chart = dot_chart.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_gauge/')
def graph_gauge():
    gauge = pygal.SolidGauge(inner_radius=0.70)
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter

    gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
              formatter=dollar_formatter)
    gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
    gauge.add('Series 3', [{'value': 3}])
    gauge.add(
        'Series 4', [
            {'value': 51, 'max_value': 100},
            {'value': 12, 'max_value': 100}])
    gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
    gauge.add('Series 6', 99)
    gauge.add('Series 7', [{'value': 100, 'max_value': 100}])

    chart = gauge.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_line/')
def graph_line():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])

    chart = line_chart.render_data_uri()
    return render_template("rendu.html", chart=chart)


@app.route('/dashboard/graph_treemap/')
def graph_treemap():
    treemap = pygal.Treemap()
    treemap.title = 'Binary TreeMap'
    treemap.add('A', [2, 1, 12, 4, 2, 1, 1, 3, 12, 3, 4, None, 9])
    treemap.add('B', [4, 2, 5, 10, 3, 4, 2, 7, 4, -10, None, 8, 3, 1])
    treemap.add('C', [3, 8, 3, 3, 5, 3, 3, 5, 4, 12])
    treemap.add('D', [23, 18])
    treemap.add('E', [1, 2, 1, 2, 3, 3, 1, 2, 3,
                      4, 3, 1, 2, 1, 1, 1, 1, 1])
    treemap.add('F', [31])
    treemap.add('G', [5, 9.3, 8.1, 12, 4, 3, 2])
    treemap.add('H', [12, 3, 3])

    chart = treemap.render_data_uri()
    return render_template("rendu.html", chart=chart)

@app.route('/dashboard/graph_map/')
def graph_map():
    fr_chart = pygal.maps.fr.Departments()
    fr_chart.title = 'Some departments'
    fr_chart.add('Métropole', ['69', '92', '13'])
    fr_chart.add('Corse', ['2A', '2B'])
    fr_chart.add('DOM COM', ['971', '972', '973', '974'])

    chart = fr_chart.render_data_uri()
    return render_template("rendu.html", chart=chart)
#*****************************

api.add_resource(Multiply, '/multiply/<int:x>')
#api.add_resource(Info, '/info/')

if __name__ == "__main__":
    app.run(debug=True)