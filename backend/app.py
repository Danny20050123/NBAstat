from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from nba_api.stats.endpoints import playergamelog, leaguedashteamstats, teamgamelog,BoxScoreAdvancedV2
from nba_api.stats.static import players, teams
import pandas
import json

app = Flask(__name__)
CORS(app)

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    else:
        return None

def get_team_stats(season):
    team_stats = leaguedashteamstats.LeagueDashTeamStats(season=season).get_data_frames()[0]
    time.sleep(0.5)
    team_stats['Possessions'] = 0.5 * (
        team_stats['FGA'] + 
        0.4 * team_stats['FTA'] - 
        team_stats['OREB'] + 
        team_stats['TOV']
    )/team_stats['GP']
    team_stats['REB']=team_stats['REB']/team_stats['GP']
    return team_stats.set_index('TEAM_ID')

@app.route('/player-stats', methods=['GET'])
def player_stats():
    try:
        player_name = request.args.get('name')
        if not player_name:
            return jsonify({'error': 'Player name is required'}), 400

        player_id = get_player_id(player_name)
        if not player_id:
            return jsonify({'error': f'Player {player_name} not found'}), 404

        all_stats = []
        count = 0
        for season in range(2024, 2010, -1):
            season_str = f"{season}-{str(season + 1)[2:]}"
            try:
                game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season_str)
                time.sleep(0.5)
                stats = game_log.get_data_frames()[0]
                team_stats = get_team_stats(season_str)

                for game in stats.to_dict('records'):
                    matchup = game['MATCHUP']
                    opponent_team_name = matchup.split(' ')[2]
                    opponent_team_id = teams.find_team_by_abbreviation(opponent_team_name)['id']
                    player_min = game['MIN']

                    if opponent_team_id in team_stats.index:
                        defense = BoxScoreAdvancedV2(game_id=game['Game_ID']).team_stats.get_json()
                        defense=json.loads(defense)
                        time.sleep(0.5)


                        headers = defense['headers']
                        data = defense['data']

                        team_id_index = headers.index('TEAM_ID')
                        def_rating_index = headers.index('DEF_RATING')
                        opponent_def_rating = None 
                        for team in data:
                            if team[team_id_index] == opponent_team_id:
                                opponent_def_rating = team[def_rating_index]
                                break


                            
                        opponent_reb = team_stats.at[opponent_team_id, 'REB']
                        opponent_possessions = team_stats.at[opponent_team_id, 'Possessions']
                    else:
                        opponent_def_rating = None
                        opponent_reb = None
                        opponent_possessions = None

                    player_stats = {
                        'name': player_name,
                        **game,
                        'opponent_def_rating': opponent_def_rating,
                        'opponent_reb': opponent_reb,
                        'opponent_possessions': opponent_possessions,
                    }

                    # Calculate usage percentage

                    all_stats.append(player_stats)
                    count += 1
                    if count >= 150:
                        break

                if count >= 150:
                    break

            except Exception as e:
                print(f"Error fetching stats for season {season_str}: {e}")
                continue

        prev_df = pandas.read_csv('stats.csv')
        prev_df = prev_df.drop(prev_df[prev_df.iloc[:, 0] == player_name].index)
        prev_df.to_csv('stats.csv', index=False)

        stat_df = pandas.concat([pandas.DataFrame(all_stats)], ignore_index=True)
        stat_df.to_csv("stats.csv", mode='a', index=False, header=False)

        print(pandas.read_csv("stats.csv").head(10))
        return jsonify({'stats': all_stats})

    except Exception as e:
        print(f"Unhandled error: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
