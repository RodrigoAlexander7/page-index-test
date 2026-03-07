import json
from typing import Dict, List
from core.client import gemini_client
from repositories.tree_repository import TreeRepository
from api.models import NodeInfo


class QuechuaService:
    """Service layer for answering questions about Quechua language"""
    
    def __init__(self, repository: TreeRepository):
        self.repository = repository
        self.gemini_client = gemini_client
    
    async def answer_question(self, question: str) -> Dict:
        """
        Answer a question using tree search and LLM generation
        Returns dict with answer, reasoning, and nodes used
        """
        # Step 1: Tree search to find relevant nodes
        search_result = await self._search_trees(question)
        
        # Step 2: Extract context from relevant nodes
        context = self._extract_context(
            search_result["quechua_nodes"],
            search_result["gramar_nodes"]
        )
        
        # Step 3: Generate answer using context
        answer = await self._generate_answer(question, context)
        
        # Step 4: Build response with metadata
        nodes_info = self._build_nodes_info(
            search_result["quechua_nodes"],
            search_result["gramar_nodes"]
        )
        
        return {
            "answer": answer,
            "reasoning": search_result["thinking"],
            "nodes_used": nodes_info
        }
    
    async def _search_trees(self, question: str) -> Dict:
        """Search both trees for relevant nodes using LLM"""
        # Get trees without text for the prompt
        quechua_tree_clean = self.repository.get_tree_without_text(
            self.repository.quechua_tree
        )
        gramar_tree_clean = self.repository.get_tree_without_text(
            self.repository.gramar_tree
        )
        
        search_prompt = f"""
You are given a question and two tree structures from different documents about Quechua language.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes from BOTH documents that are likely to contain the answer to the question.

Question: {question}

Document 1 - Quechua Grammar tree structure:
{json.dumps(quechua_tree_clean, indent=2)}

Document 2 - Gramar tree structure:
{json.dumps(gramar_tree_clean, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process on which nodes from both documents are relevant to the question>",
    "quechua_nodes": ["node_id_1", "node_id_2", ...],
    "gramar_nodes": ["node_id_1", "node_id_2", ...]
}}
Directly return the final JSON structure. Do not output anything else.
"""
        
        result_text = await self.gemini_client.generate_text(search_prompt)
        return json.loads(result_text)
    
    def _extract_context(self, quechua_nodes: List[str], gramar_nodes: List[str]) -> str:
        """Extract and combine text from relevant nodes"""
        quechua_content = self.repository.get_nodes_text(quechua_nodes, "quechua")
        gramar_content = self.repository.get_nodes_text(gramar_nodes, "gramar")
        
        combined_content = f"""
=== Context from Quechua Grammar Document ===
{quechua_content}

=== Context from Gramar Document ===
{gramar_content}
"""
        return combined_content
    
    async def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM with provided context"""
        answer_prompt = f"""
Answer the question based on the context from both documents:

Question: {question}

Context: {context}

Provide a clear, accurate answer based only on the context provided.
Include explanations of the grammatical structures used when relevant.
"""
        
        return await self.gemini_client.generate_text(answer_prompt)
    
    def _build_nodes_info(self, quechua_nodes: List[str], gramar_nodes: List[str]) -> List[NodeInfo]:
        """Build list of NodeInfo objects for response"""
        nodes_info = []
        
        for node_id in quechua_nodes:
            node = self.repository.get_node(node_id, "quechua")
            if node:
                nodes_info.append(NodeInfo(
                    node_id=node["node_id"],
                    page_index=node.get("page_index", 0),
                    title=node.get("title", ""),
                    source="quechua"
                ))
        
        for node_id in gramar_nodes:
            node = self.repository.get_node(node_id, "gramar")
            if node:
                nodes_info.append(NodeInfo(
                    node_id=node["node_id"],
                    page_index=node.get("page_index", 0),
                    title=node.get("title", ""),
                    source="gramar"
                ))
        
        return nodes_info
