import React, { useEffect, useState } from 'react';

const USERS_API = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    console.log('Fetching from:', USERS_API);
    fetch(USERS_API)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setUsers(results);
        console.log('Fetched users:', results);
      })
      .catch(err => console.error('Error fetching users:', err));
  }, []);

  return (
    <div className="container mt-3">
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h2 className="card-title text-secondary mb-3">Users</h2>
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, idx) => (
                <tr key={idx}>
                  <td>{user.username}</td>
                  <td>{user.email || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <button className="btn btn-secondary">Add User</button>
    </div>
  );
}

export default Users;
