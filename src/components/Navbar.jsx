import React, { useState } from "react";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  const navLinks = ["Home", "About", "Features", "Contact"];

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <span className="text-xl font-bold text-blue-600">RunningApp</span>
          </div>
          <div className="hidden md:flex space-x-6 items-center">
            {navLinks.map((link) => (
              <a
                key={link}
                href="#"
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
              >
                {link}
              </a>
            ))}
            <button className="ml-4 px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
              Sign In
            </button>
          </div>
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setOpen(!open)}
              className="text-gray-700 focus:outline-none"
            >
              {open ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {open && (
        <div className="md:hidden bg-white shadow-md">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navLinks.map((link) => (
              <a
                key={link}
                href="#"
                className="block text-gray-700 hover:text-blue-600 px-3 py-2 rounded font-medium transition-colors"
              >
                {link}
              </a>
            ))}
            <button className="w-full px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
              Sign In
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
