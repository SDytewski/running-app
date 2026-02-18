
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <main className="p-8">
        <h1 className="text-3xl font-bold text-gray-800">Welcome to Running App</h1>
        <p className="mt-4 text-gray-600">
          This is a modern Tailwind-styled React app.
        </p>
      </main>
    </div>
  );
}
