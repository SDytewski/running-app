import './index.css'
import './globals.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import CardSection from './components/CardSection'
import CTASection from './components/CTASection'
import Footer from './components/Footer'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      <Navbar />
      {/* <Hero />
      <CardSection />
      <CTASection />
      <Footer /> */}
    </div>
  )
}
