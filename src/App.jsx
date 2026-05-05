
import { useState } from "react";
import Navbar from "./components/Navbar";
import Features from "./components/Features";
import Signin from "./components/Signin";

export default function App() {
  const [showSignIn, setShowSignIn] = useState(false);
  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <main className="p-8">
        <h1 className="text-3xl font-bold text-gray-800">Welcome to Running App</h1>
        <p className="mt-4 text-gray-600">
          This is a modern Tailwind-styled React app.
        </p>
      </main>
      <Features />
    </div>
  );
}
