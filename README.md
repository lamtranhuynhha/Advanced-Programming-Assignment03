# Symbol Table Implementation Assignment

## Overview
This project implements a symbol table for a simple programming language with scope management and type checking. It's part of the Advanced Programming course assignment. This assignment demands skillful use of Functional Programming, higher-order function and list comprehension.  

## Project Structure
BTL03/ 
├── main.py # Entry point and test runner
├── StaticError.py # Error definitions 
├── Symbol.py # Symbol class definition 
├── SymbolTable.py # Core symbol table implementation 
├── TestSuite.py # Test cases 
└── TestUtils.py # Testing utilities

## Features
- Variable declaration and type checking
- Scope management with BEGIN/END blocks
- Variable lookup across scopes
- Print functionality for symbol table state
- Two variable types: number and string
- Comprehensive error handling

## Commands
- `INSERT name type` - Declare a variable
- `ASSIGN name value` - Assign value to variable
- `BEGIN` - Start new scope
- `END` - End current scope
- `LOOKUP name` - Find variable's scope level
- `PRINT` - Display all visible variables
- `RPRINT` - Display all visible variables in reverse order

## Running Tests
```bash
py main.py           # Run all tests
py main.py test_001  # Run specific test
```

## Test Cases Cover
1. Basic variable declarations
2. Type checking
3. Scope management
4. Error handling
    Redeclaration errors
    Type mismatches
    Undeclared variables
    Invalid commands
    Block errors
