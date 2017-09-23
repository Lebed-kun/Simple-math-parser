
import re
import math
import random

class Token(object):
    def __init__(self, lexeme, value=None):
        self.lexeme = lexeme
        self.value = value


class Lexer():
    NUMBER = r'(?:0|[1-9]\d*)(?:\.\d+)?'
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIVIDE = r'\/'
    POWER = r'\^'
    LPAREN = r'\('
    RPAREN = r'\)'
    KWFUNC = r'(abs|sqrt|ln|sin|cos|tg|asin|acos|atg|rand)(?=[ \t]*\()'
    KWCONST = r'pi|e'

    def Lexify(inp):
        toks = []
        acc = 0
        remString = inp

        while(len(remString) > 0):
            if not re.match(r'[ \t]+', remString) is None:
                spaces = re.match(r'[ \t]+', remString).group()
                acc += len(spaces)
                remString = remString[len(spaces):]
            else:
                if not re.match(Lexer.NUMBER, remString) is None:
                    num = float(re.match(Lexer.NUMBER, remString).group())
                    toks.append(Token(Lexer.NUMBER, num))
                elif not re.match(Lexer.PLUS, remString) is None:
                    toks.append(Token(Lexer.PLUS))
                elif not re.match(Lexer.MINUS, remString) is None:
                    toks.append(Token(Lexer.MINUS))
                elif not re.match(Lexer.TIMES, remString) is None:
                    toks.append(Token(Lexer.TIMES))
                elif not re.match(Lexer.DIVIDE, remString) is None:
                    toks.append(Token(Lexer.DIVIDE))
                elif not re.match(Lexer.POWER, remString) is None:
                    toks.append(Token(Lexer.POWER))
                elif not re.match(Lexer.LPAREN, remString) is None:
                    toks.append(Token(Lexer.LPAREN))
                elif not re.match(Lexer.RPAREN, remString) is None:
                    toks.append(Token(Lexer.RPAREN))
                elif not re.match(Lexer.KWFUNC, remString) is None:
                    func = re.match(Lexer.KWFUNC, remString).group()
                    toks.append(Token(Lexer.KWFUNC, func))
                elif not re.match(Lexer.KWCONST, remString) is None:
                    cons = re.match(Lexer.KWCONST, remString).group()
                    toks.append(Token(Lexer.KWCONST, cons))
                else:
                    print("! Error: invalid token at "+acc)
                    toks = []
                    break

                tail = re.match(toks[-1].lexeme, remString).group()
                acc += len(tail)
                remString = remString[len(tail):]


        return toks


class Parser():
    """
        expr ::= expr '+' term
        expr ::= expr '-' term
        expr ::= term

        term ::= term '*' fact
        term ::= term '/' fact
        term ::= fact

        fact ::= atom '^' fact
        fact ::= atom

        atom ::= kwfunc '(' expr ')'
        atom ::= '(' expr ')'
        atom ::= '+' atom
        atom ::= '-' atom
        atom ::= kwconst
        atom ::= number
    """

    def ParseExpression(tokens):
        parens = 0
        i = 0

        while i < len(tokens):
            if tokens[len(tokens)-1-i].lexeme == Lexer.LPAREN:
                parens += 1
            elif tokens[len(tokens)-1-i].lexeme == Lexer.RPAREN:
                parens -= 1

            if parens == 0:
                if (tokens[len(tokens)-1-i].lexeme == Lexer.PLUS) and (len(tokens)-1-i != 0):
                    return Parser.ParseExpression(tokens[:len(tokens)-1-i]) + Parser.ParseTerm(tokens[len(tokens)-i:])
                elif (tokens[len(tokens)-1-i].lexeme == Lexer.MINUS) and (len(tokens)-1-i != 0):
                    return Parser.ParseExpression(tokens[:len(tokens)-1-i]) - Parser.ParseTerm(tokens[len(tokens)-i:])

            i += 1

        if parens == 0:
            return Parser.ParseTerm(tokens)
        else:
            print("! Error: unmatching brackets")

    def ParseTerm(tokens):
        parens = 0
        i = 0

        while i < len(tokens):
            if tokens[len(tokens)-1-i].lexeme == Lexer.LPAREN:
                parens += 1
            elif tokens[len(tokens)-1-i].lexeme == Lexer.RPAREN:
                parens -= 1

            if parens == 0:
                if tokens[len(tokens)-1-i].lexeme == Lexer.TIMES:
                    return Parser.ParseTerm(tokens[:len(tokens)-1-i]) * Parser.ParseFactor(tokens[len(tokens)-i:])
                elif tokens[len(tokens)-1-i].lexeme == Lexer.DIVIDE:
                    return Parser.ParseTerm(tokens[:len(tokens)-1-i]) / Parser.ParseFactor(tokens[len(tokens)-i:])

            i += 1

        if parens == 0:
            return Parser.ParseFactor(tokens)
        else:
            print("! Error: unmatching brackets")

    def ParseFactor(tokens):
        parens = 0
        i = 0

        while i < len(tokens):
            if tokens[i].lexeme == Lexer.LPAREN:
                parens += 1
            elif tokens[i].lexeme == Lexer.RPAREN:
                parens -= 1

            if (parens == 0) and (tokens[i].lexeme == Lexer.POWER):
                return Parser.ParseAtom(tokens[:i]) ** Parser.ParseFactor(tokens[i+1:])
                

            i += 1

        if parens == 0:
            return Parser.ParseAtom(tokens)
        else:
            print("! Error: unmatching brackets")
        pass

    def ParseAtom(tokens):
        if len(tokens) >= 4:
            cond = (tokens[0].lexeme == Lexer.KWFUNC) and (tokens[1].lexeme == Lexer.LPAREN)
            cond = cond and (tokens[len(tokens)-1].lexeme == Lexer.RPAREN)

            if cond:
                expr = tokens[2:len(tokens)-1]
                if tokens[0].value == 'abs':
                    return abs(Parser.ParseExpression(expr))
                elif tokens[0].value == 'sqrt':
                    return math.sqrt(Parser.ParseExpression(expr))
                elif tokens[0].value == 'ln':
                    return math.log(Parser.ParseExpression(expr))
                elif tokens[0].value == 'sin':
                    return math.sin(Parser.ParseExpression(expr))
                elif tokens[0].value == 'cos':
                    return math.cos(Parser.ParseExpression(expr))
                elif tokens[0].value == 'tg':
                    return math.tan(Parser.ParseExpression(expr))
                elif tokens[0].value == 'asin':
                    return math.asin(Parser.ParseExpression(expr))
                elif tokens[0].value == 'acos':
                    return math.acos(Parser.ParseExpression(expr))
                elif tokens[0].value == 'atg':
                    return math.atan(Parser.ParseExpression(expr))
            elif (tokens[0].lexeme == Lexer.LPAREN) and (tokens[len(tokens)-1].lexeme == Lexer.RPAREN):
                expr = tokens[1:len(tokens)-1]
                return Parser.ParseExpression(expr)
        

        elif len(tokens) >= 2:
            cond = (tokens[0].value == 'rand') and (tokens[1].lexeme == Lexer.LPAREN)
            cond = cond and (tokens[len(tokens)-1] == Lexer.RPAREN)
            cond = cond and len(tokens) == 3

            if cond:
                return random.random()
            elif tokens[0].lexeme == Lexer.PLUS:
                return Parser.ParseAtom(tokens[1:])
            elif tokens[0].lexeme == Lexer.MINUS:
                return -Parser.ParseAtom(tokens[1:])
            elif (len(tokens) >= 3) and (tokens[0].lexeme == Lexer.LPAREN) and (tokens[len(tokens)-1].lexeme == Lexer.RPAREN):
                return Parser.ParseExpression(tokens[1:len(tokens)-1])
        elif len(tokens) == 1:
            if tokens[0].lexeme == Lexer.KWCONST:
                if tokens[0].value == 'pi':
                    return math.pi
                elif tokens[0].value == 'e':
                    return math.e
            elif tokens[0].lexeme == Lexer.NUMBER:
                return tokens[0].value
                
    def Parse(tokens):
        return Parser.ParseExpression(tokens)


print(Parser.Parse(Lexer.Lexify("ln (sin (pi / 4))")))
