import React, { useState } from 'react';
import axios from 'axios';

function BirthForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    dateOfBirth: '',
    timeOfBirth: '',
    placeOfBirth: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/birth_details', formData);
      onSubmit({ ...formData, chart: res.data });
    } catch (err) {
      console.error(err);
      setError('⚠️ Failed to submit birth details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(to bottom right, #fdf4ff, #fef9c3)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'Georgia, serif',
      padding: '2rem'
    }}>
      <form onSubmit={handleSubmit} style={{
        background: '#fff',
        borderRadius: '12px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        padding: '2rem',
        width: '100%',
        maxWidth: '450px',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        <h2 style={{ textAlign: 'center', color: '#7c3aed' }}>🌸 Enter Your Birth Details</h2>

        <label>
          Name
          <input
            type="text"
            name="name"
            required
            placeholder="e.g. Arya"
            onChange={handleChange}
            style={inputStyle}
          />
        </label>

        <label>
          Date of Birth
          <input
            type="date"
            name="dateOfBirth"
            required
            onChange={handleChange}
            style={inputStyle}
          />
        </label>

        <label>
          Time of Birth
          <input
            type="time"
            name="timeOfBirth"
            required
            onChange={handleChange}
            style={inputStyle}
          />
        </label>

        <label>
          Place of Birth
          <input
            type="text"
            name="placeOfBirth"
            required
            placeholder="e.g. Delhi"
            onChange={handleChange}
            style={inputStyle}
          />
        </label>

        <button type="submit" disabled={loading} style={buttonStyle}>
          {loading ? 'Calculating Chart...' : '🪷 Submit & Begin'}
        </button>

        {error && <p style={{ color: 'crimson', textAlign: 'center' }}>{error}</p>}
      </form>
    </div>
  );
}

const inputStyle = {
  width: '100%',
  padding: '0.6rem',
  borderRadius: '6px',
  border: '1px solid #ccc',
  marginTop: '0.25rem'
};

const buttonStyle = {
  marginTop: '1rem',
  padding: '0.75rem',
  backgroundColor: '#a855f7',
  color: 'white',
  fontSize: '1rem',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer'
};

export default BirthForm;
