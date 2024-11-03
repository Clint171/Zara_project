from lexer import Token, TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def advance(self):
        """Move to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None  # End of input

    def parse(self):
        """Start parsing the input tokens."""
        try:
            self.statements()
            print("Parsing completed successfully.")
        except Exception as e:
            print("Parsing error:", e)

    def match(self, token_type):
        """Check if current token matches a type and advance if it does."""
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def statements(self):
        """Parse multiple statements."""
        while self.current_token is not None:
            self.statement()

    def statement(self):
        """Parse a single statement, such as an expression or control structure."""
        if self.current_token.value == "if":
            self.if_statement()
        elif self.current_token.value == "do":
            self.do_while_statement()
        elif self.current_token.value == "{" or self.current_token.value == ";":
            self.advance()  # Just move past empty blocks or standalone semicolons
        else:
            self.expression()
            self.match(TokenType.DELIMITER)  # Expecting ';' after an expression

    def expression(self):
        """Parse an expression (very simple version for arithmetic)."""
        self.term()
        while self.current_token and self.current_token.value in ("+", "-"):
            self.advance()
            self.term()

    def term(self):
        """Parse a term within an expression (handling *, /)."""
        self.factor()
        while self.current_token and self.current_token.value in ("*", "/"):
            self.advance()
            self.factor()

    def factor(self):
        """Parse a factor in an expression, like a number or identifier."""
        if self.current_token.type == TokenType.LITERAL or self.current_token.type == TokenType.IDENTIFIER:
            self.advance()
        elif self.current_token.value == "(":
            self.advance()
            self.expression()
            self.match(TokenType.DELIMITER)  # Expecting ')'
        else:
            raise SyntaxError("Unexpected token in expression")

    def if_statement(self):
        """Parse an if-else statement."""
        self.match(TokenType.KEYWORD)  # 'if'
        self.match(TokenType.DELIMITER)  # '('
        self.expression()
        self.match(TokenType.DELIMITER)  # ')'
        self.match(TokenType.DELIMITER)  # '{'
        self.statements()  # parse the statements inside the block
        self.match(TokenType.DELIMITER)  # '}'
        if self.current_token and self.current_token.value == "else":
            self.advance()  # 'else'
            self.match(TokenType.DELIMITER)  # '{'
            self.statements()  # parse the else block
            self.match(TokenType.DELIMITER)  # '}'

    def do_while_statement(self):
        """Parse a do-while loop."""
        self.match(TokenType.KEYWORD)  # 'do'
        self.match(TokenType.DELIMITER)  # '{'
        self.statements()  # parse the body of the loop
        self.match(TokenType.DELIMITER)  # '}'
        self.match(TokenType.KEYWORD)  # 'while'
        self.match(TokenType.DELIMITER)  # '('
        self.expression()
        self.match(TokenType.DELIMITER)  # ')'
        self.match(TokenType.DELIMITER)  # ';'

# Sample Zara code tokens (after lexical analysis)
tokens = [
    Token(TokenType.KEYWORD, "do"),
    Token(TokenType.DELIMITER, "{"),
    Token(TokenType.IDENTIFIER, "x"),
    Token(TokenType.OPERATOR, "="),
    Token(TokenType.LITERAL, 10),
    Token(TokenType.DELIMITER, ";"),
    Token(TokenType.DELIMITER, "}"),
    Token(TokenType.KEYWORD, "while"),
    Token(TokenType.DELIMITER, "("),
    Token(TokenType.IDENTIFIER, "x"),
    Token(TokenType.OPERATOR, ">"),
    Token(TokenType.LITERAL, 0),
    Token(TokenType.DELIMITER, ")"),
    Token(TokenType.DELIMITER, ";")
]

# Parse the tokens
parser = Parser(tokens)
parser.parse()
