# -*- coding: utf-8 -*-
import pygal
import pygal.maps.fr
import random
from random import *

import numpy as np
import pandas as pd
import json
import statistics
import pymongo
from pymongo import MongoClient
from pandas.io.json import json_normalize

#datapoints = list(db.collection_name.find({})

#nba = json_normalize(datapoints)
from flask import Flask,render_template,Response
from flask_restful import Resource, Api, reqparse
import sys
sys.path.append('../scrapping')


langage_de_progs = ["JavaScript","Java","Python","PHP","C#","C++","CSS","Ruby","C","Objective-C","Swift","TypeScript","Scala","Shell","Go","R","PowerShell","Perl","Haskell","Kotlin", "Dart",
"Haskell", "Ocaml","Lua", "F#","Scala","D","Swift","Erlang", "Julia"]

app = Flask(__name__)
api = Api(app)  # type: Api

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('x', type=int, default=False, required=False)
parser.add_argument('y', type=int, default=False, required=False)

df = pd.read_csv("../../data/indeed.predicted.csv")
class Multiply(Resource):
    def get(self, x):
        result = x * x
        return {'result': result}

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/Paris_Vs_Ville/page/<string:tag>')
def paris_vs_ville(tag):
    return render_template("ParisVsVille.html")


@app.route('/Paris_Vs_Ville/data')
def paris_vs_ville_data():
    locations = np.unique(df[pd.notnull(df["localisation"])]["localisation"]).tolist()
    result = {}
    for item in locations:
        temp = df[df["localisation"] == item]
        result[item] = {"min": statistics.mean(temp["salaire_min"]),
                        "moyen": statistics.mean(temp["salaire_moyen"]),
                        "max": statistics.mean(temp["salaire_max"])
                        }
    return json.dumps(result)


#langage_de_prog.html
@app.route('/salaire_langage_de_prog/page/<string:tag>')
def salaire_langage_de_prog(tag):
    return render_template("langage_de_prog.html")

@app.route('/salaire_langage_de_prog/data')
def salaire_langage_de_prog_data():
    locations = np.unique(df[pd.notnull(df["localisation"])]["localisation"]).tolist()
    result = {}
    for lg in langage_de_progs:
        lg = lg.lower()
        if lg not in df.columns:
            continue
        for index, item in enumerate(df[lg]):
            if item == 1:
                key = lg + "_toutes"
                if key not in result:
                    result[key] = df['salaire_moyen'][index]
                else:
                    result[key] = (result[key] + df['salaire_moyen'][index]) / 2
                for loc in locations:
                    if df["localisation"][index] == loc:
                        key_ = lg + "_" + loc
                        if key_ not in result:
                            result[key_] = df['salaire_moyen'][index]
                        else:
                            result[key_] = (result[key_] + df['salaire_moyen'][index]) / 2

    return json.dumps(result)


@app.route('/salaire_langage_de_prog/popularity')
def salaire_langage_de_prog_popularity():
    locations = np.unique(df[pd.notnull(df["localisation"])]["localisation"]).tolist()
    result = {}
    for lg in langage_de_progs:
        lg = lg.lower()
        if lg not in df.columns:
            continue
        for index, item in enumerate(df[lg]):
            if item == 1:
                key = lg + "_toutes"
                if key not in result:
                    result[key] = 1
                else:
                    result[key] = result[key] + 1
                for loc in locations:
                    if df["localisation"][index] == loc:
                        key_ = lg + "_" + loc
                        if key_ not in result:
                            result[key_] = 1
                        else:
                            result[key_] = result[key_] + 1
    return json.dumps(result)


@app.route('/salaire_outils/page/<string:tag>')
def salaire_outils(tag):
    return render_template("outils.html")


api.add_resource(Multiply, '/multiply/<int:x>')
#api.add_resource(Info, '/info/')

if __name__ == "__main__":
    app.run(debug=True)