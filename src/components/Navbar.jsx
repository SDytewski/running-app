export default function Navbar() {
  return (
    <nav className="bg-[#FF4500] text-white px-6 py-4 flex justify-between items-center">
      <div className="text-2xl font-bold">Sportify</div>
      <ul className="hidden md:flex space-x-6">
        <li><a href="#" className="hover:underline">Home</a></li>
        <li><a href="#" className="hover:underline">Teams</a></li>
        <li><a href="#" className="hover:underline">Schedule</a></li>
        <li><a href="#" className="hover:underline">Stats</a></li>
        <li><a href="#" className="hover:underline">Contact</a></li>
      </ul>
      <div className="md:hidden">
        <button className="text-white">&#9776;</button>
      </div>
    </nav>
  )
}
