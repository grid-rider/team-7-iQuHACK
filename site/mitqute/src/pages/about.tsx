// About.js
import React from "react";
import Navbar from "../app/Navbar";
import '../app/globals.css';

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 to-gray-900 text-white py-12">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-4">About MITqute</h1>
        <p className="mb-4 text-lg">
          At MITqute, we're pioneering the intersection of quantum computing and social connectivity to bring forth a new era of matchmaking.
        </p>
        <h2 className="text-3xl font-semibold mb-3">Our Mission</h2>
        <p className="mb-4 text-lg">
          Our mission is to utilize the untapped potential of quantum computing to revolutionize the concept of matchmaking. We aim to create deeply compatible connections through a scientific and innovative approach.
        </p>
        <h2 className="text-3xl font-semibold mb-3">How It Works</h2>
        <ol className="list-decimal list-outside ml-4 mb-4 text-lg">
          <li>
            Users fill out a detailed Google Form about their interests, preferences, and what they're looking for in a match.
          </li>
          <li>
            We express the collected data as a quadratic programming problem, encapsulating the complex nature of human compatibility into a mathematical model.
          </li>
          <li>
            This model is then converted into a Quadratic Unconstrained Binary Optimization (QUBO) problem, making it suitable for processing with quantum algorithms.
          </li>
          <li>
            We employ the Quantum Approximate Optimization Algorithm (QAOA) to solve this problem, leveraging the power of quantum computing to find optimal matches.
          </li>
        </ol>
        <p className="mb-4 text-lg">
          This cutting-edge approach not only sets a new standard for matchmaking but also showcases the practical applications of quantum computing in everyday life.
        </p>
        <h2 className="text-3xl font-semibold mb-3">Join Us</h2>
        <p className="text-lg">
          Become part of a revolutionary journey at the intersection of technology, science, and human connections. Discover your quantum match with MITqute.
        </p>
        <h2 className="text-3xl font-semibold mb-3">The Team</h2>
        <p className="mb-4 text-lg">
          MITqute was brought to life by a team of passionate individuals from MIT, dedicated to exploring the frontiers of quantum computing and matchmaking:
        </p>
        <ul className="list-disc list-outside ml-4 mb-4 text-lg">
          <li>Liam Kronman</li>
          <li>Maggie Bao</li>
          <li>Nicole Shen</li>
          <li>Armin Ulrich</li>
          <li>Sierra Romo</li>
        </ul>

        <h2 className="text-3xl font-semibold mb-3">Explore Our Work</h2>
        <p className="text-lg mb-4">
          Dive deeper into the quantum mechanics of love and explore the code behind MITqute on our GitHub repository.
        </p>
        <a
          href="https://github.com/grid-rider/team-7-iQuHACK"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:text-blue-300 transition duration-300 ease-in-out"
        >
          Visit our GitHub
        </a>
      </div>
    </div>
  );
};

export default About;