import pandas as pd
import sqlite3
import csv
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go

# 取得看板列表
def getBoardList():
    all_boards = open('all_boards.csv')
    reader = csv.reader(all_boards)
    result = list(reader)
    all_boards.close()
    return result

def get_data():
    conn = sqlite3.connect('db/ptt_watcher.db')
    c = conn.cursor()
    c_output = c.execute("select * from board_online_usr_log where log_time > datetime(\'now\',\'localtime\',\'-1 day\');")
    return c_output

# 取得最新一筆資料
def get_last_data():
    conn = sqlite3.connect('db/ptt_watcher.db')
    c = conn.cursor()
    c_output = c.execute("select * from board_online_usr_log ORDER BY log_time DESC LIMIT 1;")
    return c_output

# 取得指定欄位的資料
def get_board_data(board_name):
    conn = sqlite3.connect('db/ptt_watcher.db')
    c = conn.cursor()
    c_output = c.execute("select log_time, [" + board_name.replace('-','_') + "] from board_online_usr_log where log_time > datetime(\'now\',\'localtime\',\'-45 minute\');")
    return c_output


app = Dash()
app.layout = html.Div([
    html.Div(children=[
        dcc.Graph(id='graph-content-bar', style={'width': '1000px','height': '560px','display': 'inline-block'}),
        dcc.Interval(
            id='interval-component-bar',
            interval=4000, # in milliseconds
            n_intervals=0
        ),
        html.Div(children=[
            dcc.Graph(id='graph-content1', style={'width': '630px','height': '190px'}),
            dcc.Interval(
                id='interval-component1',
                interval=4000, # in milliseconds
                n_intervals=0
            ),
            dcc.Graph(id='graph-content2', style={'width': '630px','height': '190px'}),
            dcc.Interval(
                id='interval-component2',
                interval=4000, # in milliseconds
                n_intervals=0
            ),
            dcc.Graph(id='graph-content3', style={'width': '630px','height': '190px'}),
            dcc.Interval(
                id='interval-component3',
                interval=4000, # in milliseconds
                n_intervals=0
            )
        ], style={'display': 'inline-block'})
    ]),
    html.Div(children=[
        dcc.Graph(id='graph-content', style={'width': '1800px','height': '600px','display': 'inline-block'}),
        dcc.Interval(
            id='interval-component',
            interval=4000, # in milliseconds
            n_intervals=0
        )
    ])
])

@callback(
    Output('graph-content1', 'figure'),
    Input('interval-component1', 'n_intervals')
)
def update_graph1(n):
    board_list = getBoardList()
    column_data = ['log_time']
    for i in range(len(board_list)):
        column_data.append(board_list[i][0])
    last_data = pd.DataFrame(get_last_data(), columns=column_data)
    y_column_list = last_data.squeeze(axis=0).drop('log_time').sort_values(ascending=False).head(1)
    y_column = y_column_list.index.to_list()[0]
    chart_data = pd.DataFrame(get_board_data(y_column), columns=['log_time', y_column])
    return px.line(chart_data, x='log_time', y=y_column).update_layout(font_size=16, margin=dict(l=10, r=10, t=10, b=20)).update_xaxes(tickformat="%H:%M\n%Y-%m-%d", title='')
    # return px.line(chart_data, x='log_time', y=y_column, title='上線人數NO.1 ' + y_column + ' ' + str(y_column_list.to_list()[0]) + '人')

@callback(
    Output('graph-content2', 'figure'),
    Input('interval-component2', 'n_intervals')
)
def update_graph2(n):
    board_list = getBoardList()
    column_data = ['log_time']
    for i in range(len(board_list)):
        column_data.append(board_list[i][0])
    last_data = pd.DataFrame(get_last_data(), columns=column_data)
    y_column_list = last_data.squeeze(axis=0).drop('log_time').sort_values(ascending=False).head(2).tail(1)
    y_column = y_column_list.index.to_list()[0]
    chart_data = pd.DataFrame(get_board_data(y_column), columns=['log_time', y_column])
    return px.line(chart_data, x='log_time', y=y_column).update_layout(font_size=16, margin=dict(l=10, r=10, t=10, b=20)).update_xaxes(tickformat="%H:%M\n%Y-%m-%d", title='')
    # return px.line(chart_data, x='log_time', y=y_column, title='上線人數NO.2 ' + y_column + ' ' + str(y_column_list.to_list()[0]) + '人')

@callback(
    Output('graph-content3', 'figure'),
    Input('interval-component3', 'n_intervals')
)
def update_graph3(n):
    board_list = getBoardList()
    column_data = ['log_time']
    for i in range(len(board_list)):
        column_data.append(board_list[i][0])
    last_data = pd.DataFrame(get_last_data(), columns=column_data)
    y_column_list = last_data.squeeze(axis=0).drop('log_time').sort_values(ascending=False).head(3).tail(1)
    y_column = y_column_list.index.to_list()[0]
    chart_data = pd.DataFrame(get_board_data(y_column), columns=['log_time', y_column])
    return px.line(chart_data, x='log_time', y=y_column).update_layout(font_size=16, margin=dict(l=10, r=10, t=10, b=20)).update_xaxes(tickformat="%H:%M\n%Y-%m-%d", title='')
    # return px.line(chart_data, x='log_time', y=y_column, title='上線人數NO.3 ' + y_column + ' ' + str(y_column_list.to_list()[0]) + '人')


@callback(
    Output('graph-content', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    board_list = getBoardList()
    column_data = ['log_time']
    for i in range(len(board_list)):
        column_data.append(board_list[i][0])
    chart_data = pd.DataFrame(get_data(), columns=column_data)
    column_data = chart_data.tail(1).squeeze(axis=0).drop('log_time').sort_values(ascending=False).head(20).index.to_list()
    return px.line(chart_data, x='log_time', y=column_data).update_layout(font_size=14, margin=dict(l=10, r=10, t=10, b=20)).update_xaxes(tickformat="%H:%M\n%Y-%m-%d", title='').update_yaxes(title='')

@callback(
    Output('graph-content-bar', 'figure'),
    Input('interval-component-bar', 'n_intervals')
)
def update_graph_bar(n):
    board_list = getBoardList()
    column_data = ['log_time']
    for i in range(len(board_list)):
        column_data.append(board_list[i][0])
    last_data = pd.DataFrame(get_last_data(), columns=column_data)
    y_column_list = last_data.squeeze(axis=0).drop('log_time').sort_values().tail(10)
    return go.Figure(go.Bar(x=y_column_list.to_list(), y=y_column_list.index.to_list(), orientation='h', text=y_column_list.to_list())).update_layout(font_size=25, margin=dict(l=10, r=10, t=0, b=20))

if __name__ == '__main__':
    app.run(debug=True)

