from flask import Flask, request, jsonify
from flask_cors import CORS
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas

app = Flask(__name__)
CORS(app)

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    else:
        return None

@app.route('/player-stats', methods=['GET'])
def player_stats():
    """
    Endpoint to retrieve player stats for the last 10 years.
    """
    try:
        player_name = request.args.get('name')
        if not player_name:
            return jsonify({'error': 'Player name is required'}), 400


        player_id = get_player_id(player_name)
        if not player_id:
            return jsonify({'error': f'Player {player_name} not found'}), 404

        all_stats = []
        count=0
        for season in range(2024, 2010, -1):
            season_str = f"{season}-{str(season + 1)[2:]}"
            try:
                game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season_str)
                stats = game_log.get_data_frames()[0]
                
                
                for game in stats.to_dict('records'):
                    game = {'PlayerName': player_name, **game}
                    all_stats.append(game)
                    count += 1
                    if count >= 150:break
                        
                
                if count >= 150:break


            except Exception as e:
                print(f"Error fetching stats for season {season_str}: {e}")
                continue
        stat_df=pandas.concat([pandas.DataFrame(all_stats)], ignore_index=True)
        stat_df.to_csv("stats.csv", mode='a', index=False, header=False)
        print(pandas.read_csv("stats.csv").head(10))
        return jsonify({'stats': all_stats})

    except Exception as e:
        print(f"Unhandled error: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500


if __name__ == '__main__':
    app.run(debug=True)
