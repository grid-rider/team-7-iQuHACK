"use client"
import React, { useState, FormEvent, ChangeEvent } from 'react';

const Home: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false); // Track loading state
  const [results, setResults] = useState<boolean>(false); // Track results state
  const [pickupLine, setPickupLine] = useState<string>(''); // Track random pickup line

  // Define an array of pickup lines
  const pickupLines = ["If love is a complex vector space, consider me an eigenstate of desire for you."
  ,"I think our wave functions are in sync because I'm attracted to you in every possible universe."
  , "I'm not certain about Heisenberg's Uncertainty Principle, but I am certain about my feelings for you."
  , "Are you a quantum computer? Because you've got my heart in a superposition of love and awe."
  , "Our chemistry must be made of quantum particles, because I feel entangled with you no matter the distance."
];

  const handleCheckMatch = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setLoading(true); // Set loading to true when the form is submitted
    setResults(false);
    console.log('Checking match for:', email);

    // Simulate an API call with setTimeout
    setTimeout(() => {
      // This is where you would normally handle the API response
      console.log('Match found or not found, this is the question!');
      setLoading(false); // Reset loading state
      setResults(true);

      // Generate and set a random pickup line
      const randomIndex = Math.floor(Math.random() * pickupLines.length);
      setPickupLine(pickupLines[randomIndex]);
    }, 2000); // Simulate API call delay
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setEmail(e.target.value);
  };

  if (loading) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-pink-100 to-pink-300">
        <div className="text-pink-700 text-center">
          <h2 className="mb-4 text-3xl font-bold">Checking your quantum entanglement...</h2>
          <p className="text-lg">Your match both found and not found until we observe the result... 🐱‍👓📦</p>
          <p>🧠💕💘Hang tight, we're collapsing the wavefunction!💘🌹🌸</p>
        </div>
      </main>
    );
  }

  if (results) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-pink-100 to-pink-300">
        <div className="text-pink-700 text-center">
          <h2 className="mb-4 text-3xl font-bold">Your match is...</h2>
          <p className="text-lg"> (placeholder)!!</p>
          <p className="text-lg">Random Pickup Line: {pickupLine}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-br from-pink-500 to-pink-700">
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
            className="w-full px-6 py-2 text-white bg-teal-400 rounded-lg hover:bg-teal-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
          >
            Check Match
          </button>
        </form>
      </div>
    </main>
  );
}

export default Home;
