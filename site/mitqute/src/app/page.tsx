// "use client";
// import React, { useState, FormEvent, ChangeEvent } from "react";
// import { FaClipboard } from "react-icons/fa"; // Ensure @heroicons/react is installed

// const Home: React.FC = () => {
//   const [email, setEmail] = useState<string>("");
//   const [matchEmail, setMatchEmail] = useState<string>("match@example.com"); // Placeholder for match's email
//   const [loading, setLoading] = useState<boolean>(false);
//   const [results, setResults] = useState<boolean>(false);
//   const [pickupLine, setPickupLine] = useState<string>("");
//   const [similarityPercentage, setSimilarityPercentage] = useState<number>(0);

//   const pickupLines = [
//     "If love is a complex vector space, consider me an eigenstate of desire for you.",
//     "I think our wave functions are in sync because I'm attracted to you in every possible universe.",
//     "I'm not certain about Heisenberg's Uncertainty Principle, but I am certain about my feelings for you.",
//     "Are you a quantum computer? Because you've got my heart in a superposition of love and awe.",
//     "Our chemistry must be made of quantum particles, because I feel entangled with you no matter the distance."
//   ];

//   const handleCheckMatch = async (e: FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     setLoading(true);
//     // Simulate checking for quantum entanglement
//     setTimeout(() => {
//       setLoading(false);
//       setResults(true);
//       const randomIndex = Math.floor(Math.random() * pickupLines.length);
//       setPickupLine(pickupLines[randomIndex]);
//       setSimilarityPercentage(Math.random() * (100 - 85) + 85); // Simulate a similarity percentage
//       // Here you would setMatchEmail with actual matched email from backend
//     }, 2000);
//   };

//   const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value);

//   const copyToClipboard = () => {
//     navigator.clipboard.writeText(pickupLine);
//     alert("Pickup line copied to clipboard!");
//   };

//   return (
//     <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-gray-700 to-gray-900">
//       {loading ? (
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-400 mx-auto"></div>
//           <h2 className="text-gray-300 text-xl font-semibold mt-5">Quantum entanglement is in progress...</h2>
//         </div>
//       ) : results ? (
//         <div className="text-center p-10 bg-gray-800 text-gray-200 rounded-lg shadow-xl">
//           <h2 className="text-3xl font-bold mb-4">Quantum Match Found!</h2>
//           <p className="text-md mb-1">Match's Email: <span className="font-semibold">{matchEmail}</span></p>
//           <p className="text-md mb-2">Compatibility: <span className="font-semibold">{similarityPercentage.toFixed(2)}%</span></p>
//           <div className="bg-gray-700 p-4 rounded-lg shadow-inner">
//             <p className="text-lg mb-2">Spark a conversation with this quantum pickup line:</p>
//             <p className="text-green-400 text-lg font-medium">"{pickupLine}"</p>
//           </div>
//           <button
//             onClick={copyToClipboard}
//             className="mt-5 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 w-full rounded flex items-center justify-center"
//           >
//             Copy Pickup Line <FaClipboard className="ml-2 h-5 w-5" />
//           </button>
//         </div>
//       ) : (
//         <form onSubmit={handleCheckMatch} className="flex flex-col items-center w-full max-w-sm mt-5">
//           <input
//             type="email"
//             placeholder="Enter your email..."
//             className="w-full p-4 mb-4 text-gray-800 rounded-lg focus:ring-4 focus:ring-green-500"
//             value={email}
//             onChange={handleEmailChange}
//             required
//           />
//           <button
//             type="submit"
//             className="w-full py-3 text-xl font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:ring-4 focus:ring-blue-300"
//           >
//             Open the box
//           </button>
//         </form>
//       )}
//     </div>
//   );
// };

// export default Home;


"use client";
import React, { useState, FormEvent, ChangeEvent } from "react";
import { FaClipboard, FaCheck } from "react-icons/fa"; // Ensure react-icons is installed

const Home: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [matchEmail, setMatchEmail] = useState<string>("match@example.com"); // Placeholder for the match's email
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<boolean>(false);
  const [pickupLine, setPickupLine] = useState<string>("");
  const [similarityPercentage, setSimilarityPercentage] = useState<number>(0);
  const [copied, setCopied] = useState<boolean>(false); // State to manage copy feedback

  const pickupLines = [
    "If love is a complex vector space, consider me an eigenstate of desire for you.",
    "I think our wave functions are in sync because I'm attracted to you in every possible universe.",
    "I'm not certain about Heisenberg's Uncertainty Principle, but I am certain about my feelings for you.",
    "Are you a quantum computer? Because you've got my heart in a superposition of love and awe.",
    "Our chemistry must be made of quantum particles, because I feel entangled with you no matter the distance."
  ];

  const handleCheckMatch = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setResults(true);
      const randomIndex = Math.floor(Math.random() * pickupLines.length);
      setPickupLine(pickupLines[randomIndex]);
      setSimilarityPercentage(Math.random() * (100 - 85) + 85); // Simulate a similarity percentage
      // Set match email from backend here
      setCopied(false); // Reset copy state
    }, 2000);
  };

  const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(pickupLine).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset copied state after 2 seconds
    }).catch(err => console.error("Failed to copy: ", err));
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-gray-700 to-gray-900">
      {loading ? (
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-400 mx-auto"></div>
          <h2 className="text-gray-300 text-xl font-semibold mt-5">Quantum entanglement is in progress...</h2>
        </div>
      ) : results ? (
        <div className="text-center p-10 bg-gray-800 text-gray-200 rounded-lg shadow-xl">
          <h2 className="text-3xl font-bold mb-4">Quantum Match Found!</h2>
          <p className="text-md mb-1">Match's Email: <span className="font-semibold">{matchEmail}</span></p>
          <p className="text-md mb-2">Compatibility: <span className="font-semibold">{similarityPercentage.toFixed(2)}%</span></p>
          <div className="bg-gray-700 p-4 rounded-lg shadow-inner">
            <p className="text-lg mb-2">Spark a conversation with this quantum pickup line:</p>
            <p className="text-green-400 text-lg font-medium">"{pickupLine}"</p>
          </div>
          <button
            onClick={copyToClipboard}
            className="mt-5 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded flex items-center justify-center"
          >
            {copied ? <FaCheck className="mr-2"/> : <FaClipboard className="mr-2"/>}
            {copied ? "Copied!" : "Copy Pickup Line"}
          </button>
        </div>
      ) : (
        <form onSubmit={handleCheckMatch} className="flex flex-col items-center w-full max-w-sm mt-5">
          <input
            type="email"
            placeholder="Enter your email..."
            className="w-full p-4 mb-4 text-gray-800 rounded-lg focus:ring-4 focus:ring-green-500"
            value={email}
            onChange={handleEmailChange}
            required
          />
          <button
            type="submit"
            className="w-full py-3 text-xl font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:ring-4 focus:ring-blue-300"
          >
            Open the box
          </button>
        </form>
      )}
    </div>
  );
};

export default Home;
