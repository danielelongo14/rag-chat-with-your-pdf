import { useState } from 'react';

export default function ChatForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const res = await fetch('http://localhost:8000/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const result = await res.json();
      setResponse(result.response);
    } catch (error) {
      console.error('Error sending chat message:', error);
      alert('Failed to send message.');
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-gray-700">Chat with Document</h2>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows="4"
          className="border border-gray-300 p-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button type="submit" className="bg-gradient-to-r from-blue-500 to-purple-500 text-white p-2 rounded-lg hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          Send
        </button>
      </form>
      {response && (
        <div className="mt-4 p-4 bg-gray-50 border border-gray-300 rounded-lg">
          {response}
        </div>
      )}
    </div>
  );
}
