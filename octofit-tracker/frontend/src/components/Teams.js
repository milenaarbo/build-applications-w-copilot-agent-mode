import React, { useEffect, useState } from 'react';

const TEAMS_API = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

function Teams() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    console.log('Fetching from:', TEAMS_API);
    fetch(TEAMS_API)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setTeams(results);
        console.log('Fetched teams:', results);
      })
      .catch(err => console.error('Error fetching teams:', err));
  }, []);

  return (
    <div className="container mt-3">
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h2 className="card-title text-warning mb-3">Teams</h2>
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Name</th>
                <th>Members</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((team, idx) => (
                <tr key={idx}>
                  <td>{team.name}</td>
                  <td>{team.members ? team.members.join(', ') : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <button className="btn btn-warning">Create Team</button>
    </div>
  );
}

export default Teams;
