import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-2xl font-bold mb-2">Welcome to Scripture Studio</h1>
        <p className="text-gray-700">
          Explore Scripture with interlinked lexicon references, live sermon transcription, AI devotionals, historical study notes,
          and apologetics training tools.
        </p>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        <Feature title="Bible Viewer" description="Navigate per verse with Strong's inline links" to="/bible/John/3/16" />
        <Feature title="Lexicon" description="Tap Strong's numbers for Hebrew/Greek insight" to="/lexicon" />
        <Feature title="Live Transcribe" description="Capture sermons with Web Speech API or uploads" to="/transcribe" />
        <Feature title="Devotionals" description="Generate AI devotionals by verse" to="/devotional" />
        <Feature title="Apologetics Lab" description="Lessons, quizzes, and debate simulator" to="/apologetics" />
      </div>
    </div>
  );
}

function Feature({ title, description, to }: { title: string; description: string; to: string }) {
  return (
    <Link to={to} className="card hover:shadow-md transition block h-full">
      <h3 className="font-semibold text-lg mb-1">{title}</h3>
      <p className="text-gray-600 text-sm">{description}</p>
    </Link>
  );
}
