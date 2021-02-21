#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Nov  6 11:11:28 2020

@author: laurenkirsch
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from app import server

from apps import links, graph

#external_stylesheets = [dbc.themes.CYBORG]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    html.Div([
        dcc.Link('Graph | ', href='/apps/graph'),
        dcc.Link('PubMedIDs', href='/apps/links'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])



@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/graph':
        return links.layout
    elif pathname == '/apps/links':
        return graph.layout
    else:
        return graph.layout

if __name__ == '__main__':
    app.run_server(debug=True)
