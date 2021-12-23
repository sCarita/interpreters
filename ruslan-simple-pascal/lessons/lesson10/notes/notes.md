# Notes

**Source** [https://ruslanspivak.com/lsbasi-part10/](https://ruslanspivak.com/lsbasi-part8/)

- Let's sum up what we had to do to extend the Pascal interpreter in this article:
    - Add new rules to the grammar and update some existing rules
    - Add new tokens and supporting methods to the lexer, update and modify some existing methods
    - Add new AST nodes to the parser for new language constructs
    - Add new methods corresponding to the new grammar rules to our recursive-descent parser and update some existing methods
    - Add new visitor methods to the interpreter and update one existing visitor method

    As a result of our changes we also got rid of some of the hacks I introduced in [Part 9](https://ruslanspivak.com/lsbasi-part9/), namely:

    - Our interpreter can now handle the ***PROGRAM*** header
    - Variables can now be declared using the ***VAR*** keyword
    - The ***DIV*** keyword is used for integer division and a forward slash / is used for float division