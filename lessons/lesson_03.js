// Types
const INTEGER = 'INTEGER';
// Operations
const MINUS = 'MINUS';
const PLUS = 'PLUS';
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

class Interpreter {
    constructor(input) {
        this.input = input;
        this.pointer = 0;
        this.current_token = null;
    }

    #isNumber() {
        return (this.#currentLexeme() >= '0' && this.#currentLexeme() <= '9');
    }

    #isOperation() {
        return (this.#currentLexeme() == '+' || this.#currentLexeme() == '-');
    }

    #isWhitespace() {
        return this.#currentLexeme() === ' ';
    }

    #integer() {
        let lexemes = [];

        while (this.#isNumber(this.#currentLexeme())) {
            lexemes.push(this.#currentLexeme());
            this.#advance();
        }

        return parseInt(lexemes.join(''));
    }

    #operation() {
        if (this.#currentLexeme() == '+') {
            return new Token(PLUS, '+');
        } else if (this.#currentLexeme() == '-') {
            return new Token(MINUS, '-');
        }
    }

    #currentLexeme() {
        return this.input[this.pointer];
    }

    #advance() {
        this.pointer++;
    }

    #nextToken() {
        while (this.#currentLexeme() != null) {
            if (this.#isWhitespace()) {
                this.#advance();
                continue;
            }

            if (this.#isNumber()) {
                return new Token(INTEGER, this.#integer());
            }

            if (this.#isOperation()) {
                let op = this.#operation();
                this.#advance();
                return op;
            }

            throw `Compilation Error! "${this.#currentLexeme()}" is considered invalid.`
        }
        return new Token(EOF, 'EOF');
    }

    #check(type) {
        return (this.current_token.type == type)
    }

    expr() {
        let result = null;

        this.current_token = this.#nextToken();
        this.#check(INTEGER);

        if (this.current_token.type != INTEGER) {
            throw `Compilation Error!`
        }

        while (this.current_token.type != EOF) {
            if (result == null) {
                result = this.current_token.value;

            } else {
                this.current_token = this.#nextToken();

                if (this.#check(MINUS)) {
                    this.current_token = this.#nextToken();
                    this.#check(INTEGER);

                    result = result - this.current_token.value;
                } else if (this.#check(PLUS)) {
                    this.current_token = this.#nextToken();
                    this.#check(INTEGER);

                    result = result + this.current_token.value;
                }
            }
        }

        return result;
    }
}