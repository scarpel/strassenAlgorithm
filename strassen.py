import time
from math import log2

# Matrix Operations
def shape(matrix):
    return [len(matrix), len(matrix[0])]

def multiply_matrix(matrix1, matrix2):
    multipliedMatrix = []
    n = shape(matrix1)[0]
    m,p = shape(matrix2)

    for i in range(n):
        arr = []

        for j in range(p):
            arr.append(0)
            for k in range(m):
                arr[j] += matrix1[i][k] * matrix2[k][j]
                
        multipliedMatrix.append(arr)

    return multipliedMatrix

def matrix_operation(matrix1, matrix2, operation, size=None):
    if(size is None): 
        lines, columns = shape(matrix1)
    else: lines, columns = size

    finalMatrix = []

    for line in range(lines):
        arr = []

        for column in range(columns):
            arr.append(operation(matrix1[line][column], matrix2[line][column]))

        finalMatrix.append(arr)
    
    return finalMatrix

def add_matrix(matrix1, matrix2, size=None):
    return matrix_operation(matrix1, matrix2, lambda x,y: x+y, size)

def sub_matrix(matrix1, matrix2, size=None):
    return matrix_operation(matrix1, matrix2, lambda x,y: x-y, size)


def pad_columns(matrix, numColumns, value=0):
    array = [value for i in range(numColumns)]

    for line in matrix: line += array
    
    return matrix

def pad_lines(matrix, numColumns, numLines, value=0):
    array = [[value for i in range(numColumns)]]

    for _ in range(numLines): matrix += array
    
    return matrix

def get_pad_value(value):
    exponent = log2(value)

    if(exponent != int(exponent)):
        exponent = int(exponent+1)
        return 2**exponent - value
    else: return 0

def pad_matrix_2n(matrix, matrixShape=None):
    if(matrixShape is None): lines, columns = shape(matrix)
    else: lines, columns = matrixShape

    if(lines == columns):
        padValue = get_pad_value(lines)
        if(padValue != 0):
            matrix = pad_lines(pad_columns(matrix, padValue), columns+padValue, padValue)
    else:
        columnsPad = get_pad_value(columns)
        linesPad = get_pad_value(lines)

        if(columnsPad != 0): matrix = pad_columns(matrix, columnsPad)
        if(linesPad != 0): matrix = pad_lines(matrix, columns, linesPad)

    return matrix

def remove_column_pad(matrix, numLines, numColumns):
    for i in range(numLines):
        matrix[i] = matrix[i][0:numColumns]

    return matrix
    
def remove_line_pad(matrix, numLines):
    return matrix[0:numLines]

# Strassen Algorithm
def get_subArrays(matrix, size, half):
    subArrays = []
    lineIndex = 0

    for _ in range(2):
        firstHalf = []
        lastHalf = []

        for _ in range(half):
            matrixLine = matrix[lineIndex]
            firstHalf.append(matrixLine[0:half])
            lastHalf.append(matrixLine[half:])

            lineIndex += 1

        subArrays.append(firstHalf)
        subArrays.append(lastHalf)

    return subArrays

def get_parts(matrix1, matrix2, size, half=None):
    if(half is None): half = int(size/2)
    matrixSize = [half, half]
    abcd = get_subArrays(matrix1, size, half)
    efgh = get_subArrays(matrix2, size, half)

    p1 = _strassen(abcd[0], sub_matrix(efgh[1], efgh[3], matrixSize), half)
    p2 = _strassen(add_matrix(abcd[0], abcd[1], matrixSize), efgh[3], half)
    p3 = _strassen(add_matrix(abcd[2], abcd[3], matrixSize), efgh[0], half)
    p4 = _strassen(abcd[3], sub_matrix(efgh[2], efgh[0], matrixSize), half)
    p5 = _strassen(add_matrix(abcd[0], abcd[3], matrixSize), add_matrix(efgh[0], efgh[3], matrixSize), half)
    p6 = _strassen(sub_matrix(abcd[1], abcd[3], matrixSize), add_matrix(efgh[2], efgh[3], matrixSize), half)
    p7 = _strassen(sub_matrix(abcd[0], abcd[2], matrixSize), add_matrix(efgh[0], efgh[1], matrixSize), half)

    return [p1, p2, p3, p4, p5, p6, p7]

def get_final_parts(parts, size):
    lines = columns = size
    finalParts = [[],[],[],[]]

    for line in range(lines):
        sum1 = []
        sum2 = []
        sum3 = []
        sum4 = []

        for column in range(columns):
            sum1.append(parts[4][line][column]+parts[3][line][column]-parts[1][line][column]+parts[5][line][column])
            sum2.append(parts[0][line][column]+parts[1][line][column])
            sum3.append(parts[2][line][column]+parts[3][line][column])
            sum4.append(parts[0][line][column]+parts[4][line][column]-parts[2][line][column]-parts[6][line][column])
        
        finalParts[0].append(sum1)
        finalParts[1].append(sum2)
        finalParts[2].append(sum3)
        finalParts[3].append(sum4)

    return finalParts

def flat_matrix(parts, size):
    lines = size
    upperArray = []
    lowerArray = []

    for line in range(lines):
        upperArray.append(parts[0][line] + parts[1][line])
        lowerArray.append(parts[2][line] + parts[3][line])
    
    return upperArray + lowerArray

def _strassen(matrix1, matrix2, size=None):
    if(size is None): size = shape(matrix1)[0]

    if(size <= 64):
        return multiply_matrix(matrix1, matrix2)
    else:
        half = int(size/2)
        return flat_matrix(get_final_parts(get_parts(matrix1, matrix2, size, half), half), half)

def strassen_multiplication(matrix1, matrix2, size=None):
    matrix1Shape = shape(matrix1)
    matrix2Shape = shape(matrix2)

    if(matrix1Shape[1] == matrix2Shape[0]):
        if(matrix1Shape == matrix2Shape):
            matrix1 = pad_matrix_2n(matrix1, matrix1Shape)
            matrix2 = pad_matrix_2n(matrix2, matrix2Shape)

            matrix = _strassen(matrix1, matrix2)
            matrixShape = shape(matrix)

            if(matrix1Shape[0] != matrixShape[0]): matrix = remove_line_pad(matrix, matrix1Shape[0])
            if(matrix2Shape[1] != matrixShape[1]): matrix = remove_column_pad(matrix, matrix1Shape[0], matrix2Shape[1]) 
            
            return matrix
        else: raise Exception("Only works with same dimension matrices!")
    else: raise Exception("Invalid matrices!")