import React, { useState } from 'react';
import { useAuthStore } from './store/authStore';
import LoginPage from './components/LoginPage';
import Dashboard from './components/dashboard/Dashboard';
import './App.css';

function App() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="app">
      {!isAuthenticated ? <LoginPage /> : <Dashboard />}
    </div>
  );
}

export default App;
