"""
DevTools Desktop — SQL Logic
"""

import re
from dataclasses import dataclass

@dataclass
class SqlResult:
    success: bool
    output: str = ""
    error_message: str = ""

def format_sql(sql: str) -> SqlResult:
    if not sql.strip():
        return SqlResult(False, error_message="No SQL input provided.")
        
    try:
        # A very basic but functional SQL formatter since we avoid heavy external dependencies.
        # This covers standard formatting requirements.
        
        # 1. Standardize whitespace
        text = re.sub(r'\s+', ' ', sql.strip())
        
        # 2. Add newlines before major keywords
        major_keywords = [
            'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING',
            'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN', 'JOIN',
            'INSERT INTO', 'UPDATE', 'DELETE FROM', 'VALUES', 'SET',
            'UNION ALL', 'UNION', 'LIMIT', 'OFFSET'
        ]
        
        for kw in major_keywords:
            text = re.sub(r'(?i)\b' + kw.replace(' ', r'\s+') + r'\b', f'\n{kw.upper()}', text)
            
        # 3. Handle commas (newline after comma in SELECT/GROUP BY/ORDER BY)
        text = re.sub(r',', ',\n    ', text)
        
        # 4. Handle AND/OR in WHERE clauses
        text = re.sub(r'(?i)\b(AND|OR)\b', r'\n  \1', text)
        
        # Clean up multiple newlines and spaces
        text = re.sub(r'\n\s*\n', '\n', text)
        lines = [line.rstrip() for line in text.split('\n') if line.strip()]
        
        # Further refine indentation (simple heuristic)
        formatted_lines = []
        indent_level = 0
        for line in lines:
            line_upper = line.upper().lstrip()
            if line_upper.startswith(')') or line_upper == ')':
                indent_level = max(0, indent_level - 1)
            
            # Use 4 spaces for indent
            indent = ' ' * (indent_level * 4)
            formatted_lines.append(indent + line.lstrip())
            
            if line_upper.endswith('(') or line_upper.endswith('(\n'):
                indent_level += 1
                
        return SqlResult(True, output='\n'.join(formatted_lines))
    except Exception as e:
        return SqlResult(False, error_message=f"Formatting error: {e}")

def minify_sql(sql: str) -> SqlResult:
    if not sql.strip():
        return SqlResult(False, error_message="No SQL input provided.")
    try:
        # Remove multi-line comments
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        # Remove single-line comments
        sql = re.sub(r'--.*', '', sql)
        # Remove extra whitespace
        minified = re.sub(r'\s+', ' ', sql).strip()
        return SqlResult(True, output=minified)
    except Exception as e:
        return SqlResult(False, error_message=f"Minification error: {e}")
