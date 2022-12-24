import sys
import javascript

from browser import window

import sys

"""
    def tableify
    params:
        variables: list of alphabetical variables used in the equation
    creates initial columns of truth table with simple variables
"""
def tableify(variables):
    global numRows
    cols = []
    rows = []
    numRows = 2**len(variables)
    start = int(numRows/2)
    for var in variables:
        newCol = []
        counter = start
        bool = False
        for i in range(numRows):
            newCol.append(bool)
            counter = (counter - 1)
            if counter == 0:
                bool = not bool
                counter = start
        start = int(start/2)
        cols.append(newCol)
        dictVars[var] = newCol

    rows.append(variables)
    table.append(variables)
    for i in range(numRows):
        rows.append([])
        table.append([])

    for col in cols:
        for i in range(numRows):
            rows[i+1].append(col[i])
            table[i + 1].append(col[i])

"""
    def printTable:
    prints table at current state
"""
def printTable():
    for row in table:
        print(row)

"""
    def logicalOr:
    params: 
        varsToCalc: list of variables to calculate
    Searches for truth values of given variables and calculates a new column 
    for the logical Or calculation of said variables.
    Appends new column to the truth table and adds title and data to dictVars for further calculation uses.
"""
def logicalOr(varsToCalc):
    calcCol = []
    numVars = len(varsToCalc)
    title = ""
    for x in range(numVars):
        if len(varsToCalc[x]) > 1:
            titlevar = "(" + varsToCalc[x] + ")"
        else:
            titlevar = varsToCalc[x]
        if x == 0:
            title = title + titlevar
        else:
            title = title + "|" + titlevar

    for i in range(numRows):
        temp = []
        for var in varsToCalc:
            temp.append(dictVars[var][i])
        newBool = 0
        for j in range(len(temp)):
            newBool = (newBool + temp[j])
        if (newBool > 0):
            calcCol.append(True)
        else:
            calcCol.append(False)

    appendNewCol(calcCol, title)

"""
    def logicalAnd:
    params: 
        varsToCalc: list of variables to calculate
    Searches for truth values of given variables and calculates a new column 
    for the logical And calculation of said variables.
    Appends new column to the truth table and adds title and data to dictVars for further calculation uses.
"""
def logicalAnd(varsToCalc):
    calcCol = []
    numVars = len(varsToCalc)
    title = ""

    for x in range(numVars):
        if len(varsToCalc[x]) > 1:
            titlevar = "(" + varsToCalc[x] + ")"
        else:
            titlevar = varsToCalc[x]
        if x == 0:
            title = title + titlevar
        else:
            title = title + "&" + titlevar

    for i in range(numRows):
        temp = []
        for var in varsToCalc:
            temp.append(dictVars[var][i])

        newBool = 0
        for j in range(len(temp)):
            newBool = (newBool + temp[j])
        if (newBool == numVars):
            calcCol.append(True)
        else:
            calcCol.append(False)

    appendNewCol(calcCol, title)

"""
    def appendNewCol:
    params:
        newCol: a list of boolean data
        title: the corresponding equation for given data
    Updates truth table with new column and corresponding equation.
    Adds new data to dictVars for further calculation uses.
"""
def appendNewCol(newCol, title):
    test = title[1:-1]
    if title in dictVars:
        return
    elif test in dictVars:
        return
    else:
        for k in range(numRows + 1):
            if (k == 0):
                table[k].append(title)
            else:
                table[k].append(newCol[k - 1])
        dictVars[title] = newCol

"""
    def logicalNot:
    params:
        varToCalc: A list containing one variable
    Calculates the logical Not of a given variable.
    If more than one variable is given, throws bracket error.
"""
def logicalNot(varToCalc):
    var = ""
    if len(varToCalc) > 1:
        sys.exit("Error: Check Brackets")
    else:
        for i in varToCalc:
            var = var + i
    calcCol = []
    title = "!" + var
    for val in dictVars[var]:
        calcCol.append(not val)

    appendNewCol(calcCol, title)

"""
    def numOperators:
    params:
        equation: string containing a predicate logic equation
    Calculates the number of boolean operators in a given equation.
    returns:
        counter
"""
def numOperators(equation):
    counter = 0
    for char in equation:
        if (char == "&") or (char == "|") or (char == "!") :
            counter = counter + 1
    return counter

"""
    def interpretString:
    params:
        equation: string containing a predicate logic equation
        layer: integer representing a counter of which recursive layer the function is on
    Iterates through characters in the given equation and assesses the first bracketed sub-equation to calculate.
    Interprets the variables and operator in said sub-equation and passes the data along 
    to the appropriate logical operator function.
    A temporary string is passed into the equation to replace the sub-equation, and the function is called recursively.
"""
def interpretString(equation, layer):
    layer = layer + 1
    ref = "temp" + str(layer)

    for char in equation:
        if char == ")":
            stop = equation.index(char)
    revEq = equation[::-1]
    index = 0
    for char in revEq:
        if char == "(":
            start = (len(revEq) - index)
            if start > stop:
                revEq = revEq[:start - 1] + "?" + revEq[start:]
            else:
                break
        index = index + 1
    subStr = equation[start:stop]

    if "temp" in subStr:
        varsToCalc = checkTemps(subStr)[0]
        operator = checkTemps(subStr)[1]
        dictTemps[ref] = convertTemps(subStr)
    else:
        dictTemps[ref] = subStr
        varsToCalc = []
        operator = ""
        for char in subStr:
            if (char == "&") or (char == "|") or (char == "!") :
                operator = operator + char
            elif char.isalpha():
                varsToCalc.append(char)
            else:
                sys.exit("Error: Invalid Character")

    if operator == "|":
        logicalOr(varsToCalc)
    elif operator == "&":
        logicalAnd(varsToCalc)
    elif operator == "!":
        logicalNot(varsToCalc)
    else:
        sys.exit("Error: Check Brackets")

    equation = equation[:start - 1] + ref + equation[stop + 1:]
    if numOperators(equation) > 0:
        interpretString(equation, layer)
    else:
        return dictVars

"""
    def checkTemps:
    params:
        subStr: string containing a predicate logic equation, a sub-string from the original equation
    Checks given equation for any temporary strings (replacing previously calculated sub-equations).
    If found, searches for related data in dictVars and returns 
    a list of variables used and the logical operator to preform.
"""
def checkTemps(subStr):
    varsToCalc = []
    for char in subStr:
        if char == "|":
            operator = "|"
        elif char == "&":
            operator = "&"
        elif char == "!":
            operator = "!"
        elif char in dictVars:
            varsToCalc.append(char)
    for key in dictTemps:
        if key in subStr:
            index = subStr.find(key)
            subStr = subStr[:index] + dictTemps[key] + subStr[(index+len(key)):]
            if "temp" in dictTemps[key]:
                new = convertTemps(dictTemps[key])
                varsToCalc.append(new)
            else:
                varsToCalc.append(dictTemps[key])
    return varsToCalc, operator

"""
    def convertTemps:
    params:
        eq: string containing a predicate logic equation containing temporary replacement strings
        for previously calculated sub-equations
    Recursively replaces temporary strings with the equations they are replacing until all temps have been replaced.
    returns eq
"""
def convertTemps(eq):
    for key in dictTemps:
        titleKey = "(" + dictTemps[key] + ")"
        if key in eq:
            index = eq.find(key)
            eq = eq[:index] + titleKey + eq[(index+len(key)):]
    if "temp" in eq:
        convertTemps(eq)
    else:
        return eq

variables = []

"""
    def setUp:
    params:
        equation: string containing a predicate logic equation
    Does a preliminary error check on a given equation to assess matching brackets.
    Creates a list of all used alphabetical variables in equation.
"""
def setUp(equation):
    countOpen = 0
    countClose = 0
    for char in equation:
        if char.isalpha():
            if not (char in variables):
                variables.append(char)
        elif (char == "&") or (char == "|") or (char == "!") :
            continue
        elif (char == ")"):
            countClose = countClose + 1
        elif (char == "("):
            countOpen = countOpen + 1
        else:
            sys.exit("Error: Invalid Character")
    if countOpen != countClose:
        sys.exit("Error: Check Brackets")

"""
    def truthTable:
    params:
        eq: string containing a predicate logic equation
    Calls necessary functions to create a truth table for given equation
    returns:
        dictionary mapping variables to truth values
"""
def truthTable(eq):
    global dictVars
    global table
    global numRows
    global layerCounter
    global dictTemps
    global variables
    dictVars = {}
    variables = []
    table = []
    numRows = 2 ** len(variables)
    layerCounter = 0
    dictTemps = {}
    setUp(eq)
    tableify(variables)
    interpretString(eq, layerCounter)
    return javascript.JSON.stringify(dictVars)

test = "((((A|B)&(A&C))|((A|C)&(A&B)))|(!B))"
test2 = "(((A&B)|(A|B))|B)"
test3 = "((A&B)|A)"
test4 = "(((A|(!B))&(!C))&(A|(!B)))"
test5 = "((A|B)|(C|D))"

eq = "(A&B)"

dictVars = {}
table = []
numRows = 2**len(variables)
layerCounter = 0
dictTemps = {}

#truthTable(eq)
#print(truthTable(eq))
#printTable()





window.truthTable = truthTable
window.brythonReady()