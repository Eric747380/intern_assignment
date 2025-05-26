import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import BirthForm from './components/BirthForm';
import ChatBox from './components/ChatBox';

function App() {
  const [step, setStep] = useState("landing"); // "landing" → "form" → "chat"
  const [birthDetails, setBirthDetails] = useState(null);

  const handleStart = () => setStep("form");

  const handleBirthFormSubmit = (data) => {
    setBirthDetails(data);
    setStep("chat");
  };

  const handleEditBirthDetails = () => {
    setBirthDetails(null);
    setStep("form");
  };

  return (
    <div className="App">
      {step === "landing" && <LandingPage onStart={handleStart} />}
      {step === "form" && <BirthForm onSubmit={handleBirthFormSubmit} />}
      {step === "chat" && <ChatBox birthDetails={birthDetails} onEdit={handleEditBirthDetails} />}
    </div>
  );
}

export default App;
