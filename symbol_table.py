class SymbolTable:
    def __init__(self):
        # Dictionary to hold symbols, each with its properties
        self.symbols = {}

    def add_symbol(self, name, symbol_type, value=None):
        """Adds a new symbol to the table if it doesn't already exist."""
        if name in self.symbols:
            raise ValueError(f"Symbol '{name}' already exists.")
        self.symbols[name] = {"type": symbol_type, "value": value}

    def update_symbol(self, name, value):
        """Updates the value of an existing symbol."""
        if name not in self.symbols:
            raise ValueError(f"Symbol '{name}' not found.")
        self.symbols[name]["value"] = value

    def get_symbol(self, name):
        """Retrieves a symbol's information."""
        if name not in self.symbols:
            raise ValueError(f"Symbol '{name}' not found.")
        return self.symbols[name]

    def __repr__(self):
        """String representation for debugging."""
        return str(self.symbols)

# Tests

# Initialize the symbol table
symbol_table = SymbolTable()

# Add different types of symbols
symbol_table.add_symbol("x", "int", 5)
symbol_table.add_symbol("pi", "float", 3.14)
symbol_table.add_symbol("greeting", "string", "Hello, Zara!")
symbol_table.add_symbol("numbers", "array<int>", [1, 2, 3, 4])
symbol_table.add_symbol("decimals", "stack<float>")

# Update a symbol's value
symbol_table.update_symbol("x", 10)

# Retrieve and print symbol information to verify accuracy
print("Symbol Table Entries:")
print(symbol_table)

# Output specific symbol details
print("\nDetails for 'x':", symbol_table.get_symbol("x"))
print("Details for 'greeting':", symbol_table.get_symbol("greeting"))
