#!/usr/bin/env python3
import sys
import io
import os

# Set UTF-8 encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "aura" / "src"))

from aura.tools.browser.intent import parse_browser_intent
from aura.tools.browser.execute import execute_browser_intent
from langchain_ollama import ChatOllama

llm = ChatOllama(model='gpt-oss:120b-cloud', temperature=0)

test_cases = [
    'open youtube',
    'open www.youtube.com',
    'play spotify',
    'open github',
    'search for python programming'
]

print('\n=== Testing Browser Intent & Execution ===\n')
for test in test_cases:
    print(f'Input: "{test}"')
    intent = parse_browser_intent(llm, test)
    if intent:
        print(f'  Intent: {intent}')
        result = execute_browser_intent(intent)
        print(f'  Result: {result}')
    else:
        print(f'  ERROR: No intent parsed')
    print()

print('=== Test Complete ===\n')
