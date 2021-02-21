#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 11:23:44 2021

@author: laurenkirsch
"""
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

external_stylesheets=[dbc.themes.CYBORG]

df = pd.read_csv('syns.txt', sep = '\n', dtype=str)

layout = html.Div([
    html.H3('PubMedIDs:'),
     dcc.Dropdown(
        id='id-dropdown',
        options=[{'label': i, 'value': i} for i in df
    ], multi=True, placeholder='Choose a gene ...'),
    dcc.Link('PubMedIDs', href= 'BRCA2.html')
    ])

@app.callback(
    Output('PubMedIDs', 'children'),
    [Input('id-dropdown', 'value')])
     
def html_up(id_val):
    dcc.Link('PubMedIDs for '+ id_val, href=f"/assets/{id_val}.html")
