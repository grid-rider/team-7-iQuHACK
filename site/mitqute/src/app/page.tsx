"use client"
import React, { useState, FormEvent, ChangeEvent } from 'react';

const Home: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false); // Track loading state

  const handleCheckMatch = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setLoading(true); // Set loading to true when the form is submitted
    console.log('Checking match for:', email);

    // Simulate an API call with setTimeout
    setTimeout(() => {
      // This is where you would normally handle the API response
      console.log('Match found or not found, this is the question!');
      setLoading(false); // Reset loading state
    }, 2000); // Simulate API call delay
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setEmail(e.target.value);
  };

  if (loading) {
    // Display the loading screen with a joke about Schrödinger's cat
    return (
      <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-cyan-500 to-blue-700">
        <div className="text-white text-center">
          <h2 className="mb-4 text-3xl font-bold">Checking your quantum entanglement...</h2>
          <p className="text-lg">Is your match both found and not found until we observe the result? 🐱‍👓📦</p>
          <p>Hang tight, we're collapsing the wavefunction!</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-cyan-500 to-blue-700">
      <div className="text-white">
        <h1 className="mb-4 text-4xl font-bold text-center">MITqute 🌌</h1>
        <p className="mb-8 text-lg text-center">Enter your email to check your quantum match status!</p>
        <form className="flex flex-col items-center justify-center w-full max-w-md" onSubmit={handleCheckMatch}>
          <input
            type="email"
            placeholder="Your MIT email..."
            className="w-full px-4 py-2 mb-4 text-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
            value={email}
            onChange={handleEmailChange}
            required
          />
          <button
            type="submit"
            className="w-full px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-300"
          >
            Check Match
          </button>
        </form>
      </div>
    </main>
  );
}

export default Home;
