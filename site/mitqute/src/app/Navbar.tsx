import React from 'react';
import Link from 'next/link';

const Navbar: React.FC = () => {
  return (
    <nav className="flex justify-between items-center px-8 py-4 bg-gray-800 text-white w-full fixed top-0 left-0">
      <Link href="/" className="font-honk text-xl">
        {/* <a className="text-xl font-bold">MITqute 🌌</a> */}
        MITqute
      </Link>
      <div className="flex gap-4">
        {/* <Link href="/">
          <a className="hover:text-gray-300">Home</a>
        </Link> */}
        <Link href="/about">
            About
          {/* <a className="hover:text-gray-300">About</a> */}
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
