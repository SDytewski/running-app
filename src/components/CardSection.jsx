export default function CardSection() {
  return (
    <section className="grid md:grid-cols-3 gap-8 px-6 py-12 md:px-20">
      <div className="bg-white rounded-lg shadow p-6 text-center hover:shadow-lg transition">
        <h2 className="text-xl font-bold mb-2">Teams</h2>
        <p>Check your favorite teams, rosters, and news updates.</p>
      </div>
      <div className="bg-white rounded-lg shadow p-6 text-center hover:shadow-lg transition">
        <h2 className="text-xl font-bold mb-2">Schedules</h2>
        <p>Never miss a game with our up-to-date match schedules.</p>
      </div>
      <div className="bg-white rounded-lg shadow p-6 text-center hover:shadow-lg transition">
        <h2 className="text-xl font-bold mb-2">Stats</h2>
        <p>Get live stats, scores, and analytics for all matches.</p>
      </div>
    </section>
  )
}
