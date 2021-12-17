# //     Karnaugh.py                                 //
# //     Program for the Karnaugh-Veitch-chart       //
# //     Version 1.0, 28/11/2021                     //

# --------------------------------------------------------------------------------------------------


# function that takes the input and prints the MINTERMs

def inputL(inp):
    index = int(0)  # number of + in the input
    inpList = []  # list for output (based on input)
    inp = inp + '0'  # input becomes 0 as an end-mark
    for i in range(len(inp)):  # determines the number of + in the input
        if (inp[i] == '+'):
            index = index + 1
    j = 0
    for i in range(index + 1):  # gets the terms
        temp = ""  # temporary string (term)
        while (inp[j] != '+' and inp[j] != '0'):  # if input[i] is not + and not 0
            temp = temp + inp[j]  # temporary string updated
            j = j + 1  # next position
        inpList.append(temp)  # the temporary string gets appended
        j = j + 1
    inpList = list(dict.fromkeys(inpList))  # removes duplicates (because they're not needed)
    return inpList  # returns the list of terms


# --------------------------------------------------------------------------------------------------


# inserts the 1's into the KV-chart

def insert(inpList):
    table = [[], [], [], [], []]  # table --> output
    for i in range(4):
        for j in range(4):
            table[i].append(0)  # initializes all table-elements with 0

    for i in range(len(inpList)):  # takes all elements

        for z in range(4):  # 1 is always one
            for x in range(4):
                if table[z][x] == 1:  # if the value is bigger or equal --> 1
                    table[z][x] = 1 + 4  # -->4 (max. length) was added to make sure that this 1 still will be in the output
                else:
                    table[z][x] = 0

        for j in range(len(inpList[i])):  # takes all characters of the elements

            count = 0  # counts the number of variables in the term

            for z in range(len(inpList[i])):
                if inpList[i][z] == "a" or inpList[i][z] == "b" or inpList[i][z] == "c" or inpList[i][z] == "d":
                    count = count + 1

            # for a and -a

            if inpList[i][j] == "a" and inpList[i][j - 1] != "-":  # proves if the element is a
                for z in range(4):
                    for x in range(2):
                        table[z][x] = table[z][x] + 1  # adds 1 to the elements of a
            elif inpList[i][j] == "-" and inpList[i][j + 1] == "a":  # proves if the element is -a
                for z in range(4):
                    for x in range(2):
                        table[z][x + 2] = table[z][x + 2] + 1  # adds 1 to the elements of -a

            # for b and -b

            if inpList[i][j] == "b" and inpList[i][j - 1] != "-":  # proves if the element is b
                for z in range(2):
                    for x in range(4):
                        table[z][x] = table[z][x] + 1  # adds 1 to the elements of b
            elif inpList[i][j] == "-" and inpList[i][j + 1] == "b":  # proves if the element is -b
                for z in range(2):
                    for x in range(4):
                        table[z + 2][x] = table[z + 2][x] + 1  # adds 1 to the elements of -b

            # for c and -c

            if inpList[i][j] == "c" and inpList[i][j - 1] != "-":  # proves if the element is c
                for z in range(2):
                    for x in range(4):
                        table[z + 1][x] = table[z + 1][x] + 1  # adds 1 to the elements of c
            elif inpList[i][j] == "-" and inpList[i][j + 1] == "c":  # proves if the element is -c
                for x in range(4):
                    table[0][x] = table[0][x] + 1  # adds 1 to the elements of -c
                for x in range(4):
                    table[3][x] = table[3][x] + 1

            # for d and -d

            if inpList[i][j] == "d" and inpList[i][j - 1] != "-":  # proves if the element is d
                for z in range(4):
                    table[z][1] = table[z][1] + 1  # adds 1 to the elements of d
                for z in range(4):
                    table[z][2] = table[z][2] + 1  # adds 1 to the elements of d
            elif inpList[i][j] == "-" and inpList[i][j + 1] == "d":  # proves if the element is -d
                for z in range(4):
                    table[z][0] = table[z][0] + 1  # adds 1 to the elements of d
                for z in range(4):
                    table[z][3] = table[z][3] + 1  # adds 1 to the elements of d

        for z in range(4):  # sets everything thats >1 to 1
            for x in range(4):
                if table[z][x] >= count:  # if the value is bigger or equal --> 1
                    table[z][x] = 1
                else:
                    table[z][x] = 0

    table[4] = table[0];  # edited table
    for z in range(4):
        table[z].append(table[z][0])

    return table


# --------------------------------------------------------------------------------------------------


# gets the terms for the output

def getTerms(table):
    temp = ""
    out = []

    # if everything is 1
    if getTrue(table, 0, 4, 0, 4) == 1:
        out.append("1")
        return out

    anyOne = 0
    # if everything is 0
    for i in range(4):
        for j in range(4):
            if table[i][j] == 1:
                anyOne = 1
    if (anyOne == 0):
        out.append("0")
        return out

    # for the 8-blocks
    ind8c = {'02': 'a', '13': 'd', '24': '-a', '35': '-d'}  # indices: rows-columns
    for z in range(4):
        if getTrue(table, 0, 4, z, z + 2) == 1:
            temp = str(z) + str(z + 2)
            table = incre(table, 0, 4, z, z + 2)
            if temp == '02':
                table = incre(table, 0, 4, 0, 2)
                table = incre(table, 0, 4, 4, 5)
            elif temp == '35':
                table = incre(table, 0, 4, 0, 1)
                table = incre(table, 0, 4, 4, 5)
            out.append(ind8c[temp])

    ind8r = {'02': 'b', '13': 'c', '24': '-b', '35': '-c'}  # indices: rows-columns
    for z in range(4):
        if getTrue(table, z, z + 2, 0, 4) == 1:
            temp = str(z) + str(z + 2)
            table = incre(table, z, z + 2, 0, 5)
            out.append(ind8r[temp])

    # swaps variables if d is used
    for i in range(len(out)):
        if (out[i] == 'd' or out[i] == '-d'):
            temp = out[i]
            for z in range(i, len(out) - 1):
                out[z] = out[z + 1]
            out[len(out) - 1] = temp

    # for the 4-blocks (squares)
    # indices: rows-columns
    ind4s = {'11': 'ab', '12': 'bd', '13': '-ab', '14': 'b-d', \
             '21': 'ac', '22': 'cd', '23': '-ac', '24': 'c-d', \
             '31': 'a-b', '32': '-bd', '33': '-a-b', '34': '-b-d', \
             '41': 'a-c', '42': '-cd', '43': '-a-c', '44': '-c-d'}  # 44 is special case!

    for z in range(4):
        for x in range(4):
            if getTrue(table, x, x + 2, z, z + 2) == 1:
                temp = str(x + 1) + str(z + 1)
                table = incre(table, x, x + 2, z, z + 2)
                out.append(ind4s[temp])
            if temp == '11':
                table = incre(table, 0, 2, 4, 5)
            elif temp == '21':
                table = incre(table, 1, 3, 4, 5)
            elif temp == '31':
                table = incre(table, 2, 4, 4, 5)
            elif temp == '41':
                incre(table, 3, 5, 4, 5)

    # for the 4-blocks (rectangles)
    ind4r = {'03': 'b-c', '13': 'bc', '23': '-bc', '33': '-b-c'}
    ind4c = {'30': 'a-d', '31': 'ad', '32': '-ad', '33': '-a-d'}
    for z in range(4):
        if getTrue(table, z, z + 1, 0, 4) == 1:
            temp = str(z) + str(3)
            table = incre(table, z, z + 1, 0, 5)
            out.append(ind4r[temp])
    for z in range(4):
        if getTrue(table, 0, 4, z, z + 1) == 1:
            temp = str(3) + str(z)
            table = incre(table, 0, 5, z, z + 1)
            out.append(ind4c[temp])

    # for the 2-blocks (side)
    ind2s = {'01': 'ab-c', '02': 'b-cd', '03': '-ab-c', '04': 'b-c-d',
             '11': 'abc', '12': 'bcd', '13': '-abc', '14': 'bc-d',
             '21': 'a-bc', '22': '-bcd', '23': '-a-bc', '24': '-bc-d',
             '31': 'a-b-c', '32': '-b-cd', '33': '-a-b-c', '34': '-b-c-d'}
    for z in range(4):
        for x in range(4):
            if getTrue(table, z, z + 1, x, x + 2) == 1:
                temp = str(z) + str(x + 1)
                table = incre(table, z, z + 1, x, x + 2)
                if (
                        temp == '04' or temp == '14' or temp == '24' or temp == '34'):  # addionally incremented (because 5th column)
                    incre(table, z, z + 1, 0, 1);
                table = incre(table, z, z + 1, 4, 5)
                out.append(ind2s[temp])

    # for the 2-blocks (down)
    ind2d = {'10': 'ab-d', '20': 'ac-d', '30': 'a-b-d', '40': 'a-c-d',
             '11': 'abd', '21': 'acd', '31': 'a-bd', '41': 'a-cd',
             '12': '-abd', '22': '-acd', '32': '-a-bd', '42': '-a-cd',
             '13': '-ab-d', '23': '-ac-d', '33': '-a-b-d', '43': '-a-c-d'}
    for z in range(4):
        for x in range(4):
            if getTrue(table, z, z + 2, x, x + 1):
                temp = str(z + 1) + str(x)
                table = incre(table, z, z + 2, x, x + 1)
                if (
                        temp == '10' or temp == '20' or temp == '30' or temp == '40'):  # addionally incremented (because 5th column)
                    incre(table, z, z + 2, 4, 5)
                out.append(ind2d[temp])

    # for the left 1-blocks
    ind1 = {'00': 'ab-c-d', '01': 'ab-cd', '02': '-ab-cd', '03': '-ab-c-d',
            '10': 'abc-d', '11': 'abcd', '12': '-abcd', '13': '-abc-d',
            '20': 'a-bc-d', '21': 'a-bcd', '22': '-a-bcd', '23': '-a-bc-d',
            '30': 'a-b-c-d', '31': 'a-b-cd', '32': '-a-b-cd', '33': '-a-b-c-d'}
    for z in range(4):
        for x in range(4):
            if table[z][x] == 1:
                temp = str(z) + str(x)
                out.append(ind1[temp])

    return out


# --------------------------------------------------------------------------------------------------


# checks if a given area has at least one 1

def getTrue(table, start, rows, cstart, columns):
    one = int(0)
    for z in range(start, rows):
        for x in range(cstart, columns):
            if (table[z][x]) == 1:
                one = int(1)
            if (table[z][x]) == 0:
                return 0
    return one


# --------------------------------------------------------------------------------------------------


# increments a given area

def incre(table, start, rows, cstart, columns):
    for z in range(start, rows):
        for x in range(cstart, columns):
            if (table[z][x]) == 1:
                table[z][x] += 1
    return table


# --------------------------------------------------------------------------------------------------

def main(input):
    list = inputL(str(input))
    table = insert(list)
    out = getTerms(table)
    return out


# --------------------------------------------------------------------------------------------------

def retTable(input):
    list = inputL(str(input))
    table = insert(list)
    return table
