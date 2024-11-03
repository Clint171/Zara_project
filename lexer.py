import re
from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    DATA_TYPE = "DATA_TYPE"
    LITERAL = "LITERAL"
    DELIMITER = "DELIMITER"
    UNKNOWN = "UNKNOWN"

KEYWORDS = {"if", "else", "do", "while", "for"}
OPERATORS = {"=", "+", "-", "*", "/", "==", ">"}
DATA_TYPES = {"int", "float", "string", "array", "stack"}
DELIMITERS = {"(", ")", "{", "}", ";", ","}

# Regular expressions for literals
NUMBER_PATTERN = re.compile(r"\b\d+(\.\d+)?\b")  # Integer or float numbers
STRING_PATTERN = re.compile(r'"([^"\\]|\\.)*"')  # Strings enclosed in double quotes
IDENTIFIER_PATTERN = re.compile(r"\b[a-zA-Z_]\w*\b")  # Identifiers (variable names)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        # Remove any surrounding whitespace and iterate over the code
        index = 0
        while index < len(self.code):
            char = self.code[index]

            # Skip whitespace
            if char.isspace():
                index += 1
                continue

            # Check for delimiters
            if char in DELIMITERS:
                self.tokens.append(Token(TokenType.DELIMITER, char))
                index += 1
                continue

            # Check for operators (could be multi-character like '==')
            elif any(self.code.startswith(op, index) for op in OPERATORS):
                for op in OPERATORS:
                    if self.code.startswith(op, index):
                        self.tokens.append(Token(TokenType.OPERATOR, op))
                        index += len(op)
                        break
                continue

            # Check for literals (numbers)
            elif NUMBER_PATTERN.match(self.code, index):
                match = NUMBER_PATTERN.match(self.code, index)
                number = match.group(0)
                self.tokens.append(Token(TokenType.LITERAL, float(number) if '.' in number else int(number)))
                index += len(number)
                continue

            # Check for string literals
            elif STRING_PATTERN.match(self.code, index):
                match = STRING_PATTERN.match(self.code, index)
                string_literal = match.group(0).strip('"')
                self.tokens.append(Token(TokenType.LITERAL, string_literal))
                index += len(match.group(0))
                continue

            # Check for identifiers or keywords
            elif IDENTIFIER_PATTERN.match(self.code, index):
                match = IDENTIFIER_PATTERN.match(self.code, index)
                identifier = match.group(0)
                if identifier in KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD, identifier))
                elif identifier in DATA_TYPES:
                    self.tokens.append(Token(TokenType.DATA_TYPE, identifier))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, identifier))
                index += len(identifier)
                continue

            # If none of the above, mark as unknown and move forward
            else:
                self.tokens.append(Token(TokenType.UNKNOWN, char))
                index += 1

        return self.tokens


# Tests

# Sample Zara code to tokenize
zara_code = '''
int x = 5;
float y = 3.14;
string greeting = "Hello, Zara!";
if (x > 0) {
    greeting = "Positive";
}
'''

# Create and run the lexer
lexer = Lexer(zara_code)
tokens = lexer.tokenize()

# Print out the tokens
print("Tokens:")
for token in tokens:
    print(token)
