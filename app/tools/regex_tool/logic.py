"""
DevTools Desktop — Regex Logic
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class RegexMatchInfo:
    full_match: str
    start: int
    end: int
    groups: List[str]
    named_groups: Dict[str, str]

@dataclass
class RegexResult:
    success: bool
    matches: List[RegexMatchInfo] = None
    error_message: str = ""
    error_detail: str = ""
    replacement: str = ""

def test_regex(pattern: str, text: str, flags: int = 0, replace_pattern: str = "") -> RegexResult:
    if not pattern:
        return RegexResult(True, matches=[])
        
    try:
        # Use a timeout wrapper if we wanted to prevent catastrophic backtracking,
        # but standard `re` module doesn't natively support timeouts.
        # For simplicity and standard usage, we just use standard `re`.
        compiled = re.compile(pattern, flags)
        
        matches = []
        for m in compiled.finditer(text):
            groups = [m.group(i) for i in range(1, compiled.groups + 1)]
            named_groups = m.groupdict()
            matches.append(RegexMatchInfo(
                full_match=m.group(0),
                start=m.start(),
                end=m.end(),
                groups=groups,
                named_groups=named_groups
            ))
            
            # Limit number of matches to prevent memory issues on crazy inputs
            if len(matches) > 1000:
                break
                
        replacement = ""
        if replace_pattern:
            replacement = compiled.sub(replace_pattern, text)
            
        return RegexResult(success=True, matches=matches, replacement=replacement)
        
    except re.error as e:
        return RegexResult(success=False, error_message="Invalid regular expression", error_detail=str(e))
    except Exception as e:
        return RegexResult(success=False, error_message="Error processing regex", error_detail=str(e))
