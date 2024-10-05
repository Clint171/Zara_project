class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, symbol_type, value=None):
        if name in self.symbols:
            self.update_symbol_value(name, value)
        else:
            symbol_type = symbol_type.upper()
            self.symbols[name] = (symbol_type, value)
            print(f"Symbol '{name}' added with type '{symbol_type}'.")

    def update_symbol(self, name, symbol_type):
        if name in self.symbols:
            symbol_type = symbol_type.upper()
            self.symbols[name] = (symbol_type, self.symbols[name][1])
            print(f"Symbol '{name}' updated to type '{symbol_type}'.")
        else:
            print(f"Error: Symbol '{name}' not found.")

    def update_symbol_value(self, name, value=None):
        if name in self.symbols:
            if value == None:
                return
            self.symbols[name] = (self.symbols[name][0], value)
            print(f"Symbol '{name}' updated to value '{value}'.")
        else:
            print(f"Error: Symbol '{name}' not found.")

    def get_symbol(self, name):
        if name in self.symbols:
            return f"Symbol: {name}, Type: {self.symbols[name][0]}, Value: {self.symbols[name][1]}"
        else:
            return f"Error: Symbol '{name}' not found."

    def display_table(self):
        print("\nSymbol Table:")
        for name, value in self.symbols.items():
            print(f"{name}: ({value[0]}, {value[1]})")