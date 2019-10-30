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
outils_db = ["oracle", "mysql","Microsoft SQL Server", "PostgreSQL","DB2","Microsoft Access","SQLite","Teradata", "SAP Adaptative Server", "Hive", "FileMaker"
             ,"SAP HANA", "MariaDB", "Informix", "Firebird", "microsoft azure sql database", "Vertica", "Netezza", "Ingres", "Greenplum", "mongodb","Liquibase"]
outils_ci_cd = ["Buddy", "Semaphore", "GoCD", "Drone.io", "TeamCity", "Wercker", "Codeship", "Travis CI", "CircleCI", "Bamboo","Jenkins"]
outils_collab = ["VersionOne", "Phabricator", "Asana", "Pivotal Tracker", "Basecamp", "Visual Studio", "Trello", "Jira Software", "Mingle"]
outils_version_control = ["Kallithea", "Beanstalk", "GitBucket", "Mercurial", "Gogs", "GitLab", "Bitbucket", "GitHub", "Subversion", "Git"]
outils_test = ["SoapUI","Katalon Studio","ThreatModeler","Checkmarx","RSpec","SpecFlow","Pa11y","Browsersync","Serverspec","pytest","BlazeMeter","Load Impact","Galen Framework",
"TestNG","QUnit","NUnit","FitNesse","Karma","Gatling","OWASP ZAP","Gauntlt","Mocha","Jmeter","Cucumber","JUnit","Jasmine","Selenium"]
outils_bi_log = ["Nagios","Keen IO","Opsgenie","Beats","Moogsoft","PagerDuty","Rollbar","Raygun","Graphite","Grafana","APImetrics","Riemann","Atlas","Runscope","Dynatrace","Sensu","Pinpoint","Prometheus"
,"Vizceral","Sentry","Google Analytics","Grok","Zipkin","Zabbix","Datadog","Kibana","Elasticsearch","Logstash","Airbrake","New Relic","App Dynamics","Vector","Splunk"]
outils_cloud = ["Morpheus","Dokku","Engine Yard","OpenShift","Cloud Foundry","Flynn","Azure","OpenStack","Rackspace","Google Cloud Platform","Heroku","Amazon Web Services"]
app = Flask(__name__)
api = Api(app)  # type: Api

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('x', type=int, default=False, required=False)
parser.add_argument('y', type=int, default=False, required=False)

#indeed.predicted est un fichier traité en amont pour avoir les prédictions, les lables
#qui sont des bornes: prédictions à partir de cela
df = pd.read_csv("../../data/indeed.predicted.csv")
locations = np.unique(df[pd.notnull(df["localisation"])]["localisation"]).tolist()

@app.route("/")
def hello():
    return render_template("index.html")

#dashboard/data
@app.route('/dashboard/data')
def get_dashboard_data():
    result = {}
    result["nombre_annonces"] = len(df)
    result["nombre_annonces"] = len(df)
    return json.dumps(result)

@app.route('/Paris_Vs_Ville/page/<string:tag>')
def paris_vs_ville(tag):
    return render_template("ParisVsVille.html")


@app.route('/Paris_Vs_Ville/data')
def paris_vs_ville_data():
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
    return  get_salaire_moyen_data(langage_de_progs)


@app.route('/salaire_langage_de_prog/popularity')
def salaire_langage_de_prog_popularity():
    return get_popularite_data(langage_de_progs)


@app.route('/salaire_outils/page/<string:tag>')
def salaire_outils(tag):
    return render_template("outils.html")


@app.route('/salaire_outils/db/data')
def salaire_outils_db_data():
    return get_salaire_moyen_data(outils_db)

@app.route('/salaire_outils/db/popularity')
def salaire_outils_db_popularity():
    return get_popularite_data(outils_db)


@app.route('/salaire_outils/ci_cd/data')
def salaire_outils_ci_cd_data():
    return get_salaire_moyen_data(outils_ci_cd)

@app.route('/salaire_outils/ci_cd/popularity')
def salaire_outils_ci_cd_popularity():
    return get_popularite_data(outils_ci_cd)

@app.route('/salaire_outils/collab/data')
def salaire_outils_collab_data():
    return get_salaire_moyen_data(outils_collab)

@app.route('/salaire_outils/collab/popularity')
def salaire_outils_collab_popularity():
    return get_popularite_data(outils_collab)


@app.route('/salaire_outils/version_control/data')
def salaire_outils_version_control_data():
    return get_salaire_moyen_data(outils_version_control)

@app.route('/salaire_outils/version_control/popularity')
def salaire_outils_version_control_popularity():
    return get_popularite_data(outils_version_control)

@app.route('/salaire_outils/test/data')
def salaire_outils_test_data():
    return get_salaire_moyen_data(outils_test)

@app.route('/salaire_outils/test/popularity')
def salaire_outils_test_popularity():
    return get_popularite_data(outils_test)

@app.route('/salaire_outils/bi_log/data')
def salaire_outils_bi_log_data():
    return get_salaire_moyen_data(outils_bi_log)

@app.route('/salaire_outils/bi_log/popularity')
def salaire_outils_bi_log_popularity():
    return get_popularite_data(outils_bi_log)



@app.route('/salaire_outils/cloud/data')
def salaire_outils_cloud_data():
    return get_salaire_moyen_data(outils_cloud)
@app.route('/salaire_outils/cloud/popularity')
def salaire_outils_cloud_popularity():
    return get_popularite_data(outils_cloud)

def get_salaire_moyen_data(list):
    result = {}
    for lg in list:
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

def get_popularite_data(list):
    result = {}
    for lg in list:
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

@app.route('/villes_vs_periph/page/<string:tag>')
def ville_vs_periph(tag):
    return render_template("VillesVsPeriph.html")

@app.route('/villes_vs_periph/data')
def get_ville_vs_periph_data():
    list_depts = {
        "Paris": ["78", "77", "91", "60", "27", "76", "45", "61", "02", "75"],
        "Lyon": ["71", "42", "38", "03", "39", "01", "63", "38", "73", "21", "69"],
        "Toulouse": ["09", "32", "65", "64", "40", "82", "81", "11", "66", "46", "34"],
        "Bordeaux": ["17", "16", "24", "87", "33"],
        "Nantes": ["56", "35", "53", "85", "49", "22", "29", "29", "44"]
    }

    result = {}
    for index, item in enumerate(locations):
        temp = df[df["localisation"] == item]
        for i, item2 in temp.iterrows():
            address = item2["adresse"]

            to_continue = False
            if item == "Toulouse":
                exlude_list = ["Paris", "Marseille", "Lille", "France"]
                for to_exclude in exlude_list:
                    if to_exclude in address:
                        to_continue = True
            if to_continue == True:
                continue

            if item in address:
                address = item
            if item not in result:
                result[item] = {}
            if address not in result[item]:
                result[item][address] = item2["salaire_moyen"]
            else:
                result[item][address] = (result[item][address] + item2["salaire_moyen"]) / 2
    return json.dumps(result)



if __name__ == "__main__":
    app.run(debug=True)