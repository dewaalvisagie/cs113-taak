import stdarray
import sys
import stdio
# size =  int(input("Size of pattern"))
# size = 5

def printQR(pospattern):
    for i in range(len(pospattern)):
        for j in range(len(pospattern)):
            stdio.write(str(pospattern[i][j])+" ")
        stdio.writeln()
    


def checkValidPosPat(size):
    if size < 4:
        errormessage = "ERROR: Invalid position pattern size argument: " + str(size)
        #stdio.writeln(errormessage)
        return False

    else:
        return True

# This is the main function that generates the 
# pospat for the QR code
def genBasePosPat(inputArray,n):
    # to account for offset:
   if checkValidPosPat(n) :
        offset = n - 4
        if offset < 0:
            offset = 0

        if n >= 6:
            offset = countUnevenAfter5(n)

        for i in range(len(inputArray)):
            for j in range(len(inputArray)):
                if(i == 3 or j == 3):
                    inputArray[i+offset][j+offset] = 0
                elif(i < 4 and j < 4) : 
                    inputArray[i+offset][j+offset] = 1
                if(i == 3 and j == 3):
                    return inputArray  
    
# this function is used to determine the offset of the position pattern
def countUnevenAfter5(target):
    offset = 0
    for i in range(5, target+1):
        if(i % 2 != 0):
            # print(i)
            offset = offset + 1

    # print("The offset is:" + str(offset))
    return offset


# This function takes a position pattern and adds a 
# "layer to the onion on the left hand side"
def buildLeft(inputArray):

    # logic for determining what value to build with
    buildwith = 2
    if (countUnevenAfter5(len(inputArray)+1) % 2) == 0 :
        # should build with 1's
        buildwith = 1
    else:
        # should build with 0's
        buildwith = 0

    newArray = stdarray.create2D(len(inputArray)+1, len(inputArray)+1, buildwith)
    moveDiag = 1
    # import previous array:
    for i in range(len(inputArray)):
        for j in range(len(inputArray)):
            newArray[i+moveDiag][j+moveDiag] = inputArray[i][j]

    return newArray

# This function takes a position pattern and adds a 
# "layer to the onion on the right hand side"
def buildRight(inputArray):
    buildwith = 2
    
    if (int((len(inputArray)+1) / 2) % 2) == 1 :
        # should build with 1's
        buildwith = 1
    else:
        # should build with 0's
        buildwith = 0
        
   # print("buildwith is: ",int((len(inputArray)+1) / 2))
    newArray = stdarray.create2D(len(inputArray)+1, len(inputArray)+1, buildwith)
    # import previous array:
    for i in range(len(inputArray)):
        for j in range(len(inputArray)):
            newArray[i][j] = inputArray[i][j]

    return newArray

def buildToTargetPosPat(n):
   
    if not checkValidPosPat(n):
        return
    
    baseVal = 4
    pospattern = stdarray.create2D(baseVal,baseVal,0)
    currentPosPat = genBasePosPat(pospattern,baseVal)

    for i in range(5, n+1):
        if (i % 2) == 0:
            currentPosPat = buildRight(currentPosPat)
        else:
            currentPosPat = buildLeft(currentPosPat)

    return currentPosPat


#printQR(buildToTargetPosPat(7))
#buildtotargetPospat is die final pos pattern wat jy moet insert orals.
def MakeCleanQR(size):
    CleanQR = stdarray.create2D(size,size,0)#Makes a clean array of size n that we are going to populate with the other elements.
    return CleanQR

def reflect_x_axis(matrix):
    """Reflects an nxn 2D array along the x-axis using only array operations."""
    n = len(matrix)
    reflected = stdarray.create2D(n, n, 0)  # Create an empty nxn array

    for i in range(n):
        for j in range(n):
            reflected[i][j] = matrix[n - 1 - i][j]  # Swap rows

    return reflected

def reflect_y_axis(matrix):
    """Reflects an nxn 2D array along the y-axis using only array operations."""
    n = len(matrix)
    reflected = stdarray.create2D(n, n, 0)  # Create an empty nxn array

    for i in range(n):
        for j in range(n):
            reflected[i][j] = matrix[i][n - 1 - j]  # Swap columns

    return reflected

def addPospatToQR(n, size, alsize):
    pospat = buildToTargetPosPat(n)  # n is the size of the position pattern. size is the size of the QR code.
    pospatpopRight = MakeCleanQR(size)
    # if not checkifalpatisbiggerthanqrcode(alsize,size):
    #     return "ERROR: Invalid alignment pattern size argument"+str(alsize)
    # sys.exit(1)
      
    # TopLeft
    for i in range(len(pospat)):
        for j in range(len(pospat)):
            pospatpopRight[i][j] = pospat[i][j]
    
    prev_postpat = pospat
    pospat = reflect_x_axis(pospat)
    
    # Bottom left
    for i in range(len(pospat)):
        for j in range(len(pospat)):
            pospatpopRight[len(pospatpopRight) - len(pospat) + i][j] = pospat[i][j]  

    pospat = prev_postpat
    pospat = reflect_y_axis(pospat)
    
    # Top right
    for i in range(len(pospat)):
        for j in range(len(pospat)):
            pospatpopRight[i][len(pospatpopRight) - len(pospat) + j] = pospat[i][j]

    # ADD THE ALIGNMENT PATTERN TO THE CORRECT POSITION
    alignmentpat = MakeAlignmentPattern(alsize)
    start_x = size - n - 1
    start_y = size - n - 1

    for i in range(alsize):
        for j in range(alsize):
            pospatpopRight[start_x + i][start_y + j] = alignmentpat[i][j]

    return pospatpopRight  # Return the updated QR array
def is_valid_alignment_size(size):
    if size < 1:
        return False  # The sequence starts at 1

    n = (size + 3) / 4  # Solving for n in T_n = 4n - 3

    return n.is_integer()  # Valid if n is a whole number
# def checkifalpatisbiggerthanqrcode(sizeofallpat,sizeofQRcode):
#     if sizeofallpat>sizeofQRcode:#alignment pattern bigger than the qr code
#         return False
#     else:
#         return True

def MakeAlignmentPattern(alpatsize):
    
    # if not is_valid_alignment_size(alpatsize):
    #     return "ERROR: Invalid alignment pattern size argument: " + str(alpatsize)
    #     sys.exit(1)
    # if not checkifalpatoverlapswithpospat(alpatsize):
    #     return "ERROR: Alignment/position pattern out of bounds"
    #     sys.exit(1)

    Alignmentpat = stdarray.create2D(alpatsize, alpatsize, 1)  # Initialize with 1s

    # Create alternating square pattern
    for layer in range(1, alpatsize // 2, 2):  # Step by 2 to maintain the pattern
        for i in range(layer, alpatsize - layer):
            for j in range(layer, alpatsize - layer):
                if (i == layer or i == alpatsize - layer - 1 or
                    j == layer or j == alpatsize - layer - 1):
                    Alignmentpat[i][j] = 0

    return Alignmentpat




# def checkifalpatoverlapswithpospat(sizeofAllPat,sizeofQRcode,sizeofpospat):
#     if  (sizeofQRcode - sizeofpospat - 1) < 0 or (sizeofQRcode - sizeofAllPat - 1) < 0:#alignment pattern overlaps with th e
#         return False
        
def print_pattern(pattern):
    for row in pattern:
        for value in row:
            stdio.write(value)
            stdio.write(" ")  # Add space between values
        stdio.writeln()
# Main is only for testing
if __name__ == "__main__":
    sizeofpospat = int(sys.argv[1])
    sizeofQRcode = int(sys.argv[2])
    sizeofAllPat = int(sys.argv[3])
    
    stdio.writeln(sizeofpospat)
    printQR(addPospatToQR(sizeofpospat,sizeofQRcode,sizeofAllPat))
    




