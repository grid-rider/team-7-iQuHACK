"use client"
import React, { useState, FormEvent, ChangeEvent, useEffect } from 'react';

const Home: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<boolean>(false);
  const [pickupLine, setPickupLine] = useState<string>('');

  const pickupLines = [
    "If love is a complex vector space, consider me an eigenstate of desire for you.",
    "I think our wave functions are in sync because I'm attracted to you in every possible universe.",
    "I'm not certain about Heisenberg's Uncertainty Principle, but I am certain about my feelings for you.",
    "Are you a quantum computer? Because you've got my heart in a superposition of love and awe.",
    "Our chemistry must be made of quantum particles, because I feel entangled with you no matter the distance."
  ];

  const handleCheckMatch = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setLoading(true);
    setResults(false);
    console.log('Checking match for:', email);

    setTimeout(() => {
      console.log('Match found or not found, this is the question!');
      setLoading(false);
      setResults(true);

      const randomIndex = Math.floor(Math.random() * pickupLines.length);
      setPickupLine(pickupLines[randomIndex]);
    }, 2000);
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setEmail(e.target.value);
  };

  const handleGeneratePickupLine = () => {
    const randomIndex = Math.floor(Math.random() * pickupLines.length);
    setPickupLine(pickupLines[randomIndex]);
  };

  useEffect(() => {
    setLoading(false); // Make sure loading state is reset when component mounts
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-pink-500 to-pink-700">
      <div className="text-white">
        <h1 className="mb-4 text-4xl font-bold text-center">MITqute 🌌</h1>
        {loading && (
          <div className="text-center">
            <h2 className="mb-4 text-3xl font-bold">Checking your quantum entanglement...</h2>
            <p className="text-lg">Your match both found and not found until we observe the result... 🐱‍👓📦</p>
            <p>🧠💕💘Hang tight, we're collapsing the wavefunction!💘🌹🌸</p>
          </div>
        )}
        {!loading && !results && (
          <form className="flex flex-col items-center justify-center w-full max-w-md" onSubmit={handleCheckMatch}>
            <input
              type="email"
              placeholder="Your email..."
              className="w-full px-4 py-2 mb-4 text-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
              value={email}
              onChange={handleEmailChange}
              required
            />
            <button
              type="submit"
              className="w-full px-6 py-2 text-white bg-teal-400 rounded-lg hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              Check Match
            </button>
          </form>
        )}
        {results && !loading && (
          <div className="text-center">
            <h2 className="mb-4 text-3xl font-bold">Your match is...</h2>
            <p className="text-lg"> (placeholder)!!</p>
            <p className="text-lg">Try our pickup line to speed up your quantum dating: </p>
            <p className="text-lg">{pickupLine}</p>
            <button
              onClick={handleGeneratePickupLine}
              className="mt-4 px-6 py-2 text-white bg-teal-400 rounded-lg hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              Generate New Pickup Line
            </button>
          </div>
        )}
      </div>
    </main>
  );
};

export default Home;
