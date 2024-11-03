import re


class LexicalAnalyzer:
    # Define token patterns
    token_patterns = {
        'KEYWORD': r'\b(if|else|do|while|for)\b',
        'DATATYPE': r'\b(integer|float|string|array|stack)\b',
        'OPERATOR': r'[+\-*/=<>]',
        'IDENTIFIER': r'\b[A-Za-z_]\w*\b',
        'NUMBER': r'\b\d+(\.\d+)?\b',
        'STRING': r'\".*?\"',
        'TERMINATOR': r'[;:,]'
    }

    def __init__(self):
        self.tokens = []

    def tokenize(self, code):
        # Combine all patterns into one regex
        pattern = '|'.join(f'(?P<{name}>{regex})'
                           for name, regex in self.token_patterns.items())
        regex = re.compile(pattern)
        # Find all tokens
        for match in regex.finditer(code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            self.tokens.append((token_type, token_value))
        return self.tokens

    def display_tokens(self):
        print("\nTokens:")
        for token_type, token_value in self.tokens:
            print(f"{token_type}: {token_value}")
        print("")