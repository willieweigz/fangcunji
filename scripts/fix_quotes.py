# -*- coding: utf-8 -*-
"""Fix unescaped ASCII double quotes inside JSON description string values."""
import json
import sys

filepath = sys.argv[1] if len(sys.argv) > 1 else 'data/stamps/1995.json'

with open(filepath, 'r', encoding='utf-8') as f:
    raw = f.read()

# We need to find description fields and fix internal ASCII double quotes
# Strategy: walk through the text character by character, tracking JSON context
result = []
i = 0
n = len(raw)

while i < n:
    # Check if we're at a description field
    if raw[i:i+16] == '"description": "':
        result.append(raw[i:i+16])
        i += 16
        # Now inside the string value
        value_chars = []
        quote_open = True  # alternate between opening and closing Chinese quotes
        while i < n:
            ch = raw[i]
            if ch == '\\' and i + 1 < n:
                # Escaped character - keep as is
                value_chars.append(ch)
                value_chars.append(raw[i+1])
                i += 2
                continue
            elif ch == '"':
                # Check if this is the end of the string value
                # Look ahead past whitespace to see if next is , or }
                j = i + 1
                while j < n and raw[j] in ' \t\n\r':
                    j += 1
                if j < n and raw[j] in ',}':
                    # This is the closing quote of the string
                    result.append(''.join(value_chars))
                    result.append('"')
                    i += 1
                    break
                else:
                    # Internal double quote - replace with Chinese full-width
                    if quote_open:
                        value_chars.append('\u201c')  # left double quote
                        quote_open = False
                    else:
                        value_chars.append('\u201d')  # right double quote
                        quote_open = True
                    i += 1
                    continue
            else:
                value_chars.append(ch)
                i += 1
        else:
            result.append(''.join(value_chars))
    else:
        result.append(raw[i])
        i += 1

fixed = ''.join(result)

# Verify it's valid JSON
try:
    json.loads(fixed)
    print('JSON is valid after fix!')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print('File saved.')
except json.JSONDecodeError as e:
    print(f'Still has error at line {e.lineno}, col {e.colno}: {e.msg}')
    # Show context
    start = max(0, e.pos - 100)
    end = min(len(fixed), e.pos + 100)
    print(f'Context:')
    print(fixed[start:end])
