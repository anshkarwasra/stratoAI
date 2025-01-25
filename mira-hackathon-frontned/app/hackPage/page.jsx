"use client"

import React, { useState, useEffect } from 'react';
import { Clock, Rocket } from 'lucide-react';
import { useRouter } from 'next/navigation';

const featchData = (jsonData)=>{
  let newArr = jsonData.data.split('###');
  return newArr
}

const HackathonMentorUI = () => {
  const router = useRouter();
  const [IsLoading, setIsLoading] = useState(true);
  const [timeRemaining, setTimeRemaining] = useState(48 * 60 * 60);
  const [hackathonDetails, setHackathonDetails] = useState(null);
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [ProjArr, setProjArr] = useState([])

  const [projectIdeas, setProjectIdeas] = useState([
    {
      name: "GreenUrban Navigator",
      description: "AI-powered platform for sustainable urban living",
      progress: 35,
      difficulty: "Medium",
    },
    {
      name: "Waste2Resource Exchange",
      description: "Blockchain marketplace for waste recycling",
      progress: 20,
      difficulty: "Hard",
    },
  ]);

  useEffect(() => {
    const storedDetails = localStorage.getItem("hackathonDetails");
    const generatePrompt = (details) => {
      const prompt = `
Generate hackathon project ideas for a ${details.hackathonName} focusing on ${details.type} with a duration of ${details.duration} hours. 
The participants have expertise in ${details.techExpertise}. 
`;
      setGeneratedPrompt(prompt);
    };

    const fetchTopics = async () => {
      try {
        let ideas = generatedPrompt;
        const res = await fetch("http://localhost:5000/getData", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            details: ideas,
          }),
        });
        const data = await res.json();
        setProjArr(featchData(data))
        let titleArr = [],
          desArr = [];
        let senArr = data.data.split("\n\n");
        let objArr = [];

        senArr.forEach((element) => {
          element = element.trim();

          if (element.startsWith("###")) {
            titleArr.push(element.replace("###", "").trim());
          } else if (element.includes("Brief Description:")) {
            let description = element.split("Brief Description:")[1].trim();
            desArr.push(description);
          }
        });

        for (let i = 0; i < Math.min(titleArr.length, desArr.length); i++) {
          objArr.push({
            name: titleArr[i],
            description: desArr[i],
            progress: Math.round(Math.random() * 100),
            difficulty: "Medium",
          });
        }
        
        setProjectIdeas(objArr);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching topics:", error);
        setIsLoading(false);
      }
    };

    if (storedDetails) {
      const details = JSON.parse(storedDetails);
      setHackathonDetails(details);
      generatePrompt(details);
      setTimeRemaining(details.duration);
    }

    fetchTopics();
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  // Cursor effect logic
  useEffect(() => {
    const cursor = document.getElementById('cursor');
    
    if (cursor) {  // Check if the cursor element exists
      const updateCursor = (e) => {
        cursor.style.top = `${e.pageY - 20}px`;
        cursor.style.left = `${e.pageX - 20}px`;
      };

      window.addEventListener('mousemove', updateCursor);

      return () => {
        window.removeEventListener('mousemove', updateCursor);
      };
    }
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining(prev => prev <= 0 ? 0 : prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleClick = (index) =>{
    const jsonData = ProjArr[index];
    console.log(jsonData)
    localStorage.setItem('hackathonProjectDetails',JSON.stringify(jsonData));
    router.push('/hackathon')
  }

  if (IsLoading) {
    return (
      <div className='flex flex-col items-center justify-center'>
        Loading ideas ........ please wait
      </div>
    );
  }
  
  return (
    <div className="min-h-screen py-6 bg-gradient-to-br from-gray-800 via-gray-900 to-black text-white">
      <div className="container mx-auto">
        {/* Hackathon Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-extrabold text-gray-100 tracking-tight">Mira AI Hackathon</h1>
        </div>

        {/* Time Remaining & Progress */}
        <div className="bg-gray-800/80 p-6 rounded-xl mb-8 flex items-center shadow-2xl">
          <Clock className="mr-6 text-white text-3xl" />
          <div>
            <div className="text-2xl font-semibold text-white">Time Remaining: {formatTime(timeRemaining)}</div>
            <div className="w-full bg-gray-700 h-4 mt-2 rounded-full overflow-hidden">
              <div
                className="bg-blue-500 h-full"
                style={{ width: `${(timeRemaining / (48 * 60 * 60)) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Project Ideas */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {projectIdeas.map((project, index) => (
            <div
              onClick={()=> handleClick(index)}
              key={index}
              className="bg-gradient-to-br from-gray-700 via-gray-800 to-gray-900 p-8 rounded-2xl shadow-2xl hover:scale-105 transition-all cursor-pointer"
            >
              <div className="flex flex-col space-y-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-3xl font-bold text-white">{project.name}</h2>
                  <Rocket className="text-blue-400" />
                </div>
                <p className="text-gray-300">{project.description}</p>

                {/* Difficulty */}
                <div className="flex justify-between items-center">
                  <span className="text-white font-semibold text-lg">Difficulty: {project.difficulty}</span>
                </div>

                {/* Progress Indicator */}
                <div className="flex items-center space-x-4">
                  <div className="w-full bg-gray-700 h-2 rounded-full">
                    <div
                      className="bg-blue-500 h-full rounded-full"
                      style={{ width: `${project.progress}%` }}
                    ></div>
                  </div>
                  <span className="text-white font-semibold">{project.progress}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cursor Effect */}
      <div id="cursor" className="fixed w-12 h-12 bg-white rounded-full transition-all ease-in-out duration-200"></div>
    </div>
  );
};

export default HackathonMentorUI;