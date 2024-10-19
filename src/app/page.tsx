"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import './globals.css';

function HomePage() {
  const router = useRouter();

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      console.log('Video uploaded:', file.name);
      // Redirect to the second page after uploading
      router.push('/second-page');
    }
  };

  const handleClick = () => {
    document.getElementById('fileInput')?.click();
  };

  return (
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
      </div>
    </div>
  );
}