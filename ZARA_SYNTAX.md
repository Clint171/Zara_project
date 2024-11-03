# Zara Syntax

### 1. Variable Declaration and Assignment

Zara will follow Java’s declaration format, with keywords for data types. The language uses `=` for assignment.

```zara
int x = 5;
float y = 3.14;
string greeting = "Hello, Zara!";
array<int> numbers = [1, 2, 3, 4];
stack<float> decimals;
```

### 2. Control Structures

#### If-Else

```zara
if (x > 0) {
    print("Positive number");
} else if (x < 0) {
    print("Negative number");
} else {
    print("Zero");
}
```

#### For Loop

```zara
for (int i = 0; i < 10; i++) {
    print(i);
}
```

#### Do-While Loop

```zara
int counter = 0;
do {
    print(counter);
    counter = counter + 1;
} while (counter < 5);
```

### 3. Methods and Functions

Functions will start with a return type, followed by the function name, and parameters.

```zara
int add(int a, int b) {
    return a + b;
}

void greet(string name) {
    print("Hello, " + name + "!");
}
```

### 4. Classes and Object-Oriented Syntax

```zara
class Person {
    string name;
    int age;
    
    Person(string name, int age) {
        this.name = name;
        this.age = age;
    }
    
    void introduce() {
        print("Hello, my name is " + this.name + " and I am " + this.age + " years old.");
    }
}

// Creating an object
Person john = new Person("John Doe", 25);
john.introduce();
```

### 5. Hybrid Functional Paradigm

Functions can be treated as first-class entities, allowing for some functional features like passing functions as arguments.

```zara
void applyFunction(int x, function<int, int> func) {
    int result = func(x);
    print(result);
}

int square(int n) {
    return n * n;
}

// Using the function as an argument
applyFunction(5, square);
```

### 6. Example Program in Zara

Putting it all together, here’s an example of Zara code:

```zara
class Calculator {
    int add(int a, int b) {
        return a + b;
    }

    int multiply(int a, int b) {
        return a * b;
    }
}

void main() {
    Calculator calc = new Calculator();
    int result1 = calc.add(10, 20);
    int result2 = calc.multiply(5, 4);

    if (result1 > result2) {
        print("Addition result is greater.");
    } else {
        print("Multiplication result is greater or equal.");
    }
}
```