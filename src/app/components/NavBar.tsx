// Navbar.tsx
"use client";

import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h2><Link to="/">Home</Link></h2>
        
      </div>
    </nav>
  );
}

export default Navbar;
