import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login, isLoading, error } = useAuth();
    const navigate = useNavigate();


    const handleSubmit = async (e: React.FormEvent) =>  {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/tasks');
    } catch (err) {
        // Error is handled by context
    }
    };

    return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
    <h1>Login</h1>
    {error && <p style={{ color: 'red' }}>{error}</p>}

    <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
            <label>Email:</label>
            <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
        </div>

        <div style ={{ marginBottom: '15px' }}>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
              />
        </div>

        <button 
        type="submit"
        disabled={isLoading}
        style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#007BFF',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
        }}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
    </form>


<p>
    You do not have an account? <a href="/signup">Sign up here</a>
</p>
    </div>
);
};
// This component provides a login form for users to authenticate. It uses the AuthContext to handle the login process and displays any errors that occur. Upon successful login, it navigates the user to the tasks page.