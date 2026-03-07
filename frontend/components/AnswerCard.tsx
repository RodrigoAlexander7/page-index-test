'use client';

import { AnswerResponse } from '@/lib/types';
import SourceCard from './SourceCard';

interface AnswerCardProps {
  answer: AnswerResponse;
}

export default function AnswerCard({ answer }: AnswerCardProps) {
  return (
    <div className="w-full space-y-6 bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      {/* Answer Section */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Respuesta</h3>
        <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
          {answer.answer}
        </div>
      </div>

      {/* Reasoning Section */}
      {answer.reasoning && (
        <div className="border-t border-gray-200 pt-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Proceso de búsqueda</h3>
          <div className="text-sm text-gray-600 whitespace-pre-wrap bg-gray-50 p-4 rounded">
            {answer.reasoning}
          </div>
        </div>
      )}

      {/* Sources Section */}
      {answer.nodes_used && answer.nodes_used.length > 0 && (
        <div className="border-t border-gray-200 pt-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Fuentes consultadas ({answer.nodes_used.length})
          </h3>
          <div className="space-y-2">
            {answer.nodes_used.map((node, index) => (
              <SourceCard key={`${node.node_id}-${index}`} node={node} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
