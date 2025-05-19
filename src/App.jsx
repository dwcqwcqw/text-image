import React, { useState } from 'react';

const defaultOptions = {
  gender: '',
  age: '',
  style: '',
  clothing: '',
  pose: '',
  background: '',
  art_style: '',
  free_prompt: '',
};

const genders = ['Male', 'Female', 'Other'];
const ages = ['Young', 'Mature'];
const styles = ['Loli', 'Mature Woman', 'Muscular Man', 'Boyish'];
const clothings = ['Nude', 'Semi-nude', 'Lingerie', 'Uniform', 'Bikini', 'Casual'];
const poses = ['Standing', 'Sitting', 'Lying', 'Doggy Style', 'Riding'];
const backgrounds = [
  'Bedroom', 'Bathroom', 'Classroom', 'Infirmary',
  'Beach', 'Hotel Balcony', 'Alley',
];
const artStyles = ['Realistic', 'Anime', '3D Render', 'Manga Sketch'];

const glassStyle = {
  background: 'rgba(30, 30, 40, 0.7)',
  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  backdropFilter: 'blur(12px)',
  WebkitBackdropFilter: 'blur(12px)',
  borderRadius: 20,
  border: '1px solid rgba(255, 255, 255, 0.18)',
  padding: 32,
  marginTop: 48,
};

const buttonStyle = {
  background: 'linear-gradient(90deg, #b993ff 0%, #8ca6ff 100%)',
  color: '#fff',
  border: 'none',
  borderRadius: 12,
  padding: '12px 0',
  fontSize: 18,
  fontWeight: 600,
  cursor: 'pointer',
  boxShadow: '0 2px 8px rgba(140,166,255,0.2)',
  transition: 'background 0.2s',
};

const labelStyle = {
  display: 'flex',
  flexDirection: 'column',
  color: '#fff',
  fontWeight: 500,
  fontSize: 16,
  gap: 4,
};

function App() {
  const [options, setOptions] = useState(defaultOptions);
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setOptions({ ...options, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setImageUrl(null);
    try {
      const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(options),
      });
      if (!res.ok) {
        const err = await res.json();
        setError(err.error || 'Failed to generate image');
        setLoading(false);
        return;
      }
      // Get blob and create object URL
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      setImageUrl(url);
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(120deg, #181824 0%, #23233a 100%)',
      padding: 0,
      margin: 0,
      fontFamily: 'Inter, sans-serif',
    }}>
      <div style={{ maxWidth: 480, margin: '0 auto', paddingTop: 60 }}>
        <h1 style={{ color: '#b993ff', textAlign: 'center', fontWeight: 800, fontSize: 32, letterSpacing: 1, marginBottom: 0 }}>NSFW Text-to-Image</h1>
        <p style={{ color: '#ccc', textAlign: 'center', marginBottom: 32, marginTop: 8, fontSize: 16 }}>Generate characters in any scene. For adults only.</p>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 18, ...glassStyle }}>
          <label style={labelStyle}>
            Gender
            <select name="gender" value={options.gender} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {genders.map(g => <option key={g} value={g}>{g}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Age
            <select name="age" value={options.age} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {ages.map(a => <option key={a} value={a}>{a}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Character Style
            <select name="style" value={options.style} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {styles.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Clothing
            <select name="clothing" value={options.clothing} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {clothings.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Pose
            <select name="pose" value={options.pose} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {poses.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Background
            <select name="background" value={options.background} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {backgrounds.map(b => <option key={b} value={b}>{b}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Art Style
            <select name="art_style" value={options.art_style} onChange={handleChange} style={{ borderRadius: 8, padding: 8, fontSize: 15 }}>
              <option value="">Select</option>
              {artStyles.map(a => <option key={a} value={a}>{a}</option>)}
            </select>
          </label>
          <label style={labelStyle}>
            Free Prompt
            <input
              type="text"
              name="free_prompt"
              value={options.free_prompt}
              onChange={handleChange}
              placeholder="Enter any additional description..."
              style={{ borderRadius: 8, padding: 8, fontSize: 15 }}
            />
          </label>
          <button type="submit" disabled={loading} style={buttonStyle}>
            {loading ? 'Generating...' : 'Generate Image'}
          </button>
        </form>
        {error && <div style={{ color: '#ff6bcb', marginTop: 24, textAlign: 'center', fontWeight: 600 }}>{error}</div>}
        {imageUrl && (
          <div style={{ ...glassStyle, marginTop: 36, textAlign: 'center' }}>
            <img src={imageUrl} alt="Generated" style={{ maxWidth: '100%', borderRadius: 12, marginBottom: 16, boxShadow: '0 2px 16px #0008' }} />
            <a href={imageUrl} download="generated.png" style={{ ...buttonStyle, display: 'inline-block', width: '100%', marginTop: 8, textDecoration: 'none', textAlign: 'center' }}>
              Download Image
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
