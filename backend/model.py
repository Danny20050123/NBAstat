import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
def visualize(player_name):
    
    columns = ['name', 'SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 
           'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 
           'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE', 'opponent_def_rating', 'opponent_reb', 'opponent_possessions']
    data = pd.read_csv('stats.csv',names=columns,header=0)
    player_data=data[data['name'] == player_name]

    factors= ['FG_PCT', 'FGA', 'FG3A', 'FG3_PCT', 'FTA', 'FT_PCT', 'opponent_def_rating', 'opponent_possessions']
    #linear, linear,   linear,  ???,    ???,      linear, delete,  
    for factor in factors:
        sns.relplot(data=player_data, x=factor, y='PTS', kind='scatter', height=6, aspect=1.5)
        plt.title(f'PTS vs {factor}')
        plt.show()

        player_data.loc[:, f'{factor}_log'] = np.log(player_data[factor].replace(0, np.nan))  # Avoid log(0)
        sns.relplot(data=player_data, x=f'{factor}_log', y='PTS', kind='scatter', height=6, aspect=1.5)
        plt.title(f'Log Transformation: PTS vs {factor}')
        plt.show()

        player_data.loc[:, f'{factor}_sqrt'] = np.sqrt(player_data[factor].replace(0, np.nan))  # Avoid sqrt(0)
        sns.relplot(data=player_data, x=f'{factor}_sqrt', y='PTS', kind='scatter', height=6, aspect=1.5)
        plt.title(f'Square Root Transformation: PTS vs {factor}')
        plt.show()

        player_data.loc[:, f'{factor}_squared'] = np.square(player_data[factor])
        sns.relplot(data=player_data, x=f'{factor}_squared', y='PTS', kind='scatter', height=6, aspect=1.5)
        plt.title(f'Squared Transformation: PTS vs {factor}')
        plt.show()

        player_data.loc[:, f'{factor}_inverse'] = 1 / player_data[factor].replace(0, np.nan)
        sns.relplot(data=player_data, x=f'{factor}_inverse', y='PTS', kind='scatter', height=6, aspect=1.5)
        plt.title(f'Inverse Transformation: PTS vs {factor}')
        plt.show()
        
if __name__ == "__main__":
    visualize("Anthony Edwards")