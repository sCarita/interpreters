# Assignments

1. **What is an interpreter?**

    An **interpreter** interprets a language by reading the text or source code and then performing computations as it processes the text to execute the text. So as the interpreter is reading the source of the program, the program runs or executes as the interpreter reads lines of code and performs those actions.

    It performs the operations implied by the source program. Operations are usually implied in form of [intermediate code](https://en.wikipedia.org/wiki/Intermediate_representation) representation.

2. **What is a compiler?**

    A **compiler** compiles a language by reading the text or source and transforms the source code into another form which is typically machine code.

3. **What's the difference between an interpreter and a compiler?**

    In basic terms the **difference between an interpreter and a compiler** is the point at which a source text is actually executed.

    **The key difference is this**: An interpreter processes the source code as it runs it. It does not convert the source into machine code, it simply uses its own code to accomplish what the source directs. A compiler converts the source code into machine code that can be run directly.

    Not all compilers are separate from the execution process. For example, most Java run-times include a "JIT compiler" that compiles Java code while it's running, as needed.

    You can have things in-between. Essentially, a process similar to compiling can be used first to convert the source code into something smaller and easier to interpret. This compiled output can then be interpreted. (For example, a first pass could convert, say 'if' to 53, 'else' to 54, 'for' to 55, and so on -- this will save the interpreter from having to handle variable-length strings in code that doesn't actually deal with strings.)

4. **What is a token?**

    A **token** is an object that has a type and a value.

5. **What is the name of the process that breaks input apart into tokens?**

    The process responsible for breaking a given input into tokens is called lexical analysis.

6. **What is the part of the interpreter that does lexical analysis called?**

    Lexical analysis is commonly executed by the lexical analyzer.

7. **What are the other common names for that part of an interpreter or a compiler?**

    Can also be called lexer, scanner, or tokenizer.