from symbol_table import SymbolTable
from lexer import Token, TokenType

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, op, arg1=None, arg2=None, result=None):
        self.instructions.append([op, arg1, arg2, result])

    def display_instructions(self):
        for inst in self.instructions:
            print(f"{inst[3]} = {inst[1]} {inst[0]} {inst[2]}" if inst[2] else f"{inst[3]} = {inst[1]}")


class ParserWithTranslation:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.tac = TACGenerator()

    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def parse(self):
        while self.current_token_index < len(self.tokens):
            self.statement()

    def statement(self):
        if self.current_token.type == TokenType.DATA_TYPE:
            self.variable_declaration()
        elif self.current_token.type == TokenType.IDENTIFIER:
            self.assignment()

    def variable_declaration(self):
        data_type = self.current_token.value
        self.current_token_index += 1  # Move to identifier
        identifier = self.tokens[self.current_token_index].value
        self.symbol_table.add_symbol(identifier, data_type)
        self.match(TokenType.IDENTIFIER)
        if self.current_token and self.current_token.type == TokenType.OPERATOR:
            self.match(TokenType.OPERATOR)  # '='
            value = self.tokens[self.current_token_index]
            temp = self.tac.new_temp()
            if value.type == TokenType.LITERAL:
                self.tac.emit('=', value.value, None, identifier)
            self.match(TokenType.LITERAL)
        self.match(TokenType.DELIMITER)  # ';'

    def assignment(self):
        identifier = self.current_token.value
        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.OPERATOR)  # '='
        expr_value = self.expression()
        self.tac.emit('=', expr_value, None, identifier)
        self.match(TokenType.DELIMITER)  # ';'

    def expression(self):
        term_val = self.term()
        while self.current_token and self.current_token.value in ("+", "-"):
            op = self.current_token.value
            self.current_token_index += 1
            next_term_val = self.term()
            temp = self.tac.new_temp()
            self.tac.emit(op, term_val, next_term_val, temp)
            term_val = temp
        return term_val

    def term(self):
        factor_val = self.factor()
        while self.current_token and self.current_token.value in ("*", "/"):
            op = self.current_token.value
            self.current_token_index += 1
            next_factor_val = self.factor()
            temp = self.tac.new_temp()
            self.tac.emit(op, factor_val, next_factor_val, temp)
            factor_val = temp
        return factor_val

    def factor(self):
        if self.current_token.type == TokenType.LITERAL:
            value = self.current_token.value
            self.current_token_index += 1
            return value
        elif self.current_token.type == TokenType.IDENTIFIER:
            identifier = self.current_token.value
            self.current_token_index += 1
            return identifier
        else:
            raise SyntaxError("Unexpected token in factor")

    def display_tac(self):
        print("Three-Address Code (TAC):")
        self.tac.display_instructions()
    def if_statement(self):
        # Match 'if' keyword and process condition
        self.match(TokenType.KEYWORD)  # 'if'
        self.match(TokenType.DELIMITER)  # '('
        condition = self.expression()
        self.match(TokenType.DELIMITER)  # ')'

        # Label for if-true block
        true_label = self.tac.new_label()
        end_label = self.tac.new_label()

        # Emit TAC for condition check and jump to true_label if true
        self.tac.emit('if', condition, None, true_label)
        self.tac.emit('goto', None, None, end_label)  # Skip true block if false
        self.tac.emit('label', true_label, None, None)

        # Process if-true block
        self.match(TokenType.DELIMITER)  # '{'
        while self.current_token and self.current_token.type != TokenType.DELIMITER:
            self.statement()
        self.match(TokenType.DELIMITER)  # '}'

        # Optional else
        self.tac.emit('label', end_label, None, None)
        if self.current_token and self.current_token.type == TokenType.KEYWORD and self.current_token.value == "else":
            self.match(TokenType.KEYWORD)  # 'else'
            else_label = self.tac.new_label()
            self.tac.emit('goto', None, None, else_label)
            self.tac.emit('label', else_label, None, None)
            self.match(TokenType.DELIMITER)  # '{'
            while self.current_token and self.current_token.type != TokenType.DELIMITER:
                self.statement()
            self.match(TokenType.DELIMITER)  # '}'

    def do_while_loop(self):
        # Label for the beginning of the loop
        loop_start = self.tac.new_label()
        self.tac.emit('label', loop_start, None, None)

        # Process loop body
        self.match(TokenType.KEYWORD)  # 'do'
        self.match(TokenType.DELIMITER)  # '{'
        while self.current_token and self.current_token.type != TokenType.DELIMITER:
            self.statement()
        self.match(TokenType.DELIMITER)  # '}'

        # Process loop condition
        self.match(TokenType.KEYWORD)  # 'while'
        self.match(TokenType.DELIMITER)  # '('
        condition = self.expression()
        self.match(TokenType.DELIMITER)  # ')'
        self.match(TokenType.DELIMITER)  # ';'

        # Emit TAC for condition and jump back to loop_start if true
        self.tac.emit('if', condition, None, loop_start)

tokens = [
    # Variable declarations
    Token(TokenType.DATA_TYPE, "int"), Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, "="), Token(TokenType.LITERAL, 5), Token(TokenType.DELIMITER, ";"),
    
    # If statement
    Token(TokenType.KEYWORD, "if"), Token(TokenType.DELIMITER, "("), Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, ">"), Token(TokenType.LITERAL, 0), Token(TokenType.DELIMITER, ")"),
    Token(TokenType.DELIMITER, "{"), Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, "="), Token(TokenType.LITERAL, 10), Token(TokenType.DELIMITER, ";"), Token(TokenType.DELIMITER, "}"),
    
    # Do-while loop
    Token(TokenType.KEYWORD, "do"), Token(TokenType.DELIMITER, "{"),
    Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, "="), Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, "+"), Token(TokenType.LITERAL, 1), Token(TokenType.DELIMITER, ";"),
    Token(TokenType.DELIMITER, "}"), Token(TokenType.KEYWORD, "while"), Token(TokenType.DELIMITER, "("), Token(TokenType.IDENTIFIER, "x"), Token(TokenType.OPERATOR, "<"), Token(TokenType.LITERAL, 20), Token(TokenType.DELIMITER, ")"), Token(TokenType.DELIMITER, ";"),
]

symbol_table = SymbolTable()
parser = ParserWithTranslation(tokens, symbol_table)
parser.parse()
parser.display_tac()
