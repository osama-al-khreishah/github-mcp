# Utility function to extract text between two substrings

def extract_between(text: str, start: str, end: str) -> str:
    start_idx = text.find(start)
    if start_idx == -1:
        return ""
    start_idx += len(start)
    end_idx = text.find(end, start_idx)
    if end_idx == -1:
        return text[start_idx:].strip()
    return text[start_idx:end_idx].strip()

# Utility function to extract text after a substring

def extract_after(text: str, start: str) -> str:
    start_idx = text.find(start)
    if start_idx == -1:
        return ""
    return text[start_idx + len(start):].strip()
#------------------------------------------