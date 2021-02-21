#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Nov  6 11:11:28 2020

@author: laurenkirsch
"""

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.io as pio
pio.templates.default = "plotly_dark"

from app import app

try:
    external_stylesheets = [dbc.themes.CYBORG]

    layout = html.Div([
        html.Br(),
        html.H3('Gene-NE'),
        html.H6('Created by Lauren Kirsch and Dr. Chiquito Crasto'),
        html.Label('Search Box'),
        dcc.Input(id="search_gene",
                  type="text",
                  value='',
                  placeholder="Type a human gene name",
                  debounce=True,
                  minLength=0, maxLength=50,
                  autoComplete='on',
                  size='40'),
        html.Div([
            html.Div([
                dcc.Graph(id='mygraph')])]),
        dcc.RadioItems(
            id="vertical_display_toggle",
            options=[
                {'label': 'Show vertical date bars', 'value': 'show'},
                {'label': 'Hide vertical bars', 'value': 'hide'}],
            value='hide',  # first loading value selected
            labelStyle={'display': 'inline-block'}, inputStyle={"margin-left": "10px", "margin-right": "5px"}),
        dcc.RadioItems(
            id="synonym_display_toggle",
            options=[
                {'label': 'Show synonyms', 'value': 'show'},
                {'label': 'Hide synonyms', 'value': 'hide'},
            ],
            value='hide',  # first loading value selected
            labelStyle={'display': 'inline-block'}, inputStyle={"margin-left": "10px", "margin-right": "5px"}
        ),
        html.Br(),
        html.H6('Texas Tech University Center for Biotechnology and Genomics')
    ])

    df = pd.read_csv('list_out.txt', sep='\t', dtype=str)
    df = df.transpose().reset_index().rename(columns={'index': 'Date'})
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df.iloc[0:600]
    df = df.set_index('Date')
    df = df.iloc[:, ~df.columns.duplicated()]

    @app.callback(
    Output('mygraph', 'figure'),
    [Input('search_gene', 'value'),
     Input('vertical_display_toggle', 'value'),
     Input('synonym_display_toggle', 'value')])

    def update_output(search_gene, vertical_display_user_slct, synonym_display_user_slct):
        df1 = df
        lookup_df = pd.read_csv('Gene_Lookup.csv', dtype=str)
        link = lookup_df.set_index('Approved_Symbol').Linked_Genes.str.split('|').to_dict()
        link_date = lookup_df.set_index('Approved_Symbol').Date_Name_Changed.to_dict()

        if search_gene:
            search_gene = search_gene.upper()
            #search_gene = 'BRCA2'
            syns = link[search_gene]
            file1 = open("syns.txt", "w+")
            with open('syns.txt', 'w') as f:
                f.write(search_gene + '\n')
                for item in syns:
                    f.write("%s\n" % item)
            file1.close()

        trace1 = go.Scatter(x=df1.index, y=df1[search_gene], line_shape='linear', line=dict(color='white'),
                            name=search_gene)

        fig = go.Figure()
        fig.add_trace(trace1)

        if synonym_display_user_slct == "show":
            for i in syns:
                try:
                    fig.add_trace(go.Scatter(x=df.index, y=df1[i], line_shape='linear', name=i))
                except:
                    pass

            fig.update_layout(xaxis_title="Date", yaxis_title="Count")
            genes = link[search_gene]
            genes.append(search_gene)
            df_date = df1[syns]
            date = link_date[search_gene]
            d_max = df_date.applymap(int).values.max()
            graph_max = d_max + 10

            if vertical_display_user_slct == "show":
                fig.add_shape(type="line",
                              x0='2003-4', y0=0, x1='2003-4', y1=graph_max,
                              line=dict(color="lightblue", width=3))
                fig.add_trace(go.Scatter(
                    x=['2003-4'], y=[d_max], name='Genome Publication',
                    mode="markers+text",
                    text=["Date Human Genome Published"], textposition='top left', line=dict(color='lightblue')))
                fig.add_shape(type="line", name='Date Name Changed',
                              x0=date, y0=0, x1=date, y1=graph_max,
                              line=dict(color="blue", width=3))
                fig.add_trace(go.Scatter(
                    x=[date], y=[d_max], name='Symbol Standardiztion',
                    mode="markers+text",
                    text=["Date Gene Name Changed"], textposition='top left', line=dict(color='blue')))
            elif search_gene is None or len(search_gene) == 0:
                gene = 'BRCA2'
                syns = link[gene]

                trace1 = go.Scatter(x=df.index, y=df1[gene], line_shape='linear', line=dict(color='white'), name=gene)

                fig = go.Figure()
                fig.add_trace(trace1)

                if synonym_display_user_slct == "show":
                    for i in syns:
                        try:
                            fig.add_trace(go.Scatter(x=df.index, y=df1[i], line_shape='linear', name=i))
                        except:
                            pass

                fig.update_layout(xaxis_title="Date", yaxis_title="Count")
                genes = link[gene]
                genes.append(gene)
                df_date = df1[syns]
                date = link_date[gene]
                d_max = df_date.applymap(int).values.max()
                graph_max = d_max + 10

                if vertical_display_user_slct == "show":
                    fig.add_shape(type="line",
                                  x0='2003-4', y0=0, x1='2003-4', y1=graph_max,
                                  line=dict(color="lightblue", width=3))
                    fig.add_trace(go.Scatter(
                        x=['2003-4'], y=[d_max], name='Genome Publication',
                        mode="markers+text",
                        text=["Date Human Genome Published"], textposition='top left', line=dict(color='lightblue')))
                    fig.add_shape(type="line", name='Date Name Changed',
                                  x0=date, y0=0, x1=date, y1=graph_max,
                                  line=dict(color="blue", width=3))
                    fig.add_trace(go.Scatter(
                        x=[date], y=[d_max], name='Symbol Standardiztion',
                        mode="markers+text",
                        text=["Date Gene Name Changed"], textposition='top left', line=dict(color='blue')))
            return fig

except:
    pass
