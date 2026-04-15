import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

const emptyForm = {
  runnerName: "",
  runDate: "",
  title: "",
  distanceMiles: "",
  notes: "",
};

export default function Features() {
  const [runs, setRuns] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchRuns();
  }, []);

  async function fetchRuns() {
    const { data, error } = await supabase
      .from("runs")
      .select("*")
      .order("run_date", { ascending: false })
      .order("created_at", { ascending: false });

    if (error) {
      setErrorMessage(error.message);
      return;
    }

    setRuns(data);
  }

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");
    setIsSubmitting(true);

    const { error } = await supabase.from("runs").insert([
      {
        runner_name: form.runnerName.trim(),
        run_date: form.runDate || null,
        title: form.title.trim(),
        distance_miles: Number(form.distanceMiles),
        notes: form.notes.trim(),
      },
    ]);

    if (error) {
      setErrorMessage(error.message);
      setIsSubmitting(false);
      return;
    }

    setForm(emptyForm);
    setSuccessMessage("Run saved.");
    await fetchRuns();
    setIsSubmitting(false);
  }

  return (
    <section id="features" className="min-h-screen p-8">
      <h2 className="text-2xl font-bold text-gray-800">Features</h2>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4 rounded-xl border bg-white p-6 shadow-sm"
      >
        <div>
          <label
            htmlFor="runnerName"
            className="block text-sm font-medium text-gray-700"
          >
            Runner name
          </label>
          <input
            id="runnerName"
            name="runnerName"
            type="text"
            value={form.runnerName}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Jordan"
            required
          />
        </div>

        <div>
          <label
            htmlFor="runDate"
            className="block text-sm font-medium text-gray-700"
          >
            Run date
          </label>
          <input
            id="runDate"
            name="runDate"
            type="date"
            value={form.runDate}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            required
          />
        </div>

        <div>
          <label
            htmlFor="title"
            className="block text-sm font-medium text-gray-700"
          >
            Title
          </label>
          <input
            id="title"
            name="title"
            type="text"
            value={form.title}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Morning Run"
            required
          />
        </div>

        <div>
          <label
            htmlFor="distanceMiles"
            className="block text-sm font-medium text-gray-700"
          >
            Distance (miles)
          </label>
          <input
            id="distanceMiles"
            name="distanceMiles"
            type="number"
            step="0.01"
            min="0"
            value={form.distanceMiles}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="3.50"
            required
          />
        </div>

        <div>
          <label
            htmlFor="notes"
            className="block text-sm font-medium text-gray-700"
          >
            Notes
          </label>
          <textarea
            id="notes"
            name="notes"
            value={form.notes}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            placeholder="Easy pace around the neighborhood."
            rows="4"
          />
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Saving..." : "Save run"}
        </button>
      </form>

      {errorMessage && (
        <p className="mt-4 text-red-600">{errorMessage}</p>
      )}

      {successMessage && (
        <p className="mt-4 text-green-600">{successMessage}</p>
      )}

      {!errorMessage && (
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
      )}
    </section>
  );
}
