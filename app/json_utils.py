import json
import re
from typing import Dict, Any

def clean_json(text: str) -> str:
    cleaned = re.sub(r"```json\s*", "", text)
    cleaned = re.sub(r"```\s*", "", cleaned)
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    if start != -1 and end != -1:
        cleaned = cleaned[start:end+1]
    return cleaned.strip()

def safe_parse_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(clean_json(text))
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON")
