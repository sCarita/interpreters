# Notes

**Source**: [https://ruslanspivak.com/lsbasi-part3/](https://ruslanspivak.com/lsbasi-part3/)

- A **syntax diagram** is a graphical representation of a programming language's syntax rules. Basically, a syntax diagram visually shows you which statements are allowed in your programming language and which are not.

    ![](./imgs/img_00.png)

- Syntax diagrams serve two main purposes:
    - They graphically represent the specification (grammar) of a programming language.
    - They can be used to help you write your parser - you can map a diagram to code by following simple rules.
- You've learned that the process of recognizing a phrase in the stream of tokens is called **parsing**. And the part of an interpreter or compiler that performs that job is called a **parser**. Parsing is also called **syntax analysis**, and the parser is also aptly called, you guessed it right, a **syntax analyzer**.
