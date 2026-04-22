import re

def clean_text(s: str) -> str:
    """Collapse repeated whitespace and trim both ends."""
    return re.sub(r"\s+", " ", str(s)).strip()

def normalize_value(raw: str | None) -> str | None:
    """
    Clean a scraped field value and remove leading ':' if present.

    Example:
        ': [[malam02]]' -> '[[malam02]]'
        ': Integrated Science Center 3373' -> 'Integrated Science Center 3373'
    """
    if raw is None:
        return None

    raw = clean_text(raw)
    raw = re.sub(r"^:\s*", "", raw).strip()
    return raw if raw else None

def parse_email(raw: str | None) -> str | None:
    """
    Convert page-specific email placeholders into full wm.edu emails.

    Examples:
        [[malam02]] -> malam02@wm.edu
        [[w|hchen23]] -> hchen23@wm.edu
    """
    raw = normalize_value(raw)
    if raw is None:
        return None

    simple_match = re.fullmatch(r"\[\[([A-Za-z0-9._-]+)\]\]", raw)
    if simple_match:
        return f"{simple_match.group(1)}@wm.edu"

    pipe_match = re.fullmatch(r"\[\[[A-Za-z]+\|([A-Za-z0-9._-]+)\]\]", raw)
    if pipe_match:
        return f"{pipe_match.group(1)}@wm.edu"

    return raw

def parse_webpage(raw: str | None) -> str | None:
    """
    Extract the URL from page-specific webpage placeholders.

    Example:
        {{https://haipeng-chen.github.io/, Personal Website}}
        -> https://haipeng-chen.github.io/
    """
    raw = normalize_value(raw)
    if raw is None:
        return None

    match = re.fullmatch(r"\{\{([^,}]+),\s*[^}]+\}\}", raw)
    if match:
        return match.group(1).strip()

    return raw

def fix_name(name: str) -> str:
    """
    Fix the name format from "Last, First" to "First Last" for better search results in Semantic Scholar.
        Args:
            name (str): The name in "Last, First" format.
    """
    if "," in name:
        last, first = name.split(",", 1)
        return first.strip() + " " + last.strip()
    return name