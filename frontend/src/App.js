import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000';

axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [editing, setEditing] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [mode, setMode] = useState('login');

  useEffect(() => {
    if (isLoggedIn) fetchItems();
  }, [isLoggedIn]);

  const fetchItems = () => {
      axios.get(`${API_BASE}/items`)
        .then(res => setItems(res.data))
        .catch(err => console.error('Error fetching items:', err));
  };

  const handleSubmit = e => {
    e.preventDefault();
    const method = editing ? 'put' : 'post';
    const url = `${API_BASE}/items${editing ? `/${editing}` : ''}`;
      axios[method](url, { name }, {
          headers: {
              'Content-Type': 'application/json',
          }
      }).then(() => {
          setEditing(null);
          setName('');
          fetchItems();
      }).catch(err => {
          console.error('Error submitting item:', err.response?.data || err.message);
      });
  };

  const handleEdit = (item) => {
    setEditing(item.id);
    setName(item.name);
  };

  const handleDelete = (id) => {
    axios.delete(`${API_BASE}/items/${id}`).then(fetchItems);
  };

    const handleRegister = e => {
        e.preventDefault();
        axios.post(`${API_BASE}/auth/register`, { username, password })
            .then(() => {
                alert('Registration successful. You can now log in.');
                setMode('login');
                setUsername('');
                setPassword('');
            })
            .catch(() => alert('Registration failed (username may already be taken).'));
    };

  const handleLogin = e => {
    e.preventDefault();
      axios.post(`${API_BASE}/auth/login`, { username, password })
        .then(res => {
          localStorage.setItem('token', res.data.access_token);
            setIsLoggedIn(true);
            setUsername('');
            setPassword('');
        })
        .catch(() => alert('Invalid credentials'));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setItems([]);
  };

  if (!isLoggedIn) {
      return (
          <div style={{ padding: '2rem' }}>
            <h2>{mode == 'login' ? 'Login' : 'Register'}</h2>
            <form onSubmit={mode == 'login' ? handleLogin : handleRegister}>
              <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
              <button type="submit">{mode == 'login' ? 'Login' : 'Register'}</button>
            </form>
            <p>
              {mode == 'login'
                ? <>Do not have an account? <button onClick={() => setMode('register')}>Register</button></>
                : <>Already registered? <button onClick={() => setMode('login')}>Login</button></>
              }
            </p>
          </div>
      );
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Items</h2>
      <button onClick={handleLogout}>Logout</button>
      <form onSubmit={handleSubmit}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <button type="submit">{editing ? 'Update' : 'Add'}</button>
        {editing && <button onClick={() => { setEditing(null); setName(''); }}>Cancel</button>}
      </form>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} &nbsp;
            <button onClick={() => handleEdit(item)}>Edit</button> &nbsp;
            <button onClick={() => handleDelete(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
