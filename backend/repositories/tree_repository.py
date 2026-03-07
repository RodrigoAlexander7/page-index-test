import json
from pathlib import Path
from typing import Dict, List, Any


class TreeRepository:
    """Repository for loading and accessing tree data from JSON files"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.quechua_tree: List[Dict[str, Any]] = []
        self.gramar_tree: List[Dict[str, Any]] = []
        self.quechua_node_map: Dict[str, Dict[str, Any]] = {}
        self.gramar_node_map: Dict[str, Dict[str, Any]] = {}
        self._load_trees()
    
    def _load_trees(self) -> None:
        """Load both tree JSON files and create node mappings"""
        quechua_path = self.data_dir / "quechua_tree.json"
        gramar_path = self.data_dir / "gramar_tree.json"
        
        if not quechua_path.exists():
            raise FileNotFoundError(f"Quechua tree file not found: {quechua_path}")
        if not gramar_path.exists():
            raise FileNotFoundError(f"Gramar tree file not found: {gramar_path}")
        
        with open(quechua_path, 'r', encoding='utf-8') as f:
            self.quechua_tree = json.load(f)
        
        with open(gramar_path, 'r', encoding='utf-8') as f:
            self.gramar_tree = json.load(f)
        
        # Create node mappings for quick access
        self.quechua_node_map = self._create_node_mapping(self.quechua_tree)
        self.gramar_node_map = self._create_node_mapping(self.gramar_tree)
    
    def _create_node_mapping(self, tree: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Create a dictionary mapping node_id to node data"""
        node_map = {}
        
        def traverse(nodes: List[Dict[str, Any]]) -> None:
            for node in nodes:
                node_map[node['node_id']] = node
                if 'children' in node:
                    traverse(node['children'])
        
        traverse(tree)
        return node_map
    
    def get_tree_without_text(self, tree: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return a copy of the tree without 'text' field for prompts"""
        return self._remove_fields(tree, ['text'])
    
    def _remove_fields(self, tree: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
        """Remove specified fields from tree nodes"""
        import copy
        tree_copy = copy.deepcopy(tree)
        
        def remove_recursive(nodes: List[Dict[str, Any]]) -> None:
            for node in nodes:
                for field in fields:
                    node.pop(field, None)
                if 'children' in node:
                    remove_recursive(node['children'])
        
        remove_recursive(tree_copy)
        return tree_copy
    
    def get_node(self, node_id: str, source: str) -> Dict[str, Any]:
        """Get a specific node by ID from specified source"""
        node_map = self.quechua_node_map if source == "quechua" else self.gramar_node_map
        return node_map.get(node_id, {})
    
    def get_nodes_text(self, node_ids: List[str], source: str) -> str:
        """Extract and concatenate text from specified nodes"""
        node_map = self.quechua_node_map if source == "quechua" else self.gramar_node_map
        texts = [node_map[node_id].get("text", "") for node_id in node_ids if node_id in node_map]
        return "\n\n".join(texts)
