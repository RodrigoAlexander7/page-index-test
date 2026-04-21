'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';
import { AnswerResponse } from '@/lib/types';
import QuestionInput from '@/components/QuestionInput';
import AnswerCard from '@/components/AnswerCard';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorMessage from '@/components/ErrorMessage';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<AnswerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const result = await apiClient.askQuestion(question);
      setAnswer(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al obtener respuesta');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    handleSubmit();
  };

  const exampleQuestions = [
    "¿Cuáles son las reglas de formación de plural en quechua?",
    "¿Cómo se forman los verbos en tiempo presente?",
    "¿Qué son los sufijos en quechua?",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Quechua Q&A
          </h1>
          <p className="text-lg text-gray-600">
            Pregunta sobre gramática, vocabulario y estructura del idioma quechua
          </p>
        </div>

        {/* Question Input */}
        <div className="mb-8">
          <QuestionInput
            value={question}
            onChange={setQuestion}
            onSubmit={handleSubmit}
            disabled={loading}
          />
        </div>

        {/* Example Questions */}
        {!answer && !loading && !error && (
          <div className="mb-8">
            <h2 className="text-sm font-medium text-gray-700 mb-3">
              Preguntas de ejemplo:
            </h2>
            <div className="flex flex-wrap gap-2">
              {exampleQuestions.map((q, index) => (
                <button
                  key={index}
                  onClick={() => setQuestion(q)}
                  className="text-sm px-4 py-2 bg-white border border-gray-300 rounded-full hover:bg-gray-50 transition-colors text-gray-700"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Error State */}
        {error && <ErrorMessage message={error} onRetry={handleRetry} />}

        {/* Answer Display */}
        {answer && !loading && <AnswerCard answer={answer} />}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>Made with &lt;3 for Quechua Learners!</p>
        </div>
      </footer>
    </div>
  );
}
