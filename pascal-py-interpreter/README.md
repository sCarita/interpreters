# Pascal Simple Interpreter in Python

## Motivation

The motivation of this interpreter is to implement an *almost* feature complete Pascal interpreter in Python language. Since the building 

## Setup

    `$ make requirements`

## Development

* Verify all the type hints in our interpreter code:
    `$ make type-check`
* Run our interpreter for a program declared inside `programs/` folder:
    `$ python3 main.py {PROGRAM_NAME} --scope --stack --viz`
* Help about our interpreter flags:
    `$ python3 main.py -h`

## Grammar (implemented)

## To Do

- Implement pascal functions
  - Implement pascal function declaration
  - Implement pascal function call
- Implement control flow
- Implement loops

## Sources

- Pascal - Syntax in BNF Notation: http://www.iro.umontreal.ca/~felipe/IFT6820-Hiver2005/Complements/pascalbnf.html