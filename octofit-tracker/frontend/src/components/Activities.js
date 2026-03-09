import React, { useEffect, useState } from 'react';

const ACTIVITIES_API = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

function Activities() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    console.log('Fetching from:', ACTIVITIES_API);
    fetch(ACTIVITIES_API)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, []);

  return (
    <div className="container mt-3">
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h2 className="card-title text-success mb-3">Activities</h2>
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity, idx) => (
                <tr key={idx}>
                  <td>{activity.name}</td>
                  <td>{activity.description || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <button className="btn btn-primary">Add Activity</button>
    </div>
  );
}

export default Activities;
