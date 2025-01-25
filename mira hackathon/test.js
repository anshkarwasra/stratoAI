const featchTopics = async ()=>{
    let ideas = `
        [
  {
    "project_name": "EcoDrive",
    "readme": "# EcoDrive\nAn AI-powered route planner for sustainable transportation.\n\n## Features\n- Route optimization\n- Carbon footprint analysis\n\n## Tech Stack\n- React Native\n- Node.js\n- OpenAI API"
  },
  {
    "project_name": "HealthTrack",
    "readme": "# HealthTrack\nA personal health monitoring and analytics app.\n\n## Features\n- Heart rate monitoring\n- Sleep pattern analysis\n\n## Tech Stack\n- Flutter\n- Python\n- TensorFlow"
  },
  {
    "project_name": "EduAssist",
    "readme": "# EduAssist\nAn AI-driven platform to assist students in personalized learning.\n\n## Features\n- AI-generated study plans\n- Interactive quizzes\n- Progress tracking\n\n## Tech Stack\n- Angular\n- Django\n- Hugging Face Transformers"
  },
  {
    "project_name": "AgriSmart",
    "readme": "# AgriSmart\nA platform for precision farming using IoT and AI.\n\n## Features\n- Crop monitoring with IoT sensors\n- AI-based yield predictions\n- Weather forecasting integration\n\n## Tech Stack\n- Vue.js\n- Flask\n- PyTorch"
  }
]

    `;
    const res = await fetch('http://localhost:5000/getEvals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            details: ideas
        })
    })
    const data = await res.json();
    console.log(data)
    return data

}

featchTopics();