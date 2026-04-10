import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";

export default function Features() {
  const [runs, setRuns] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function fetchRuns() {
      const { data, error } = await supabase
        .from("runs")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) {
        setErrorMessage(error.message);
        return;
      }

      setRuns(data);
    }

    fetchRuns();
  }, []);

  return (
    <section id="features" className="min-h-screen p-8">
      <h2 className="text-2xl font-bold text-gray-800">Features</h2>

      {errorMessage && (
        <p className="mt-4 text-red-600">{errorMessage}</p>
      )}

      {!errorMessage && (
        <div className="mt-6 space-y-3">
          {runs.length === 0 ? (
            <p className="text-gray-600">No runs yet.</p>
          ) : (
            runs.map((run) => (
              <div key={run.id} className="rounded border bg-white p-4 shadow-sm">
                <h3 className="font-semibold text-gray-800">{run.title}</h3>
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
