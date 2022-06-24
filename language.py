"""
MIT License

Copyright (c) 2022 SkiingIsFun123

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
MIT License

Copyright (c) 2022 SkiingIsFun123

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional, ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator
from sys import *
import re

class NumericStringParser(object):
    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        self.bnf = expr
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val
        #MODULE FOR EVALIATING COMBINED MATH EXPRESSIONS

global variables
variables = {}
global constants
constants = {}

def mathLogic(line, element):
    elementfrommath = element
    for elementforsplit in elementfrommath.split():
        if variables.has_key(elementforsplit):
            elementfrommath = elementfrommath.replace(elementforsplit, variables[elementforsplit])
            #CHANGES VARIABLE TO NUMBER VALUE FOR MATH
        elif constants.has_key(elementforsplit):
            elementfrommath = elementfrommath.replace(elementforsplit, constants[elementforsplit])
            #CHANGES CONSTANT TO NUMBER VALUE FOR MATH
    if '+' in line and '-' not in line and '*' not in line and '/' not in line:
        elementfrommath = elementfrommath.split('+')
        newelement = elementfrommath[0]
        for i in range(len(elementfrommath)):
            if i == 0:
                pass
            else:
                newelement = int(newelement) + int(elementfrommath[i])
        return newelement
        #ADDITION LOGIC
    elif '-' in line and '+' not in line and '*' not in line and '/' not in line:
        elementfrommath = elementfrommath.split('-')
        newelement = elementfrommath[0]
        for i in range(len(elementfrommath)):
            if i == 0:
                pass
            else:
                newelement = int(newelement) - int(elementfrommath[i])
        return newelement
        #SUBTRACTION LOGIC
    elif '*' in line  and '-' not in line and '+' not in line and '/' not in line:
        elementfrommath = elementfrommath.split('*')
        newelement = elementfrommath[0]
        for i in range(len(elementfrommath)):
            if i == 0:
                pass
            else:
                newelement = int(newelement) * int(elementfrommath[i])
        return newelement
        #MULTIPLICATION LOGIC
    elif '/' in line  and '-' not in line and '*' not in line and '+' not in line:
        elementfrommath = elementfrommath.split('/')
        newelement = elementfrommath[0]
        for i in range(len(elementfrommath)):
            if i == 0:
                pass
            else:
                newelement = int(newelement) / int(elementfrommath[i])
        return newelement
        #DIVISION LOGIC
    else:
        nsp = NumericStringParser()
        result = nsp.eval(elementfrommath)
        return int(result)
        #COMBINED EXPRESSION LOGIC

def combineStringsLogic(variable):
    if ' + ' in variable:
        variablesplit = variable.split(' + ')
        varforfinalvar = ""
        itemlist = []
        for element in ' '.join(variablesplit).split():
            if "'" in element or '"' in element:
                elementone = element.replace('"', '')
                elementone = elementone.replace("'", "")
                itemlist.append(elementone)
            elif "'" not in element and '"' not in element:
                itemlist.append(variables[element])
        for i in range(len(itemlist)):
            varforfinalvar = varforfinalvar + itemlist[i]
        return varforfinalvar
        #COMBINE STRINGS LOGIC
    elif '+' in variable:
        variablesplit = variable.split('+')
        varforfinalvar = ""
        itemlist = []
        for element in ' '.join(variablesplit).split():
            if "'" in element or '"' in element:
                elementone = element.replace('"', '')
                elementone = elementone.replace("'", "")
                itemlist.append(elementone)
            elif "'" not in element and '"' not in element:
                itemlist.append(variables[element])
        for i in range(len(itemlist)):
            varforfinalvar = varforfinalvar + itemlist[i]
        return varforfinalvar
        #COMBINE STRINGS LOGIC

def printLogic(line):
    elementfromprint = line.split("print ",1)[1]
    if '"' in elementfromprint or "'" in elementfromprint:
        elementfromprint = elementfromprint.replace('"', '')
        elementfromprint = elementfromprint.replace("'", "")
        if '+' in elementfromprint:
            elementfromprint = elementfromprint.replace('"', '')
            elementfromprint = elementfromprint.replace("'", "")
            elementforsave = combineStringsLogic(''.join(elementfromprint))
            print(elementforsave)
            #COMBINES AND PRINTS STRING VALUE TO OUTPUT
        else:
            print(elementfromprint)
            #PRINTS STRING VALUE TO OUTPUT
    elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
        if '+' in line or '-' in line or '*' in line or '/' in line:
            mathreturned = mathLogic(line, elementfromprint)
            print(mathreturned)
            #HANDLES MATH LOGIC FOR PRINT
        elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
            number = elementfromprint
            print(number)
            #PRINTS NUMBER TO OUTPUT
    elif '+' in elementfromprint:
        elementfromprint = elementfromprint.replace('"', '')
        elementfromprint = elementfromprint.replace("'", "")
        elementforsave = combineStringsLogic(''.join(elementfromprint))
        print(elementforsave)
        #COMBINES AND PRINTS STRING VALUE TO OUTPUT
    else:
        if variables.has_key(elementfromprint):
            print(variables[elementfromprint])
            #PRINTS VARIABLE TO OUTPUT
        elif constants.has_key(elementfromprint):
            print(constants[elementfromprint])
            #PRINTS CONSTANT TO OUTPUT

def defineVariableLogic(line):
    elementfromdefine = line.split("variable ",1)[1]
    variable = elementfromdefine
    if ' = ' in variable:
        variablesplit = variable.split(' = ')
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split(' = ', 1)
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variablesplit[1].replace('"', '')
                varforstr = varforstr.replace("'", "")
                variables[variablesplit[0]] = varforstr
                #STRING VARIABLE
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                elementfromdefine = variablesplit[1]
                mathreturned = mathLogic(line, elementfromdefine)
                variables[variablesplit[0]] = mathreturned
                #HANDLES MATH LOGIC FOR DEFINING A VARIABLE
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                variables[variablesplit[0]] = number
                #SETS VARIABLE EQUAL TO MATH VALUE
        elif '"' not in variable and "'" not in variable:
            variables[variablesplit[0]] = variablesplit[1]
            #NUMBER VARIABLE
        else:
            print("ERROR")
            #ERROR
    elif '=' in variable:
        variablesplit = variable.split('=')
        #print(variablesplit)
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split('=')
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variable.replace('"', '')
                varforstr = varforstr.replace("'", "")
                variables[variablesplit[0]] = varforstr
                #STRING VARIABLE
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                elementfromdefine = variablesplit[1]
                mathreturned = mathLogic(line, elementfromdefine)
                variables[variablesplit[0]] = mathreturned
                #HANDLES MATH LOGIC FOR PRINT
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                variables[variablesplit[0]] = number
                #PRINTS NUMBER TO OUTPUT
        elif '"' not in variable and "'" not in variable:
            variables[variablesplit[0]] = variablesplit[1]
            #NUMBER VARIABLE
        else:
            print("ERROR")
            #ERROR
    elif '=' not in variable:
        varforstr = variable.replace('"', '')
        varforstr = varforstr.replace("'", "")
        variables[variable] = ""
        #DEFINE VARIABLE LOGIC
    else:
        print("ERROR")
        #ERROR

def defineConstantLogic(line):
    elementfromdefine = line.split("constant ",1)[1]
    variable = elementfromdefine
    if ' = ' in variable:
        variablesplit = variable.split(' = ')
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split(' = ', 1)
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variablesplit[1].replace('"', '')
                varforstr = varforstr.replace("'", "")
                constants[variablesplit[0]] = varforstr
                #STRING CONSTANT
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                returnedmathvalue = mathLogic(line, variablesplit[1])
                constants[variablesplit[0]] = returnedmathvalue
                #SETS CONSTANT EQUAL TO MATH OUTPUT
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                constants[variablesplit[0]] = number
                #SETS CONSTANT EQUAL TO NUMBER VALUE
        elif '"' not in variable and "'" not in variable:
            constants[variablesplit[0]] = variablesplit[1]
            #NUMBER CONSTANT
        else:
            print("ERROR")
            #ERROR
    elif '=' in variable:
        variablesplit = variable.split('=')
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split('=')
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variable.replace('"', '')
                varforstr = varforstr.replace("'", "")
                variables[variablesplit[0]] = varforstr
                #STRING VARIABLE
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                returnedmathvalue = mathLogic(line, variablesplit[1])
                constants[variablesplit[0]] = returnedmathvalue
                #SETS CONSTANT EQUAL TO MATH OUTPUT
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                constants[variablesplit[0]] = number
                #SETS CONSTANT EQUAL TO NUMBER VALUE
        elif '"' not in variable and "'" not in variable:
            constants[variablesplit[0]] = variablesplit[1]
            #NUMBER CONSTANT
        else:
            print("ERROR")
            #ERROR
    elif '=' not in variable:
        varforstr = variable.replace('"', '')
        varforstr = varforstr.replace("'", "")
        constants[variable] = ""
        #DEFINE CONSTANT LOGIC

def setVariableLogic(line):
    elementfromset = line.split("set ",1)[1]
    variable = elementfromset
    if ' = ' in variable:
        variablesplit = variable.split(' = ')
        #print(variablesplit)
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split(' = ', 1)
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variablesplit[1].replace('"', '')
                varforstr = varforstr.replace("'", "")
                variables[variablesplit[0]] = varforstr
                #STRING VARIABLE
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                returnedmathvalue = mathLogic(line, variablesplit[1])
                variables[variablesplit[0]] = returnedmathvalue
                #SETS VARIABLE EQUAL TO MATH OUTPUT
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                variables[variablesplit[0]] = number
                #SETS VARIABLE EQUAL TO NUMBER VALUE
        elif '"' not in variable and "'" not in variable:
            variables[variablesplit[0]] = variablesplit[1]
            #NUMBER VARIABLE

    elif '=' in variable:
        variablesplit = variable.split('=')
        #print(variablesplit)
        if '"' in variable or "'" in variable:
            if "+" in variable:
                variablesplitone = variable.split('=')
                elementforsave = combineStringsLogic(''.join(variablesplitone[1]))
                variables[variablesplitone[0]] = elementforsave
                #COMBINE STRINGS LOGIC
            else:
                varforstr = variablesplit[1].replace('"', '')
                varforstr = varforstr.replace("'", "")
                variables[variablesplit[0]] = varforstr
                #STRING VARIABLE
        elif "0" in line or "1" in line or "2" in line or "3" in line or "4" in line or "5" in line or "6" in line or "7" in line or "8" in line or "9" in line:
            if '+' in line or '-' in line or '*' in line or '/' in line:
                returnedmathvalue = mathLogic(line, variablesplit[1])
                variables[variablesplit[0]] = returnedmathvalue
                #SETS VARIABLE EQUAL TO MATH OUTPUT
            elif '+' not in line and '-' not in line and '*' not in line and '/' not in line:
                number = variablesplit[1]
                variables[variablesplit[0]] = number
                #SETS VARIABLE EQUAL TO NUMBER VALUE
        elif '"' not in variable and "'" not in variable:
            variables[variablesplit[0]] = variablesplit[1]
            #NUMBER VARIABLE
    elif '=' not in variable:
        varforstr = variable.replace('"', '')
        varforstr = varforstr.replace("'", "")
        variables[variable] = ""
        #DEFINE VARIABLE LOGIC

def userInputLogic(line):
    elementfromdefine = line.split("input ",1)[1]
    uservalue = input(elementfromdefine + ' > ')
    print(uservalue)

#def defineFunctionLogic(line):
    #functionname = line.split()[2]
    #print(functionname)
    #DEFINE FUNCTION LOGIC

#def useFunctionLogic(line):
    #functionname = line.split()[2]
    #print(functionname)
 #   pass
    #DEFINE FUNCTION LOGIC

def defineVariableNoValueLogic(line):
    elementfromset = line.split("define variable ",1)[1]
    variables[elementfromset] = ""
    #DEFINE VARIABLE WITH NO VALUE LOGIC

def defineConstantNoValueLogic(line):
    elementfromset = line.split("define constant ",1)[1]
    constants[elementfromset] = ""
    #DEFINE CONSTANT WITH NO VALUE LOGIC

def open_file(filename):
    data = open(filename, "r").read()
    data += "\n"
    data += "<EOF>"
    filenamesplit = filename.split('.')
    if str(filenamesplit[1]) == 'language':
        pass
    else:
        print('The file format ".' + str(filenamesplit[1]) + '" is not supported')
        exit()
    return data

def run():
    fileinfo = ""
    fileinfo = open_file(argv[1])
    #try:
    for i in range(1):
        fileinfo = fileinfo.split('\n')
        try:
            fileinfo.remove('')
        except:
            pass
        for line in fileinfo:
            if "print" in line and line[:2] != '//':
                printLogic(line)
            #elif "import" in line and line[:2] != '//':
            #    importLogic(line)
            elif "set" in line and line[:2] != '//':
                setVariableLogic(line)
            elif "variable" in line and "define variable" not in line  and line[:2] != '//':
                defineVariableLogic(line)
            elif "constant" in line and "define constant" not in line and line[:2] != '//':
                defineConstantLogic(line)
            elif "define variable" in line and line[:2] != '//':
                defineVariableNoValueLogic(line)
            elif "define constant" in line and line[:2] != '//':
                defineConstantNoValueLogic(line)
            elif "input" in line and line[:2] != '//':
                userInputLogic(line)
            #elif "define function" in line and line[:2] != '//':
            #    defineFunctionLogic(line)
            #elif "use" in line and line[:2] != '//':
            #    useFunctionLogic(line)
            elif line[:2] == '//':
                pass
                #COMMENT LOGIC
            elif line == "<EOF>":
                pass
            #else:
            #    print(line)
            #    print('broke')
            
    #except AttributeError:
    #    print("A file must be included for the interpreter to run")
    #except:
    #    print("There was an error")


run()
