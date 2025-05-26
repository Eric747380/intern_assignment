import React from 'react';

function LandingPage({ onStart }) {
  return (
    <div style={{
      fontFamily: 'Georgia, serif',
      backgroundColor: '#fdf4ff',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '3rem'
    }}>
      <h1 style={{ fontSize: '3rem', color: '#6b21a8' }}>🪷 Ask Devi</h1>
      <p style={{ fontSize: '1.2rem', maxWidth: '600px', textAlign: 'center', marginTop: '1rem' }}>
        Ask Devi is your personalized Vedic astrology guide, powered by ancient wisdom from the
        <strong> Brihat Parasara Hora Sastra</strong> (BPHS) and modern AI.
      </p>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '2rem',
        marginTop: '3rem',
        flexWrap: 'wrap'
      }}>
        {[
          { icon: '📅', title: 'Step 1', text: 'Enter your birth details — date, time, place' },
          { icon: '🧘', title: 'Step 2', text: 'Devi reads your chart and ancient texts' },
          { icon: '🔮', title: 'Step 3', text: 'Ask anything — love, career, purpose' }
        ].map((item, i) => (
          <div key={i} style={{
            background: '#fdf2f8',
            padding: '1rem',
            borderRadius: '1rem',
            width: '200px',
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem' }}>{item.icon}</div>
            <h3 style={{ margin: '0.5rem 0' }}>{item.title}</h3>
            <p style={{ fontSize: '0.95rem' }}>{item.text}</p>
          </div>
        ))}
      </div>

      <button onClick={onStart} style={{
        marginTop: '3rem',
        backgroundColor: '#a855f7',
        color: 'white',
        fontSize: '1.1rem',
        padding: '0.75rem 2rem',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer'
      }}>
        🔭 Begin Reading
      </button>
    </div>
  );
}

export default LandingPage;
