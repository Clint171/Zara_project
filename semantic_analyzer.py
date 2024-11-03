from symbol_table import SymbolTable
from lexer import Token, TokenType

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def analyze(self, tokens):
        """Perform semantic analysis on the given tokens."""
        self.current_token_index = 0
        self.tokens = tokens
        self.current_token = self.tokens[self.current_token_index]
        self.scopes = [{}]  # Start with global scope

        while self.current_token_index < len(self.tokens):
            self.statement()
            self.current_token_index += 1

    def statement(self):
        """Analyze a single statement."""
        if self.current_token.type == TokenType.DATA_TYPE:
            self.variable_declaration()
        elif self.current_token.type == TokenType.IDENTIFIER:
            self.assignment_or_expression()
        elif self.current_token.value == "if":
            self.if_statement()
        elif self.current_token.value == "do":
            self.do_while_statement()

    def variable_declaration(self):
        """Check for variable declarations."""
        data_type = self.current_token.value
        self.current_token_index += 1  # Move to identifier
        identifier = self.tokens[self.current_token_index].value

        if identifier in self.scopes[-1]:
            raise NameError(f"Variable '{identifier}' already declared in this scope.")
        
        self.scopes[-1][identifier] = data_type  # Add variable to current scope
        self.current_token_index += 1  # Move to '='
        self.match(TokenType.OPERATOR)  # Expect '='
        self.current_token_index += 1  # Move to value
        value = self.tokens[self.current_token_index]

        if not self.check_type_compatibility(data_type, value):
            raise TypeError(f"Type mismatch: Cannot assign {value.type} to {data_type}.")

        self.match(TokenType.LITERAL)  # Expect a literal
        self.match(TokenType.DELIMITER)  # Expect ';'

    def assignment_or_expression(self):
        """Handle assignments or expressions."""
        identifier = self.current_token.value
        
        if identifier not in self.scopes[-1]:
            raise NameError(f"Variable '{identifier}' not declared.")

        self.current_token_index += 1  # Move to '=' or expression
        if self.tokens[self.current_token_index].type == TokenType.OPERATOR:
            self.match(TokenType.OPERATOR)  # Expect '='
            self.current_token_index += 1  # Move to value
            value = self.tokens[self.current_token_index]

            if not self.check_type_compatibility(self.scopes[-1][identifier], value):
                raise TypeError(f"Type mismatch: Cannot assign {value.type} to {self.scopes[-1][identifier]}.")

            self.match(TokenType.LITERAL)  # Expect a literal
            self.match(TokenType.DELIMITER)  # Expect ';'
        else:
            # It's an expression; handle accordingly.
            self.expression()

    def if_statement(self):
        """Analyze an if statement."""
        self.match(TokenType.KEYWORD)  # 'if'
        self.match(TokenType.DELIMITER)  # '('
        self.expression()
        self.match(TokenType.DELIMITER)  # ')'
        self.match(TokenType.DELIMITER)  # '{'
        while self.current_token.value != '}':
            self.statement()
        self.match(TokenType.DELIMITER)  # '}'
        if self.current_token.value == "else":
            self.current_token_index += 1
            self.match(TokenType.DELIMITER)  # '{'
            while self.current_token.value != '}':
                self.statement()
            self.match(TokenType.DELIMITER)  # '}'

    def do_while_statement(self):
        """Analyze a do-while loop."""
        self.match(TokenType.KEYWORD)  # 'do'
        self.match(TokenType.DELIMITER)  # '{'
        while self.current_token.value != '}':
            self.statement()
        self.match(TokenType.DELIMITER)  # '}'
        self.match(TokenType.KEYWORD)  # 'while'
        self.match(TokenType.DELIMITER)  # '('
        self.expression()
        self.match(TokenType.DELIMITER)  # ')'
        self.match(TokenType.DELIMITER)  # ';'

    def expression(self):
        """Analyze an expression."""
        self.term()
        while self.current_token and self.current_token.value in ("+", "-"):
            self.current_token_index += 1
            self.term()

    def term(self):
        """Analyze a term within an expression."""
        self.factor()
        while self.current_token and self.current_token.value in ("*", "/"):
            self.current_token_index += 1
            self.factor()

    def factor(self):
        """Analyze a factor in an expression."""
        if self.current_token.type == TokenType.IDENTIFIER:
            identifier = self.current_token.value
            if identifier not in self.scopes[-1]:
                raise NameError(f"Variable '{identifier}' not declared.")
        elif self.current_token.type == TokenType.LITERAL:
            pass  # Literals are fine
        else:
            raise SyntaxError("Unexpected token in expression")

    def check_type_compatibility(self, declared_type, value_token):
        """Check if the value type matches the declared variable type."""
        if value_token.type == TokenType.LITERAL:
            if isinstance(value_token.value, str):
                return declared_type == "string"
            elif isinstance(value_token.value, float):
                return declared_type == "float"
            elif isinstance(value_token.value, int):
                return declared_type == "int"
        return False

    def match(self, token_type):
        """Check if current token matches a type and advance if it does."""
        if self.current_token and self.current_token.type == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

# Test

# Sample Zara code tokens (after lexical analysis)
tokens = [
    Token(TokenType.DATA_TYPE, "int"),
    Token(TokenType.IDENTIFIER, "x"),
    Token(TokenType.OPERATOR, "="),
    Token(TokenType.LITERAL, 5),
    Token(TokenType.DELIMITER, ";"),
    Token(TokenType.DATA_TYPE, "float"),
    Token(TokenType.IDENTIFIER, "y"),
    Token(TokenType.OPERATOR, "="),
    Token(TokenType.LITERAL, 3.14),
    Token(TokenType.DELIMITER, ";"),
    Token(TokenType.DATA_TYPE, "string"),
    Token(TokenType.IDENTIFIER, "greeting"),
    Token(TokenType.OPERATOR, "="),
    Token(TokenType.LITERAL, "Hello, Zara!"),
    Token(TokenType.DELIMITER, ";"),
    Token(TokenType.KEYWORD, "if"),
    Token(TokenType.DELIMITER, "("),
    Token(TokenType.IDENTIFIER, "x"),
    Token(TokenType.OPERATOR, ">"),
    Token(TokenType.LITERAL, 0),
    Token(TokenType.DELIMITER, ")"),
    Token(TokenType.DELIMITER, "{"),
    Token(TokenType.IDENTIFIER, "greeting"),
    Token(TokenType.OPERATOR, "="),
    Token(TokenType.LITERAL, "Positive"),
    Token(TokenType.DELIMITER, ";"),
    Token(TokenType.DELIMITER, "}"),
]

# Assume we have a symbol table already created
symbol_table = SymbolTable()
# You would populate the symbol table here as necessary

# Analyze the tokens
analyzer = SemanticAnalyzer(symbol_table)
analyzer.analyze(tokens)
