// ResponsePage.tsx
// "use client";

// import React, { useEffect, useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import Navbar from '../components/NavBar';

// function ResponsePage() {
//   const navigate = useNavigate();
//   const [videoSrc, setVideoSrc] = useState('');

//   useEffect(() => {
//     // Retrieve the uploaded video URL from localStorage
//     const storedVideo = localStorage.getItem('uploadedVideo');
//     if (storedVideo) {
//       setVideoSrc(storedVideo);
//     }
//   }, []);

//   const analysisList = [
//     { id: 1, title: 'Analysis 1' },
//     { id: 2, title: 'Analysis 2' },
//     { id: 3, title: 'Analysis 3' },
//   ];

//   return (
//     <>
//       <Navbar />
//       <div className="second-page-container">
//         <div className="video-placeholder">
//           {videoSrc ? (
//             <video width="600" controls>
//               <source src={videoSrc} type="video/mp4" />
//               Your browser does not support the video tag.
//             </video>
//           ) : (
//             <p>No video uploaded yet.</p>
//           )}
//         </div>
//         <div className="analysis-list">
//           {analysisList.map((analysis) => (
//             <div key={analysis.id} className="analysis-item">
//               <h3>{analysis.title}</h3>
//               <button className="view-analysis-button" onClick={() => navigate(`/analysis/${analysis.id}`)}>View Analysis</button>
//             </div>
//           ))}
//         </div>
//       </div>
//     </>
//   );
// }

// export default ResponsePage;
