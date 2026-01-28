import sys
from pathlib import Path

# Using the root directory to ensure imports work correctly
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from core.config import settings
from core.client import gemini_client, pi_client

pdf_path = root_dir / "data/raw_files" / "quechua_grammar.pdf"
doc_id = pi_client.submit_document(str(pdf_path))["doc_id"]
print('Document Submitted:', doc_id)