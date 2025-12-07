import { useEffect, useRef, useState } from 'react';

export default function Transcribe() {
  const [supported, setSupported] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      setSupported(true);
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.onresult = (event: any) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const res = event.results[i];
          if (res.isFinal) {
            setTranscript((prev) => prev + ' ' + res[0].transcript);
          } else {
            interim += res[0].transcript;
          }
        }
        if (interim) setTranscript((prev) => prev + ' ' + interim);
      };
      recognitionRef.current = recognition;
    }
  }, []);

  const toggle = () => {
    if (!recognitionRef.current) return;
    if (recognitionRef.current.listening) {
      recognitionRef.current.stop();
      recognitionRef.current.listening = false;
    } else {
      recognitionRef.current.start();
      recognitionRef.current.listening = true;
    }
  };

  const save = async () => {
    await fetch('/api/transcripts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: 'Live sermon', text: transcript }) });
    alert('Saved transcript');
  };

  return (
    <div className="space-y-4">
      <div className="card space-y-2">
        <h1 className="text-xl font-semibold">Live Transcribe</h1>
        {supported ? (
          <div className="space-x-2">
            <button className="bg-indigo-600 text-white px-3 py-2 rounded" onClick={toggle}>
              Start / Stop
            </button>
            <button className="bg-green-600 text-white px-3 py-2 rounded" onClick={save}>
              Save Transcript
            </button>
          </div>
        ) : (
          <p className="text-sm text-gray-600">Web Speech API not supported; upload audio below.</p>
        )}
        <textarea className="w-full border rounded p-2" rows={6} value={transcript} onChange={(e) => setTranscript(e.target.value)}></textarea>
      </div>

      <div className="card">
        <h2 className="font-semibold mb-2">Upload audio (fallback)</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const formData = new FormData(e.currentTarget as HTMLFormElement);
            await fetch('/api/transcripts/upload', { method: 'POST', body: formData });
            alert('Upload queued');
          }}
        >
          <input name="title" className="border rounded px-3 py-2 w-full mb-2" placeholder="Title" />
          <input name="speaker" className="border rounded px-3 py-2 w-full mb-2" placeholder="Speaker" />
          <input name="audio" type="file" accept="audio/*" className="mb-2" />
          <button className="bg-indigo-600 text-white px-3 py-2 rounded" type="submit">
            Upload
          </button>
        </form>
      </div>
    </div>
  );
}
