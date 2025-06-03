import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    applicant: '',
    address: '',
    status: '',
    latitude: '',
    longitude: '',
  });

  const [results, setResults] = useState([]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const params = Object.fromEntries(
        Object.entries(formData).filter(([_, v]) => v !== '')
      );

      const response = await axios.get('http://localhost:8000/api/v1/permits', {
        params,
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching permits:', error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>Mobile Food Facility Permits</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 2fr',
            gap: '1rem',
            maxWidth: '400px',
          }}
        >
          {['applicant', 'address', 'status', 'latitude', 'longitude'].map((field) => (
            <React.Fragment key={field}>
              <label htmlFor={field} style={{ textTransform: 'capitalize' }}>
                {field}:
              </label>
              <input
                type="text"
                name={field}
                id={field}
                value={formData[field]}
                onChange={handleChange}
                style={{
                  padding: '0.5rem',
                  borderRadius: '4px',
                  border: '1px solid #ccc',
                }}
              />
            </React.Fragment>
          ))}
        </div>
        <button
          type="submit"
          style={{
            marginTop: '1rem',
            padding: '0.6rem 1.2rem',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Search
        </button>
      </form>

      <h2>Results:</h2>
      {results.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={thStyle}>Applicant</th>
              <th style={thStyle}>Address</th>
              <th style={thStyle}>Status</th>
            </tr>
          </thead>
          <tbody>
            {results.map((permit, index) => (
              <tr key={index}>
                <td style={tdStyle}>{permit.Applicant}</td>
                <td style={tdStyle}>{permit.Address}</td>
                <td style={tdStyle}>{permit.Status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}

// Reusable styles
const thStyle = {
  textAlign: 'left',
  padding: '0.5rem',
  borderBottom: '2px solid #ccc',
  backgroundColor: '#f2f2f2',
};

const tdStyle = {
  padding: '0.5rem',
  borderBottom: '1px solid #ddd',
};

export default App;
