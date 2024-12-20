// App.tsx - React Frontend
import { useState } from 'react';
import './App.css';

function App() {
  const [playerName, setPlayerName] = useState('');
  const [playerStats, setPlayerStats] = useState<any[]>([]);
  const [error, setError] = useState('');

  const fetchPlayerStats = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/player-stats?name=${encodeURIComponent(playerName)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch player stats');
      }
      const data = await response.json();
      setPlayerStats(data.stats);
      setError('');
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    }
  };

  return (
    <div className="App">
      <h1>NBA Stat Predictor</h1>
      <div className="input-container">
        <input
          type="text"
          placeholder="Enter NBA Player Full Name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
        />
        <button onClick={fetchPlayerStats}>Fetch Stats</button>
      </div>
      {error && <p className="error">{error}</p>}
      {playerStats.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Matchup</th>
              <th>Date</th>
              <th>Minutes Played</th>
              <th>Points</th>
              <th>Rebounds</th>
              <th>Assists</th>
              <th>Steals</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {playerStats.map((game, index) => (
              <tr key={index}>
                <td>{game.MATCHUP}</td>
                <td>{game.GAME_DATE}</td>
                <td>{game.MIN}</td>
                <td>{game.PTS}</td>
                <td>{game.REB}</td>
                <td>{game.AST}</td>
                <td>{game.STL}</td>
                <td>{game.BLK}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;