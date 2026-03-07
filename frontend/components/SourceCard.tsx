'use client';

import { NodeInfo } from '@/lib/types';

interface SourceCardProps {
  node: NodeInfo;
}

export default function SourceCard({ node }: SourceCardProps) {
  const sourceColor = node.source === 'quechua' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800';

  return (
    <div className="flex items-center gap-3 p-3 bg-gray-50 rounded border border-gray-200 hover:bg-gray-100 transition-colors">
      <span className={`px-2 py-1 text-xs font-medium rounded ${sourceColor}`}>
        {node.source}
      </span>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">{node.title}</p>
        <p className="text-xs text-gray-500">Página {node.page_index}</p>
      </div>
    </div>
  );
}
