import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-green-600 flex flex-col items-center justify-center text-white">
      {/* Logo section */}
      <div className="flex gap-6 mb-8">
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="w-24 h-24" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="w-24 h-24" alt="React logo" />
        </a>
      </div>

      {/* Main heading */}
      <h1 className="text-5xl font-bold mb-6">Vite + React + Tailwind</h1>

      {/* Counter card */}
      <div className="bg-white text-black rounded-xl p-6 shadow-md mb-6">
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          onClick={() => setCount((count) => count + 1)}
        >
          count is {count}
        </button>
        <p className="mt-4">
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      {/* Footer */}
      <p className="text-white/80">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  )
}

export default App
