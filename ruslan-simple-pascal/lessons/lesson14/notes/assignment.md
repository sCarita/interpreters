# Assignments

1. You’ve seen in the pictures throughout the article that the Main name in a program statement had subscript zero. I also mentioned that the program’s name is not in the global scope and it’s in some other outer scope that has level zero. Extend spi.py and create a builtins scope, a new scope at level 0, and move the built-in types INTEGER and REAL into that scope. For fun and practice, you can also update the code to put the program name into that scope as well.

2. For the source program in nestedscopes04.pas do the following:

* Write down the source Pascal program on a piece of paper
* Subscript every name in the program indicating the scope level of the declaration the name resolves to.
* Draw vertical lines for every name declaration (variable and procedure) to visually show its scope. Don’t forget about scope holes and their meaning when drawing.
* Write a source-to-source compiler for the program without looking at the example source-to-source compiler in this article.
* Use the original src2srccompiler.py program to verify the output from your compiler and whether you subscripted the names correctly in the exercise (2.2).
* Modify the source-to-source compiler to add subscripts to the built-in types INTEGER and REAL

3. Uncomment the following block in the spi.py

```
# interpreter = Interpreter(tree)
# result = interpreter.interpret()
# print('')
# print('Run-time GLOBAL_MEMORY contents:')
# for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
#     print('%s = %s' % (k, v))
```
* Run the interpreter with the part10.pas file as an input:
```
$ python spi.py part10.pas
```
* Spot the problems and add the missing methods to the semantic analyzer.