# Notes

**Source** [https://ruslanspivak.com/lsbasi-part12/](https://ruslanspivak.com/lsbasi-part8/)

- While our Pascal program can be grammatically correct and the parser can successfully build an *abstract syntax tree*, the program still can contain some pretty serious errors. To catch those errors we need to use the *abstract syntax tree* and the information from the *symbol table*.
- What is ***semantic analysis***? Basically, it's just a process to help us determine whether a program makes sense, and that it has meaning, according to a language definition.
- Pascal language and, specifically, Free Pascal's compiler, has certain requirements that, if not followed in a program, would lead to an error from the *fpc* compiler indicating that the program doesn't "make sense", that it is incorrect, even though the syntax might look okay. Here are some of those requirements:
    - The variables must be declared before they are used
    - The variables must have matching types when used in arithmetic expressions (this is a big part of *semantic analysis* called *type checking* that we'll cover separately)
    - There should be no duplicate declarations (Pascal prohibits, for example, having a local variable in a procedure with the same name as one of the procedure's formal parameters)
    - A name reference in a call to a procedure must refer to the actual declared procedure (It doesn't make sense in Pascal if, in the procedure call **foo()**, the name *foo* refers to a variable foo of a primitive type INTEGER)
    - A procedure call must have the correct number of arguments and the arguments' types must match those of formal parameters in the procedure declaration
- After we implement the semantic analysis phase, the structure of our Pascal interpreter will look something like this:

    ![Untitled](Compilers%20b950f6cecac045a1a3e21a3a43b4efda/Untitled%2032.png)

- In the following section, we're going to discuss how to implement some of the semantic checks and how to build the symbol table: in other words, we are going to discuss how to perform a *semantic analysis* of our Pascal programs. Keep in mind that even though *semantic analysis* sounds fancy and deep, it's just another step after parsing our program and creating an AST to check the source program for some additional errors that the parser couldn't catch due to a lack of additional information (context).
- Today we're going to focus on the following two *static semantic checks**:
    1. That variables are declared before they are used
    2. That there are no duplicate variable declarations
    - *Static semantic checks* are the checks that we can make before interpreting (evaluating) the program, that is, before calling the interpret method on an instance of the Interpreter class. All the Pascal requirements mentioned before can be enforced with *static semantic checks* by walking an AST and using information from the symbol table.
    - *Dynamic semantic checks*, on the other hand, would require checks to be performed during the interpretation (evaluation) of the program. For example, a check that there is no division by zero, and that an array index is not out of bounds would be a *dynamic semantic check*. Our focus today is on *static semantic checks*.

    ![Untitled](Compilers%20b950f6cecac045a1a3e21a3a43b4efda/Untitled%2033.png)
