import pandas as pd

# Specify the correct encoding (e.g., 'utf-8', 'latin-1', 'cp1252', etc.)
df = pd.read_csv(r'C:\Users\Deepak\OneDrive\Desktop\New folder (2)\eci_data_2024.csv', encoding='latin-1')
const1=pd.DataFrame()

const=df.groupby(['Constituency'])['Constituency'].unique()
st=df.groupby(['Constituency'])['State'].unique()

const1['constituency']=const

winner=df.groupby(['Constituency'])['Total Votes'].unique()
winner_party=df.groupby(['Constituency'])['Party'].unique()
# print(winner_party.head())
# print(winner.head())
win=pd.DataFrame()
win['votes']=winner
win['winner_party']=winner_party
win['state']=st
max_vote=[]
for index, row in win.iterrows():
    max_vote.append(row['votes'][0])

party=[]
for index, row in win.iterrows():
    party.append(row['winner_party'][0])

state=[]
for index, row in win.iterrows():
    state.append(row['state'][0])





constituency=[]
for index, row in const1.iterrows():
    constituency.append(row['constituency'][0])
win['constituency']=constituency


win['winner_party']=party
win['max']=max_vote
win['State']=state

data=pd.DataFrame()
data['constituency']=win['constituency']
data['max_votes']=win['max']
data['winner_party']=win['winner_party']
data['State']=win['State']

print(data.head())



data.to_csv('election_data.csv')