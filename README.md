# Milk V0.01 BETA

Milk Lang is a project I made following CodePulse's tutortial on how to create the BASIC programming language in python.
I started this project whne I was almost 13 years old, and I named this language after Dani's funny obsession with milk.
Dani is a famous youtuber who is in the process of creating a fun game called Karlson.

# Contributors

* Mantas Masaitis - Owner

## Current Capabilities

- Basic data types: integers, floats, booleans, strings, and lists.
- Variable assignment and basic arithmetic operations.
- Simple control flow statements: if-else, while and for loops.
- Basic support for functions.
- Experimental features:
    - **structs/objects**
    - **error handling**

## Getting Milk!

In the future I will try to compile it into one big file of bytecode to just put in your code editor and run at moments notice
To try out Milk, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/milk-lang.git`
2. Navigate to the cloned directory
3. Run the Milk interpreter: `main.py`
4. Start experimenting with Milk code!

## Syntax

```milk
# This is a comment

let num = 42                    # Int assignment
let pi = 3.14159                # Float assignment
let name = "John"               # String assignment
let list = [1, 2, 3, 4, 5]      # List assignment

print("Hello, " + name)         # Print statement

if num > 0:                     # If statement
    print("Num is positive!")
else:
    print("Num is not positive.")

while num > 0:                  # While loop
    print(num)
    num = num - 1

func add(a, b){                 # Function Definition
  return a + b
}

struct math{                    # Object Definition (Extremently Experimental)
  func add(a, b){
    return a + b
  }
  func sub(a, b){
    return a - b
  }
  func mul(a, b){
    return a * b
  }
  func div(a, b){
    return a / b
  }
}

math.add(1, 1)
```

## Contributing

Contributions to the Milk language are welcome!
If you're interested in contributing to the project, fork it, do your modifications and send a pull request.
Anybody who contributes will get their name of this **README.md** file.


## License

The Milk language is released under the MIT License. Feel free to use and modify the code according to the terms of the license.
Disclaimer

# Please note that the Milk language is still in active development and is not stable for production use. Use it at your own risk.
