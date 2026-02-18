import { useState } from "react";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const links = ["Home", "Teams", "Schedule", "Stats"];

  return (
    <nav className="bg-[#FF4500] text-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="text-2xl font-extrabold tracking-tight">
            Running App
          </div>

          {/* Desktop Menu */}
          <ul className="hidden md:flex space-x-6 text-lg font-medium">
            {links.map((link) => (
              <li key={link}>
                <a
                  href="#"
                  className="px-3 py-2 rounded-md hover:bg-white/20 transition-colors"
                >
                  {link}
                </a>
              </li>
            ))}
          </ul>

          {/* Mobile Hamburger */}
          <div className="md:hidden">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-3xl focus:outline-none hover:text-orange-200 transition-colors"
            >
              {menuOpen ? "✕" : "☰"}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <ul className="md:hidden mt-2 bg-[#FF4500] rounded-lg shadow-lg py-2 space-y-2">
            {links.map((link) => (
              <li key={link}>
                <a
                  href="#"
                  className="block px-4 py-2 rounded-md hover:bg-orange-600 transition-colors"
                  onClick={() => setMenuOpen(false)}
                >
                  {link}
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </nav>
  );
}
