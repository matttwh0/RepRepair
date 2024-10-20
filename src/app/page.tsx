"use client";
import React, { useState, useEffect } from 'react';
import './globals.css';

function HomePage() {
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [videoURL, setVideoURL] = useState<string | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [displayedAnalysis, setDisplayedAnalysis] = useState<string>('');

const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (file) {
    // Reset all states for the new upload
    setIsLoading(true);
    setAnalysis(null);
    setVideoURL(null);
    setMessages([]);
    setDisplayedAnalysis('');

    // Create an object URL to show the uploaded video
    const videoURL = URL.createObjectURL(file);

    // Simulate processing time of 5 seconds
    setTimeout(() => {
      setVideoURL(videoURL);
      try {
        // Hardcoded analysis for demo purposes
        const analysisText = "Yoou executed several correct reps with good depth on many of them, especially your second and last ones where your elbow angles were well within a good range. However, your incorrect reps showed a noticeable imbalance, particularly in the first and fourth incorrect attempts, where your left elbow angle was considerably higher than your right. This indicates some muscle imbalance that needs to be addressed.\n**Improvements for the future:**\n- \nWork on achieving more consistent elbow angles across all sets, particularly focusing on not letting one elbow angle out heavier than the other.\n- Make sure to go deeper in your movements to ensure maximum engagement of the shoulder muscles.\n- Pay attention to maintaining balance throughout the set, particularly in those reps where you felt less stable or noticed the discrepancy in elbow angles.\nKeep up the good work, and focus on these points for your next set!";

        setAnalysis(analysisText);
      } catch (error) {
        console.error('Error processing video:', error);
        setAnalysis('Error processing video');
      } finally {
        setIsLoading(false);
      }
    }, 5000);
  }
};




 useEffect(() => {
  if (analysis && typeof analysis === 'string') {
    let currentIndex = 0;
    setDisplayedAnalysis(''); // Reset the displayed analysis

    const typingInterval = setInterval(() => {
      if (currentIndex < analysis.length) {
        setDisplayedAnalysis((prev) => prev + analysis[currentIndex]);
        currentIndex++;
      } else {
        clearInterval(typingInterval);
      }
    }, 50); // Adjust typing speed here (milliseconds per character)

    return () => clearInterval(typingInterval);
  }
}, [analysis]);


const handleClick = () => {
  document.getElementById('fileInput')?.click();
};



  return (
    <div className="background-wrapper">
      <div className="homepage-container">
        <div className="card left-section">
          <h1 className="title">RepRepair</h1>
          <button className="upload-button" onClick={handleClick}>Upload Video</button>
          <input
            id="fileInput"
            type="file"
            accept="video/*"
            style={{ display: 'none' }}
            onChange={handleFileUpload}
          />
          <div className="hardcoded-messages">
            {messages.map((message, index) => (
              <p key={index} className="hardcoded-message">{message}</p>
            ))}
          </div>
        </div>

        <div className="right-section">
          <div className="right-content">
            {isLoading ? (
              <div className="loading-circle"></div>
            ) : (
              <>
                {videoURL && (
                  <div className="video-container">
                    <video controls autoPlay src={videoURL} className="uploaded-video"></video>
                  </div>
                )}
                {videoURL && (
                  <div className="analysis-container analysis-card">
                    <h1>Analysis</h1>
                    <p>{displayedAnalysis}</p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;