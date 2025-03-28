import React, { useState } from 'react';
import { Download, CheckCircle, Loader2 } from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleDownload = () => {
    setIsLoading(true);
    // Simulate progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsLoading(false);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-6xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl mb-8">
            Baixe seus vídeos em{' '}
            <span className="text-indigo-600">segundos</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Chega de esperar! Nossa plataforma oferece downloads rápidos e seguros para seus vídeos favoritos.
          </p>
        </div>

        {/* Download Form */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="flex flex-col md:flex-row gap-4">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Cole a URL do vídeo aqui"
                className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                onKeyPress={(e) => e.key === 'Enter' && handleDownload()}
              />
              <button
                onClick={handleDownload}
                disabled={isLoading || !url}
                className={`flex items-center justify-center px-6 py-3 rounded-lg text-white font-medium transition-colors ${
                  isLoading || !url
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-700'
                }`}
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                ) : (
                  <Download className="w-5 h-5 mr-2" />
                )}
                Baixar
              </button>
            </div>

            {/* Progress Bar */}
            {isLoading && (
              <div className="mt-6">
                <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-indigo-600 h-full transition-all duration-500 ease-out"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="flex items-center justify-between mt-2 text-sm text-gray-600">
                  <span>Baixando...</span>
                  <span>{progress}%</span>
                </div>
              </div>
            )}

            {progress === 100 && !isLoading && (
              <div className="mt-6 flex items-center justify-center text-green-600">
                <CheckCircle className="w-5 h-5 mr-2" />
                <span>Download concluído com sucesso!</span>
              </div>
            )}
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full p-3 w-12 h-12 flex items-center justify-center mx-auto mb-4">
                <Download className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Download Rápido</h3>
              <p className="text-gray-600">Baixe seus vídeos em alta velocidade</p>
            </div>
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full p-3 w-12 h-12 flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Alta Qualidade</h3>
              <p className="text-gray-600">Mantenha a qualidade original dos vídeos</p>
            </div>
            <div className="text-center">
              <div className="bg-indigo-100 rounded-full p-3 w-12 h-12 flex items-center justify-center mx-auto mb-4">
                <Loader2 className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Processo Simples</h3>
              <p className="text-gray-600">Interface intuitiva e fácil de usar</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;