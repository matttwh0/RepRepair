"use client";

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';

import Navbar from './components/NavBar'; // Import Navbar component
import './globals.css';

function HomePage() {
  const navigate = useNavigate();

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('video', file);

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Error uploading video');
        }

        const angles = await response.json();
        console.log('Video processed:', angles);
      } catch (error) {
        console.error('Error processing video:', error);
      }
    }
  };

  const handleClick = () => {
    document.getElementById('fileInput')?.click();
  };

  const handleResponsePageClick = () => {
    navigate('/responsePage');
  };

  return (
    <>
      <Navbar /> {/* Add Navbar here */}
      <div className="homepage-container">
        <div className="card">
          <h1 className="title">RepRepair</h1>
          <button className="upload-button" onClick={handleClick}>Upload Video</button>
          <input
            id="fileInput"
            type="file"
            accept="video/*"
            style={{ display: 'none' }}
            onChange={handleFileUpload}
          />
          <button className="response-button" onClick={handleResponsePageClick}>Go to Response Page</button>
        </div>
      </div>
    </>
  );
}

function ResponsePage() {
  const navigate = useNavigate();

  const analysisList = [
    { id: 1, title: 'Analysis 1' },
    { id: 2, title: 'Analysis 2' },
    { id: 3, title: 'Analysis 3' },
  ];

  return (
    <div className="second-page-container">
      <div className="analysis-list">
        {analysisList.map((analysis) => (
          <div key={analysis.id} className="analysis-item">
            <h3>{analysis.title}</h3>
            <button className="view-analysis-button" onClick={() => navigate(`/analysis/${analysis.id}`)}>View Analysis</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/responsePage" element={<ResponsePage />} />
        <Route path="/analysis/:id" element={<AnalysisPage />} />
      </Routes>
    </Router>
  );
}

function AnalysisPage() {
  const navigate = useNavigate();
  const messages = [
    "Keep your back straight during squats.",
    "Ensure your knees do not go past your toes.",
    "Maintain a consistent breathing pattern."
  ];

  return (
    <div className="analysis-page-container">
      {messages.map((message, index) => (
        <p key={index} className="hardcoded-message">{message}</p>
      ))}
      <div className="chatgpt-analysis">
        ChatGPT Analysis Content Here
      </div>
      <button className="back-button" onClick={() => navigate('/responsePage')}>Back to Workout Analysis List</button>
    </div>
  );
}

export default App;