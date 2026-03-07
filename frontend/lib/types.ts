// API Types
export interface QuestionRequest {
  question: string;
}

export interface NodeInfo {
  node_id: string;
  page_index: number;
  title: string;
  source: string;
}

export interface AnswerResponse {
  answer: string;
  reasoning: string;
  nodes_used: NodeInfo[];
}

export interface HealthResponse {
  status: string;
  message: string;
}
