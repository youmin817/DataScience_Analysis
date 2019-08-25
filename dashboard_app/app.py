import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sklearn.ensemble import RandomForestRegressor

cred = credentials.Certificate("key/grader-2019-firebase-adminsdk-hddfo-d3ec04289a.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://grader-2019.firebaseio.com'
})

# retrive data from firebase
ref = db.reference('act')
df = ref.get()

# find the pattern
act = pd.DataFrame.from_dict(df[0], orient = 'index')


# convert it into dataframe
for i in range(len(df)):
    x = pd.DataFrame.from_dict(df[i], orient = 'index')
    act[i] = x[0]
# change index as ID
act = act.T

# Use github to get data set
act = pd.read_csv("https://raw.githubusercontent.com/youmin817/Data_Analysis/master/dashboard_app/ACT_Test_Score.csv")


df_sd = act.loc[:,["Name","English", "Math", "Reading", "Science", "Composite"]]

# data construction
names = df_sd.Name

df = df_sd.drop("Name", axis=1).T
df.columns = names

# subjects
columns = df_sd.columns[1:5]

# The end for data cleaning




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# prediction set tup train model
x_train = act[["English","Math","Reading"]]
y_train = act["Science"]

# Random Forest Regression for prediction
rfModel = RandomForestRegressor(n_estimators=100)
rfModel.fit(x_train, y_train)


app.layout = html.Div([
    html.H4("ACT Student Score", style={"color": "Black", "textAlign": 'center'}),
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

    html.Hr(),

    html.H4("ACT Subject Score", style={"color": "Black", "textAlign": 'center'}),

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

    html.Hr(),

    html.H6("Enter Diagnostic Test Result", style={"coler": "Black", "textAlign": "center"}),

    html.Table([
        html.Tr([
            html.Td(['Enter English below']),
            html.Td(["Enter Math below"]),
            html.Td(['Enter reading below'])
        ])
    ]),


    html.Div([
        dcc.Input(id='eng-in', value='32', type='text'),
        dcc.Input(id='math-in', value='33', type='text'),
        dcc.Input(id='reading-in', value='34', type='text')

    ]),

    html.Div(html.Div(id='out'))



]) #, style={'columnCount': 2})


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
            go.Line(
                y=df_sd[f"{subject_name}"],
                x=df_sd["Name"]
            )
        ]
    }

@app.callback(
    Output(component_id='out', component_property='children'),
    [Input('eng-in','value'), Input('math-in', 'value'),
     Input('reading-in','value')]
)


def update_output_div(eng, math, reading):
    test_score = [[eng, math, reading]]
    pred_science = rfModel.predict(test_score)

    return 'Future Science Score :  "{0}" '.format(pred_science)



if __name__ == '__main__':
    app.run_server(debug=True)

