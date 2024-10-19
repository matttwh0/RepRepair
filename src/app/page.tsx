"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
//import Image from 'next/image';
import Navbar from './components/NavBar'; // Import Navbar component
import './globals.css';
import liftingImage from './images/lifting.jpeg';

function HomePage() {
  const router = useRouter();

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      console.log('Video uploaded:', file.name);
    }
  };

  const handleClick = () => {
    document.getElementById('fileInput')?.click();
  };

  return (
    <>
      <Navbar /> {}
      <div className="homepage-container">
        {/* <Image src={liftingImage} alt="Lifting" className="lifting-image" width={400} height={300} /> */}
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
    </>
  );
}

export default HomePage;
