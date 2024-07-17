from flask import Flask, render_template,json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# Load your data
data = pd.read_csv('election_data.csv')

# Count the number of wins for each party in each state
state_party_counts = data.groupby(['State', 'winner_party'])['winner_party'].count().reset_index(name='count')

# Find the party with the maximum count of wins per state
idx = state_party_counts.groupby(['State'])['count'].idxmax()
max_counts = state_party_counts.loc[idx].reset_index(drop=True)

# Calculate total wins for each party
party_wins = data.groupby('winner_party').size().reset_index(name='count')
party_wins = party_wins.sort_values(by='count', ascending=False)

# Select the top 5 parties
top_5_parties = party_wins.head(5)
other_parties = party_wins[5:].sum(numeric_only=True).to_frame().T
other_parties['winner_party'] = 'Others'
top_5_parties = pd.concat([top_5_parties, other_parties], ignore_index=True)

# Voter turnout data
voter_turnout = {
    "Year": [2004, 2009, 2014, 2019, 2024],
    "Turnout": [58.07, 58.19, 66.40, 67.11, 65.79]
}
voter_turnout_df = pd.DataFrame(voter_turnout)
voter_turnout_df = voter_turnout_df.sort_values(by='Turnout', ascending=False)

with open('india_state.geojson') as f:
        india_geojson = json.load(f)
@app.route('/')
def index():
    # Create a Plotly choropleth map
    fig = px.choropleth(
        max_counts,
        geojson=india_geojson,
        locations='State',
        featureidkey='properties.NAME_1',
        color='winner_party',
        hover_data={'count': True},
        title='Statewise seats of the winners'
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r":20, "t":80, "l":20, "b":20},
        title={'x': 0.5, 'y': 0.95, 'xanchor': 'center', 'yanchor': 'top'},  # Adjust title position
        width=800,
        height=600
    )
    map_html = pio.to_html(fig, full_html=False)

    # Create a Plotly bar chart
    bar_fig = px.bar(
        top_5_parties,
        x='winner_party',
        y='count',
        title='Top 5 Parties by Total Wins',
        labels={'count': 'Number of Wins', 'winner_party': 'Party'},
        color='winner_party'
    )

    bar_fig.update_layout(
        xaxis_title="Party",
        yaxis_title="Number of Wins",
        margin={"r":20, "t":50, "l":20, "b":100},
        xaxis_tickangle=-45,
        bargap=0.2,  # Reduce the gap between bars
        title={'x': 0.5},  # Center the title
        width=800,
        height=600
    )
    bar_html = pio.to_html(bar_fig, full_html=False)

    # Create a Plotly pie chart
    pie_fig = px.pie(
        top_5_parties,
        names='winner_party',
        values='count',
        title='Percentage of Wins for Each Party'
    )

    pie_fig.update_layout(
        margin={"r":20, "t":50, "l":20, "b":20},
        title={'x': 0.5},  # Center the title
        width=800,
        height=300,
    )
    pie_html = pio.to_html(pie_fig, full_html=False)

    # Create a Pareto chart for voter turnout
    pareto_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    pareto_fig.add_trace(
        go.Bar(x=voter_turnout_df['Year'], y=voter_turnout_df['Turnout'], name='Turnout'),
        secondary_y=False,
    )

    pareto_fig.add_trace(
        go.Scatter(x=voter_turnout_df['Year'], y=voter_turnout_df['Turnout'], name='Voter Turnout ', mode='lines+markers'),
        secondary_y=True,
    )

    pareto_fig.update_layout(
        title_text='Voter Turnout Over the Years ',
        xaxis_title='Year',
        yaxis_title='Turnout Percentage',
        
        margin={"r":20, "t":50, "l":20, "b":20},
        width=800,
        height=600
    )
    pareto_html = pio.to_html(pareto_fig, full_html=False)

    # Render the HTML template
    return render_template('index.html', map_html=map_html, bar_html=bar_html, pie_html=pie_html, pareto_html=pareto_html)

if __name__ == '__main__':
    app.run(debug=True)
