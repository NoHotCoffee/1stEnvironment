import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Bible from './pages/Bible';
import Lexicon from './pages/Lexicon';
import Transcribe from './pages/Transcribe';
import Devotional from './pages/Devotional';
import Apologetics from './pages/Apologetics';
import './App.css';

function App() {
  return (
    <div className="min-h-screen text-gray-900">
      <header className="bg-white shadow sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-indigo-700">
            Scripture Studio
          </Link>
          <nav className="space-x-4 text-sm font-medium">
            <Link to="/bible/John/3/16">Bible</Link>
            <Link to="/lexicon">Lexicon</Link>
            <Link to="/transcribe">Live Transcribe</Link>
            <Link to="/devotional">Devotional</Link>
            <Link to="/apologetics">Apologetics Lab</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/bible/:book/:chapter/:verse" element={<Bible />} />
          <Route path="/lexicon" element={<Lexicon />} />
          <Route path="/transcribe" element={<Transcribe />} />
          <Route path="/devotional" element={<Devotional />} />
          <Route path="/apologetics" element={<Apologetics />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
