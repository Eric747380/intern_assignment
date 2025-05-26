import React, { useState } from 'react';
import axios from 'axios';
import ClipLoader from 'react-spinners/ClipLoader';

function ChatBox({ birthDetails, onEdit }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://localhost:5000/ask_question', {
        question: input,
        birthDetails
      });

      const botReply = {
        role: 'devi',
        text: res.data.answer,
        source: res.data.source
      };
      setMessages(prev => [...prev, botReply]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'devi', text: '❌ Failed to get response.' }]);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '1rem' }}>
      <h2>🔮 Chat with Devi</h2>

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        background: '#fdf2f8',
        borderRadius: '12px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        textAlign: 'center',
        fontSize: '1.1rem',
        lineHeight: '1.7'
      }}>
        <h3>🧬 Birth Chart Summary</h3>
        <p>☀️ <strong>Sun Sign:</strong> {birthDetails.chart?.chart?.sunSign}</p>
        <p>🌙 <strong>Moon Sign:</strong> {birthDetails.chart?.chart?.moonSign}</p>
        <p>⬆️ <strong>Ascendant:</strong> {birthDetails.chart?.chart?.ascendant}</p>
      </div>


      <div style={{
        border: '1px solid #ccc',
        borderRadius: '10px',
        padding: '1rem',
        backgroundColor: '#fffafc',
        height: '350px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#dbeafe' : '#fef9c3',
              borderRadius: '12px',
              padding: '0.75rem',
              marginBottom: '0.5rem',
              maxWidth: '80%',
              whiteSpace: 'pre-wrap'
            }}
          >
            <strong>{msg.role === 'user' ? 'You' : 'Devi'}:</strong> {msg.text}
            {msg.source && (
              <div style={{ fontSize: '0.8rem', color: '#777', marginTop: '0.5rem' }}>
                {msg.source}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{ marginTop: '1rem', textAlign: 'center' }}>
            <ClipLoader size={30} color="#6b46c1" loading={true} />
            <p style={{ marginTop: '0.5rem' }}>Devi is thinking...</p>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} style={{ marginTop: '1rem' }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask a question..."
          style={{
            width: '70%',
            padding: '0.5rem',
            borderRadius: '6px',
            border: '1px solid #ccc'
          }}
        />
        <button type="submit" style={{
          marginLeft: '1rem',
          padding: '0.5rem 1rem',
          borderRadius: '6px',
          border: 'none',
          backgroundColor: '#6b46c1',
          color: 'white'
        }}>Send</button>
      </form>
    </div>
  );
}

export default ChatBox;
