"use client";
import React, { useState, FormEvent, ChangeEvent } from "react";
import { FaClipboard, FaCheck } from "react-icons/fa"; // Ensure react-icons is installed
import Navbar from "./Navbar";
// Import the Graph component
import Graph from './Graph';
import { pairs, edges } from './edges';
import '../app/globals.css';

// Define your graph elements (nodes and edges) based on your matches
// const elements = [
//   { data: { id: 'Alice' } },
//   { data: { id: 'Bob' } },
//   { data: { id: 'Charlie' } },
//   { data: { id: 'ab', source: 'Alice', target: 'Bob', highlight: 1, weight: '95%' } },
//   { data: { id: 'bc', source: 'Bob', target: 'Charlie', weight: '85%' } },
// ];

// const nodes = new Set<string>();
// const edges = pairs.map(([source, target], index) => {
//   nodes.add(source);
//   nodes.add(target);
//   return { data: { id: `edge${index}`, source, target, label: `${index * 10}%` }}; // Example edge label
// });

// const elements = Array.from(nodes).map(node => ({ data: { id: node } })).concat(edges);

interface ElementData {
  id: string;
  // Include other properties here as needed, e.g., source, target, label, highlight
}

interface GraphElement {
  data: ElementData;
}

const Home: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [matchEmail, setMatchEmail] = useState<string>("match@example.com"); // Placeholder for the match's email
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<boolean>(false);
  const [pickupLine, setPickupLine] = useState<string>("");
  const [similarityPercentage, setSimilarityPercentage] = useState<number>(0);
  const [copied, setCopied] = useState<boolean>(false); // State to manage copy feedback
  const [elements, setElements] = useState<GraphElement[]>([]);

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
  
    // Simulate finding a match and the similarity percentage
    setTimeout(() => {
      setLoading(false);
      setResults(true);
  
      // Assuming 'pairs' is of type Pair[] and 'email' is of type string
      const myPair = pairs.find(pair => pair.includes(email));
      const matchedEmail = myPair?.find(e => e !== email) || "";
  
      console.log("found pair", edges.find(([source, target]) => 
        (source === email && target === matchedEmail) || 
        (target === email && source === matchedEmail)
      ));
  
      let pairsFoundInEdges = 0;
      let pairsNotFoundInEdges = 0;
  
      pairs.forEach(pair => {
        const [email1, email2] = pair;
        if (edges.some(([source, target]) => (source === email1 && target === email2) || (source === email2 && target === email1))) {
          pairsFoundInEdges++;
        } else {
          pairsNotFoundInEdges++;
        }
      });
  
      console.log("Pairs found in edges:", pairsFoundInEdges);
      console.log("Pairs not found in edges:", pairsNotFoundInEdges);
  
      const similarityScore = edges.find(([source, target]) => 
        (source === email && target === matchedEmail) || 
        (target === email && source === matchedEmail)
      )?.[2] as number ?? 0;
      
      // Update states
      setMatchEmail(matchedEmail);
      setSimilarityPercentage(similarityScore ? (1-similarityScore) * 100 : 0);
      setPickupLine(pickupLines[Math.floor(Math.random() * pickupLines.length)]);
      setCopied(false);
  
      // Construct graph elements
      const nodes = new Set<string>();
      edges.forEach(([source, target]) => {
        nodes.add(source as string);
        nodes.add(target as string);
      });
  
      const cyEdges = edges.map(([source, target, weight], index) => {
        const isHighlight = pairs.some(pair => pair.includes(source as string) && pair.includes(target as string));
  
        return {
          data: {
            id: `e${index}`,
            source,
            target,
            label: `${((1-(weight as number)) * 100).toFixed(0)}%`,
            highlight: isHighlight ? 1 : 0,
          }
        };
      });
  
      const cyNodes = Array.from(nodes).map(node => ({ data: { id: node } }));
      setElements([...cyNodes, ...cyEdges]);
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
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-gray-700 to-gray-900 pt-20">
      <Navbar />
      {loading ? (
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-400 mx-auto"></div>
          <h2 className="text-gray-300 text-xl font-semibold mt-5">Quantum entanglement is in progress...</h2>
        </div>
      ) : results && matchEmail === "" ? (
        <div className="text-center p-10 bg-gray-800 text-gray-200 rounded-lg shadow-xl w-full md:w-1/2">
          <h2 className="text-3xl font-bold mb-4">An Apology from MITqute</h2>
          <p className="text-md mb-5">It appears that our quantum algorithms have not found a match for you this time. We deeply apologize for any disappointment this may cause.</p>
          <p className="text-md mb-5">As pioneers in quantum-assisted matchmaking, we understand that our technology is not perfect. Being the first time we've run a dating app on quantum computing, there are bound to be learnings and improvements to be made.</p>
          <p className="text-md mb-5">We are continuously working to enhance our algorithms and hope that you'll give us another chance in the future. Your experience and feedback are invaluable to us as we strive to create more meaningful connections.</p>
          <p className="text-md mb-5">Thank you for your understanding and patience.</p>
          <p className="text-md">Sincerely,</p>
          <p className="text-md font-semibold">MIT qupid</p>
        </div>
      ) : results ? (
        <div className="text-center p-10 bg-gray-800 text-gray-200 rounded-lg shadow-xl">
          <h2 className="text-3xl font-bold mb-4">Quantum Match Found!</h2>
          <p className="text-md mb-1">Match's Email: <span className="font-semibold">{matchEmail}</span></p>
          {
            similarityPercentage !== 0 ? <p className="text-md mb-2">Compatibility: <span className="font-semibold">{similarityPercentage.toFixed(2)}%</span></p>
            : <p className="text-md mb-2">Compatibility: <span className="font-semibold">low - medium confidence</span></p>
          }
          <div className="bg-gray-700 p-4 rounded-lg shadow-inner">
            <p className="text-lg mb-2">Spark a conversation with this quantum pickup line:</p>
            <p className="text-green-400 text-lg font-medium">"{pickupLine}"</p>
          </div>
          <button
            onClick={copyToClipboard}
            className="mt-5 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded flex items-center justify-center mx-auto"
          >
            {copied ? <FaCheck className="mr-2"/> : <FaClipboard className="mr-2"/>}
            {copied ? "Copied!" : "Copy Pickup Line"}
          </button>
          <Graph elements={elements} userEmail={email} />
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