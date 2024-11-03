from lexical_analyzer import LexicalAnalyzer
from symbol_table import SymbolTable

# Example Zara code
zara_code = '''
integer x = 5;
float pi = 3.14;
string z = "Hello, World!";
float y = x;
if (x > 0){
    integer y = x + 1;
}
'''

# Tokenizing the Zara code
lexer = LexicalAnalyzer()
tokens = lexer.tokenize(zara_code)
lexer.display_tokens()

# Generating the symbol table from the tokens
symbol_table = SymbolTable()

current_datatype = None
current_name = None
current_operator = None
current_value = None
expected_next = ["DATATYPE", "IDENTIFIER", "KEYWORD"]

for token_type, token_value in tokens:
    if token_type in expected_next:
        if token_type == 'DATATYPE':
            current_datatype = token_value
            expected_next = ['IDENTIFIER']
            continue

        elif token_type == "IDENTIFIER":
            if current_datatype is not None:  # Handling variable declaration
                current_name = token_value
                expected_next = ["OPERATOR", "TERMINATOR"]
            else:  # Handling assignment to another variable (e.g., y = x)
                current_value = symbol_table.get_symbol(token_value)
                if current_value.startswith("Error"):
                    print(
                        f"Syntax error: Variable '{token_value}' not declared."
                    )
                    break
                expected_next = ["TERMINATOR", "OPERATOR"]
            continue

        elif token_type == "OPERATOR":
            if token_value == '=':
                expected_next = ["IDENTIFIER", "NUMBER", "STRING"]
            else:
                print(f"Syntax error: Unexpected operator {token_value}.")
                break
            continue

        elif token_type in ["NUMBER", "STRING"]:
            current_value = token_value
            symbol_table.add_symbol(current_name, current_datatype,
                                    current_value)
            expected_next = ["TERMINATOR", "OPERATOR"]
            continue

        elif token_type == "TERMINATOR":
            if current_datatype is not None and current_name is not None:
                # Complete the assignment of one variable to another (e.g., y = x)
                if current_value is not None and isinstance(current_value, tuple):
                    symbol_table.add_symbol(current_name, (current_datatype, current_value[1]))
            current_datatype, current_name, current_value = None, None, None
            expected_next = ["DATATYPE", "IDENTIFIER", "KEYWORD"]
            continue

    else:
        print(
            f'Syntax error: Expected token types: {expected_next} but got: {token_type}'
        )
        break

symbol_table.display_table()