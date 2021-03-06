# -*- coding: utf-8 -*-
"""Df_to_dash.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pZ4y_N-S8CLDrK2qdr8sMmmqzts9toUA
"""


import pandas as pd

import random

from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc

#from spacy.training.example import Example
import re
import requests
import PyPDF2
import fitz
import re

nlp2 = spacy.load("en_relation_def_extraction")
nlp_it = spacy.load('it_core_news_lg')


def clean_jud(text):
    text = text.lower()
    text = text.replace("'"," ")
    #text = text[text.find(' 1.')+3: text.find(' 1.') + 800]
    text = re.sub('art. \d', '',text)
    text = re.sub('artt. \d', '',text)
    text = re.sub("d.p.r. \d", '',text)
    text = re.sub("n. \d", '',text)
    text = re.sub("n. dep \d", '',text)
    text = re.sub('ex \d','',text)
    text = re.sub('comma \d', '',text)

    
    text = text.replace('n.','')
    text = text.replace('cost.','')
    text = text.replace('sent.', '')
    text = text.replace('num.', '')
    text = text.replace('sez.', '')
    text = text.replace('p. e p.', '')
    text = text.replace("d.lgs.", '')
    text = text.replace("cod. pen.", '')
    text = text.replace("cod.proc.pe", '')
    text = text.replace('m.a.e', '')
    text = text.replace('lett.', '')
    
    

    
    text = re.sub(' +', ' ',text)
    return text

def download_file(download_url,name):
    response = requests.get(download_url)
    
    with open(f'{name}', 'wb') as f:
        f.write(response.content)
    f.close()


def pdf2str(pdf_link):
    download_file(pdf_link,'sentenza.pdf')
    pdfFileObj = open('sentenza.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    text = ''
    for p in range(pdfReader.numPages):
        text +=  pdfReader.getPage(p).extractText()
    
    return text

def get_imputati(pdf_link, top_k=3):
    text = pdf2str(pdf_link)
    text = clean_jud(text)

    sentenza = nlp2(nlp_it(text))
    imputati = []
    for value, rel_dict in sentenza._.rel.items():
        for s in sentenza.sents:
            for e in s.ents:
                for b in s.ents:
                    if e.start == value[0] and b.start == value[1]:
                        if rel_dict['DIFENDE'] > rel_dict['GIUDICA']:
                            imputati.append((b.text[0].upper()+'*****'+b.text[-1], rel_dict['DIFENDE'],b.text))   
                        
                        
                        else:
                            imputati.append((b.text[0].upper() + '*****' + b.text[-1],  rel_dict['GIUDICA'],b.text))

    imputati.sort(key= lambda x: x[1],reverse=True)
    imp_name = set()
    new_imputati = []
    for t in imputati:
        if t[0] not in imp_name:
            new_imputati.append(t)
            imp_name.add(t[0])
    top_k = int(top_k)
    if top_k > len(new_imputati):
        top_k = len(new_imputati)
        
    return pd.DataFrame(new_imputati[:top_k], columns =['defendants','probs', 'completename'])

class Redactor:
    # constructor
    def __init__(self, path, defendant):
        self.path = path
        self.defendant = defendant
 
    def get_sensitive_data(self, lines):
       
        """ Function to get all the lines """
         
       
        for line in lines:
           for name in self.defendant.split():
                # matching the regex to each line
                if name in line:
                    # yields creates a generator
                    # generator is used to return
                    # values in between function iterations
                    yield self.defendant
                elif name.upper() in line:
                    yield self.defendant.upper()
                elif name.capitalize() in line:
                    yield self.defendant.capitalize()


    def redaction(self):
       
        """ main redactor code """
         
        # opening the pdf
        doc = fitz.open(self.path)
         
        # iterating through pages
        for page in doc:
           
            # _wrapContents is needed for fixing
            # alignment issues with rect boxes in some
            # cases where there is alignment issue
            #page._wrapContents()
             
            # getting the rect boxes which consists the matching email regex
            sensitive = self.get_sensitive_data(page.get_text("text")
                                                .split('\n'))
            for data in sensitive:
                areas = page.search_for(data)
                 
                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]
                 
            # applying the redaction
            page.apply_redactions()
             
        # saving it to a new pdf
        doc.save('/content/redacted.pdf')
        
 



import dash                              # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas

from jupyter_dash import JupyterDash
JupyterDash.infer_jupyter_proxy_config()






# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = JupyterDash()


# Define Layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H1("Extracts the probable defendants with a relation extraction model"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    width=5,
                    children=[
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                	dbc.Input(id="input_link", placeholder="inserisci il link", type="text"),
                			html.Br(),
                			html.P(id="output1"),
                        		]
                        		
                        		)   
                            ]),
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                	dbc.Input(id="input_num", placeholder="inserisci il numero di imputati", type="text"),
                			html.Br(),
                			html.P(id="output2"),
                        		]
                        		)
                            ]),
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                                ])
                            ]),
                        ], width=4),
                        dbc.Card(
                            body=True,
                            children=[
                                        dbc.Label("Summarized Content"),
                                        dcc.Textarea(
                                            id="anonymized",
                                            style={
                                                "width": "100%",
                                                "height": "calc(75vh - 275px)",
                                            },
                                        ),
                                    ]
                                )
                            
                       
                            
                        
                        
                  
                
                        ],
                ),
                
                

    ],
)
]
)








# Bar Chart ************************************************************
@app.callback(
    [Output('anonymized', 'value'), Output('bar-chart','figure')],
    [
       Input('input_link','value'),
    Input('input_num','value'),
    ],
    
)
def update_out( link,k=3):
    # Bar Chart
    df = get_imputati(link,k)
    
    fig_bar = px.bar(df, x='probs', y='defendants', template='ggplot2',
                      orientation='h', title= "Defendants of submitted judgements")
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_bar.update_traces(marker_color='blue')
    
    # text output
    text = pdf2str(link)
    text = clean_jud(text)
    imp = df.iloc[0]['completename']
    
    text = text[: text.find(imp) + 200]
    text = text.replace(imp, imp[0].upper() + '********' + imp[-1])
    
    
    
    redactor = Redactor('sentenza.pdf', imp)
    redactor.redaction()

    return text, fig_bar





if __name__=='__main__':
    app.run_server(debug=False)

                     
    
