import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { signup, isLoading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) =>  {
    e.preventDefault();
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    try {
        await signup(email, password);
        navigate('/tasks');
    } catch (err) {
        // Error is handled by context
    }
  };
  
  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
        <h1>Sign Up</h1>
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

            <div style={{ marginBottom: '15px' }}>
                <label>Password</label>
                <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                />
            </div>

            <div style={{ marginBottom: '15px' }}>
                <label>Confirm Password</label>
                <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
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
                backgroundColor: '#28A745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: isLoading ? 'not-allowed' : 'pointer',
            }}
        >
            {isLoading ? 'Signing up...' : 'Sign Up'}
            </button>
        </form>

        <p>
          Already have an account? <a href="/login">Login</a>
        </p>

    </div>
    
    );
};