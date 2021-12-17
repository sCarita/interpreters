// Types
const INTEGER = 'INTEGER';
// Operations
const MINUS = 'MINUS';
const PLUS = 'PLUS';
const DIV = 'DIV';
const MUL = 'MUL';
// Nesting Symbols
const LBRA = 'LBRA';
const RBRA = 'RBRA';
// Auxiliary tokens
const EOF = 'EOF';
const INIT = 'INIT';

// This class represent a Token to our interpreter, meaning that every group
// of lexemes will be represented using this blueprint.
class Token {
    constructor(type, value) {
        this.type = type;
        this.value = value;
    }

    toString() {
        return `Token(${this.type}, ${this.value})`;
    }
}

class TypeChecker {
    isNumber(num) {
        return (num >= '0' && num <= '9');
    }

    isOperation(op) {
        return (op == '+' || op == '-' || op == '/' || op == '*');
    }

    isNestSym(sym) {
        return (sym == '(' || sym == ')');
    }
}

class Lexer {
    constructor(input) {
        this.input = input.split(' ').join('');
        this.p = 0;
        this.checker = new TypeChecker();
    }

    advance() {
        this.p++;
    }

    getLexeme() {
        return this.input[this.p];
    }

    getInteger() {
        let integer = [];

        while (this.p < this.input.length) {
            if (this.checker.isNumber(this.getLexeme())) {
                integer.push(this.getLexeme());
            } else {
                break;
            }
            this.advance();
        }

        return parseInt(integer.join(''));
    }

    nextToken() {
        let currentLexeme = this.getLexeme();

        if (this.p >= this.input.length) {
            return new Token(EOF, 'EOF');
        } else if (this.checker.isNumber(currentLexeme)) {
            // Read the whole integer and return the integer token
            return new Token(INTEGER, this.getInteger());
        } else if (this.checker.isOperation(currentLexeme)) {
            // Return the right token for the lexeme operation
            this.advance();

            if (currentLexeme == '+') {
                return new Token(PLUS, '+')
            } else if (currentLexeme == '-') {
                return new Token(MINUS, '-')
            } else if (currentLexeme == '*') {
                return new Token(MUL, '*')
            } else if (currentLexeme == '/') {
                return new Token(DIV, '/')
            }
        } else if (this.checker.isNestSym(currentLexeme)) {
            this.advance();
            if (currentLexeme == '(') {
                return new Token(LBRA, '(')
            } else if (currentLexeme == ')') {
                return new Token(RBRA, ')')
            }
        } else {
            throw `Syntax Error! Undefined symbol found ${currentLexeme}`
        }
    }
}

class Interpreter {
    constructor(input) {
        this.lexer = new Lexer(input);
        this.currentToken = this.lexer.nextToken();
    }

    error () {
        throw 'Syntax Error!'
    }

    eat (type) {
        if (type == this.currentToken.type) {
            this.currentToken = this.lexer.nextToken();
        } else {
            this.error()
        }
    }

    factor () {
        let result = null;

        if (this.currentToken.type == INTEGER) {
            result = this.currentToken.value;
            this.eat(INTEGER);
        } else if (this.currentToken.type == LBRA) {
            this.eat(LBRA);
            result = this.expr();
            this.eat(RBRA);
        }

        return result;
    }

    term () {
        let result = this.factor();

        while (['*', '/'].includes(this.currentToken.value)) {
            if (this.currentToken.value == '*') {
                this.eat(MUL);
                result = result * this.factor();
            } else if (this.currentToken.value == '/') {
                this.eat(DIV);
                result = result / this.factor();
            }
        }

        return result;
    }

    expr () {
        let result = this.term();

        while (['+', '-'].includes(this.currentToken.value)) {
            if (this.currentToken.value == '+') {
                this.eat(PLUS);
                result = result + this.term();
            } else if (this.currentToken.value == '-') {
                this.eat(MINUS);
                result = result - this.term();
            }
        }

        return result;
    }
}

let interpreter = new Interpreter('3+7*2+(3*4+       (10*40/20*(2+3)))');
console.log(interpreter.expr());

interpreter = new Interpreter('3+7*2+(3*4+(10*40/20*(2+3)))');
console.log(interpreter.expr());
