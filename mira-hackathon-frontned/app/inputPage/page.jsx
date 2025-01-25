"use client"
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const techExpertiseOptions = [
  'Frontend Development',
  'Backend Development', 
  'Full-Stack Development',
  'Machine Learning',
  'DevOps',
  'Mobile Development',
  'Data Science',
  'Cybersecurity',
  'Cloud Computing'
];

const HackathonSetupPage = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    hackathonName: '',
    duration: '',
    type: '',
    techExpertise: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    localStorage.setItem('hackathonDetails', JSON.stringify(formData));
    router.push('/hackPage');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('/background-pattern.svg')] opacity-20 blur-sm"></div>
      
      <div className="relative z-10 bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-10 w-full max-w-md shadow-2xl">
        <h1 className="text-3xl font-bold text-white text-center mb-8">Hackathon Setup</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-white mb-2">Hackathon Name</label>
            <input 
              type="text" 
              value={formData.hackathonName}
              onChange={(e) => setFormData({...formData, hackathonName: e.target.value})}
              required
              className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-white mb-2">Hackathon Duration</label>
            <input 
              type="number" 
              value={formData.duration}
              onChange={(e) => setFormData({...formData, duration: e.target.value})}
              placeholder="Hours"
              required
              className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-white mb-2">Hackathon Type</label>
            <input 
              type="text" 
              value={formData.type}
              onChange={(e) => setFormData({...formData, type: e.target.value})}
              required
              className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-white mb-2">Technical Expertise</label>
            <select 
              value={formData.techExpertise}
              onChange={(e) => setFormData({...formData, techExpertise: e.target.value})}
              required
              className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Expertise</option>
              {techExpertiseOptions.map((option) => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </div>
          
          <button 
            type="submit" 
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg transition-colors"
          >
            Start Hackathon
          </button>
        </form>
      </div>
    </div>
  );
};

export default HackathonSetupPage;