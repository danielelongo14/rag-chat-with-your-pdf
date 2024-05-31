import Head from 'next/head';
import UploadForm from '../components/UploadForm';
import ChatForm from '../components/ChatForm';

export default function Home() {
  return (
    <div className="bg-gradient-to-r from-blue-100 to-purple-200 min-h-screen p-4">
      <Head>
        <title>Document Chat Interface</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-4xl font-extrabold text-center text-gray-800 mb-6">
          Upload Document and Chat
        </h1>
        <div className="flex flex-col items-center space-y-6">
          <UploadForm />
          <ChatForm />
        </div>
      </main>
    </div>
  );
}
