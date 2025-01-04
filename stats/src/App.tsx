// App.tsx - React Frontend
import { useState } from 'react';
import './App.css';
function App() {
  const [playerName, setPlayerName] = useState('');
  const [opponentTeam, setOpponentTeam] = useState('');
  const [playerStats, setPlayerStats] = useState<any[]>([]);
  const [predicted, setPredicted] = useState<string | null>(null);
  const [error, setError] = useState('');

  const fetchPlayerStats = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/player-stats?name=${encodeURIComponent(playerName)}&opponent=${encodeURIComponent(opponentTeam)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch player stats');
      }
      const data = await response.json();
      setPlayerStats(data.stats);
      setPredicted(data.predicted);
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
    
    <div>
      <div className="sticky top-0 bg-white p-4 shadow-md z-10 flex flex-col items-center justify-center">
        <input
          type="text"
          placeholder="Enter NBA Player Full Name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          className="w-full max-w-md p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        />
        <input
          type="text"
          placeholder="Enter Opponent Team Name"
          value={opponentTeam}
          onChange={(e) => setOpponentTeam(e.target.value)}
          className="w-full max-w-md p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        />
        <button onClick={fetchPlayerStats} className="hover:bg-gray-400 rounded-3xl px-4 py-2 border border-gray-300">Fetch Stats</button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="mt-5 w-full max-w-4xl mx-auto text-center"> {/* Wrap it with a div to apply centering */}
        {error && <p className="error">{error}</p>}
        
        <p className="predicted-info">{predicted}</p>
      </div>
      <div className="mt-5 w-full">
        
        {playerStats.length > 0 && (
          <table className="mt-5 w-full max-w-4xl mx-auto">
            <thead className="bg-gray-200 sticky top-[188px] z-20">
              <tr>
                <th className="px-4 py-2 border border-gray-300">Matchup</th>
                <th className="px-4 py-2 border border-gray-300">Date</th>
                <th className="px-4 py-2 border border-gray-300">Minutes Played</th>
                <th className="px-4 py-2 border border-gray-300">Points</th>
                <th className="px-4 py-2 border border-gray-300">Rebounds</th>
                <th className="px-4 py-2 border border-gray-300">Assists</th>
                <th className="px-4 py-2 border border-gray-300">Steals</th>
                <th className="px-4 py-2 border border-gray-300">Blocks</th>
                <th className="px-4 py-2 border border-gray-300">Opp Defensive Rating</th>
              </tr>
            </thead>
            <tbody>
              {playerStats.map((game, index) => (
                <tr key={index}>
                  <td className="px-4 py-2 border border-gray-300">{game.MATCHUP}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.GAME_DATE}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.MIN}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.PTS}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.REB}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.AST}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.STL}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.BLK}</td>
                  <td className="px-4 py-2 border border-gray-300">{game.opponent_def_rating}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;