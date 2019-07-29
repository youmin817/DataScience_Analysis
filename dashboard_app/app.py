import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from math_ans import *


df_sd = pd.read_excel("Prestige_ACT_TEST_REPORT.xlsm", sheet_name = "Sheet1")
df_sd = df_sd.loc[:,["Name","English", "Math", "Reading", "Science", "Composite Score"]]
abc = df_sd.drop("Name", axis=1).T
abc.columns = df_sd["Name"]

# subejct
columns = df_sd[1:5]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# data
names = df_sd.Name
df = abc

# Math Answer
m_ans = pd.read_excel("ACT_Report_3.xlsm", sheet_name="M_Ans").T
header = m_ans.iloc[0]
m_ans = m_ans[1:]
m_ans = m_ans.rename(columns=header)
m_ans.index = range(0, 50)

# Student Answer
sd_ans=pd.read_csv("P01_Answers.csv").T
header=sd_ans.iloc[0]
sd_ans = sd_ans[1:51]
sd_ans = sd_ans.rename(columns=header)
sd_ans.index = range(0, 50)

# Math Grader
def math_grader(math_ans,sd_ans):
    index = []
    for num in range(len(math_ans["Key"])):
        record = []
        # checking answers
        ans = math_ans.iloc[num,0]
        if sd_ans.iloc[num,0] == ans:
            record.append(True)
            index.append(record)
        else:
            record.append(False)
            index.append(record)
    result = pd.DataFrame(index, columns = ["Grade"])
    math_ans['Grade'] = result['Grade']
    grade = pd.DataFrame(math_ans['Grade'].value_counts())
    grade["Ans"] = ["Right", 'Wrong']
    return math_ans, grade

math_result, grade_result = math_grader(m_ans, sd_ans)


app.layout = html.Div([
    html.H4("ACT Student Score", style={"color": "blue", "textAlign": 'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='student',
                options=[{'label': i, 'value': i} for i in names],
                value=f'{names[0]}'
            )
        ],
            style={'width': '45%', 'display': 'inline-block'}
        ),
    ]),

    dcc.Graph(id='sd_grade'),

    html.H4("ACT Subject Score", style={"color": "blue", "textAlign": 'center'}),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='subject',
                options=[{'label': i, 'value': i} for i in columns],
                value='Math',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '60%', 'display': 'inline-block'}
        )
    ]),

    dcc.Graph(id="subject_grade"),

    html.Table([
        html.Tr([html.Td(['Ans Key']), html.Td(id='test_key')]),
        html.Tr([html.Td(['Sd Ans']), html.Td(id='test_grade')])
        ]),

\
], style={'columnCount': 2})


@app.callback(
    Output('sd_grade', 'figure'),
    [Input('student', 'value')]
            )

def update_graph(student_name):

    return {
        'data': [
            go.Bar(
                x=df.index,
                y=df[f"{student_name}"]
            )

        ]
    }

@app.callback(
     Output('subject_grade', 'figure'),
    [Input("subject", "value")]
            )

def update_graph2(subject_name):

    return{
        'data': [
            go.Bar(
                x=df_sd["Name"],
                y=df_sd[f"{subject_name}"]
            )

        ]
    }



if __name__ == '__main__':
    app.run_server(debug=True)

