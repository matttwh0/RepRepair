// ResponsePage.tsx (for example)
"use client";

import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/NavBar'; // Adjust path if needed

function ResponsePage() {
  const navigate = useNavigate();

  const analysisList = [
    { id: 1, title: 'Analysis 1' },
    { id: 2, title: 'Analysis 2' },
    { id: 3, title: 'Analysis 3' },
  ];

  return (
    <>
      <Navbar />
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
    </>
  );
}

export default ResponsePage;
