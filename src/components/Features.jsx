import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

export default function Features() {
  const [runnerName, setRunnerName] = useState("");
  const [runDate, setRunDate] = useState("");
  const [title, setTitle] = useState("");
  const [distanceMiles, setDistanceMiles] = useState("");
  const [notes, setNotes] = useState("");

  const [runs, setRuns] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getRuns();
  }, []);

  async function getRuns() {
    const result = await supabase
      .from("runs")
      .select("*")
      .order("run_date", { ascending: false })
      .order("created_at", { ascending: false });

    if (result.error) {
      setMessage("Could not load runs.");
      return;
    }

    setRuns(result.data || []);
  }

  async function saveRun(event) {
    event.preventDefault();
    setMessage("");

    const result = await supabase.from("runs").insert([
      {
        runner_name: runnerName.trim(),
        run_date: runDate,
        title: title.trim(),
        distance_miles: Number(distanceMiles),
        notes: notes.trim(),
      },
    ]);

    if (result.error) {
      setMessage("Could not save run.");
      return;
    }

    setMessage("Run saved!");

    setRunnerName("");
    setRunDate("");
    setTitle("");
    setDistanceMiles("");
    setNotes("");

    getRuns();
  }

  return (
    <section id="features" className="min-h-screen p-8">
      <h2 className="text-2xl font-bold text-gray-800">Features</h2>

      <form
        onSubmit={saveRun}
        className="mt-6 space-y-4 rounded-xl border bg-white p-6 shadow-sm"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Runner name
          </label>
          <input
            type="text"
            value={runnerName}
            onChange={(event) => setRunnerName(event.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Jordan"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Run date
          </label>
          <input
            type="date"
            value={runDate}
            onChange={(event) => setRunDate(event.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Morning Run"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Distance (miles)
          </label>
          <input
            type="number"
            value={distanceMiles}
            onChange={(event) => setDistanceMiles(event.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="3.50"
            step="0.01"
            min="0"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Notes
          </label>
          <textarea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Easy pace around the neighborhood."
            rows="4"
          />
        </div>

        <button
          type="submit"
          className="rounded-md bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
        >
          Save run
        </button>
      </form>

      {message && <p className="mt-4 text-green-600">{message}</p>}

      <div className="mt-6 space-y-3">
        {runs.length === 0 ? (
          <p className="text-gray-600">No runs yet.</p>
        ) : (
          runs.map((run) => (
            <div key={run.id} className="rounded border bg-white p-4 shadow-sm">
              <h3 className="font-semibold text-gray-800">{run.title}</h3>
              <p className="mt-1 text-sm text-gray-500">
                {run.runner_name || "Unknown runner"}
                {run.run_date ? ` on ${run.run_date}` : ""}
              </p>
              <p className="text-gray-600">{run.distance_miles} miles</p>
              {run.notes && (
                <p className="mt-2 text-sm text-gray-500">{run.notes}</p>
              )}
            </div>
          ))
        )}
      </div>
    </section>
  );
}
