import Navbar from "./components/Navbar";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="p-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome to Running App
        </h1>
        <p className="mt-4 text-gray-600">
          Your modern sports tracking app.
        </p>
      </main>
    </div>
  );
}
