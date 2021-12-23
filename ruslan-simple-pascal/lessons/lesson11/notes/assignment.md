# Assignments

- What is a symbol?

    ***symbol*** as an identifier of some program entity like a variable, subroutine, or built-in type.

- Why do we need to track symbols?

    Here are some of the reasons:

    - To make sure that when we assign a value to a variable the types are correct (type checking)
    - To make sure that a variable is declared before it is used

- What is a symbol table?

    A ***symbol table*** is an abstract data type (***ADT***) for tracking various symbols in source code.

- What is the difference between defining a symbol and resolving/looking up the symbol?

    **Defining:** The method *define* takes a symbol as a parameter and stores it internally in its *_symbols* ordered dictionary using the symbol's name as a key and the symbol instance as a value.

    **Resolving/Lookup:** Given a symbol name, we check for it's presence and return it's value if it is correct.

- Given the following small Pascal program, what would be the contents of the symbol table, the global memory (the GLOBAL_MEMORY dictionary that is part of the *Interpreter*)?

    **`PROGRAM** Part11**;VAR**x**,** y **:** **INTEGER;BEGIN**x **:=** **2;**y **:=** **3** **+** x**;END.**`