
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

df = pd.read_csv('C:\Coding\IA\Week8\FormattedDF2.csv').drop(
    ["Unnamed: 0"], axis=1)


@app.route('/', methods=['GET', 'POST'])
def dropdown():
    teams = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton',
             'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham',
             'Leeds United', 'Leicester City', 'Liverpool', 'Manchester City',
             'Manchester United', 'Newcastle United', 'Norwich City',
             'Nottingham Forest', 'Southampton', 'Tottenham', 'Watford',
             'West Ham', 'Wolves']

    selected_team = None
    selected_rows = pd.DataFrame()
    if request.method == 'POST':
        selected_team = request.form['team']
        selected_rows = df[df['team'] == selected_team]

    return render_template('test.html', teams=teams, selected_rows=selected_rows, data=df)


if __name__ == "__main__":
    app.run(host="localhost", port=int("8000"))
