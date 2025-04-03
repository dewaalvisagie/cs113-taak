import stdarray
import sys
import stdio
# size =  int(input("Size of pattern"))
# size = 5

# ______________________________Print QR______________________________
def printQR(pospattern):
    for i in range(len(pospattern)):
        for j in range(len(pospattern)):
            stdio.write(str(pospattern[i][j])+" ")
        stdio.writeln()
    
# ______________________________Validation Checks______________________________



def validateInput(Encodingparm, sizeOfQRCode, sizeOfPospat, sizeOfAlignmentPat):
    #________ValidatingSizeOfQRCode___________
    if Encodingparm == None or sizeOfQRCode == None or sizeOfPospat == None or sizeOfAlignmentPat == None:
        stdio.writeln("ERROR: Too few arguments")
        return False
    expectedargs = 4
    if len(sys.argv) != expectedargs+1:
        stdio.writeln("ERROR: Too many arguments")
        return False
    if sizeOfQRCode<10 or sizeOfQRCode>48:
        stdio.writeln("ERROR: Invalid size argument: "+str(sizeOfQRCode))
        return False
    
    #________Validatingsizeofpospat______________
    if sizeOfPospat < 4 or sizeOfPospat % 2 != 0:
        stdio.writeln("ERROR: Invalid position pattern size argument: " + str(sizeOfPospat))
        return False
    if sizeOfPospat > sizeOfQRCode:
        stdio.writeln("ERROR: Position pattern size is too large for QR code size")
        return False
    #__________Validating sizeofallignmentpattern_____________
    if sizeOfAlignmentPat < 1 or (sizeOfAlignmentPat - 1) % 4 != 0: #not in the patttern 1 5 9 13 ...
        return False
    
    

    if Encodingparm<0 or Encodingparm>32:
        stdio.writeln("ERROR: Invalid encoding argument: "+str(encodingparm))
        return False
    return True
# __________________________Build QR components______________________

#__________________________Making the snake pattern______________________________




# This is the main function that generates the 
# pospat for the QR code
def genBasePosPat(inputArray, n):
    offset = n - 4
    if offset < 0:
        offset = 0
    if n >= 6:
        offset = countUnevenAfter5(n)

    for i in range(len(inputArray)):
        for j in range(len(inputArray)):
            if i == 3 or j == 3:
                inputArray[i + offset][j + offset] = 0
            elif i < 4 and j < 4:
                inputArray[i + offset][j + offset] = 1

    return inputArray  # Ensure the function returns the modified array
    
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
    baseVal = 4
    pospattern = stdarray.create2D(baseVal,baseVal,0)
    currentPosPat = genBasePosPat(pospattern,baseVal)

    for i in range(5, n+1):
        if (i % 2) == 0:
            currentPosPat = buildRight(currentPosPat)
        else:
            currentPosPat = buildLeft(currentPosPat)

    return currentPosPat

def MakeCleanQR(size):
    CleanQR = stdarray.create2D(size,size,0) #Makes a clean array of size n that we are going to populate with the other elements.
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

def addPospatToQR(size , n, alsize):
    pospat = buildToTargetPosPat(n)  # n is the size of the position pattern. size is the size of the QR code.
    pospatpopRight = MakeCleanQR(size)#makes a clean qr code of the correct size.
    j = 0
    i = 0  
    # TopLeft
    for i in range(len(pospat)):
        for j in range(len(pospat)):
            pospatpopRight[i][j] = pospat[i][j]#hier is waar die fout le.
    
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

# __________________End of QR component generation______________________

def MakeAlignmentPattern(alpatsize):

    Alignmentpat = stdarray.create2D(alpatsize, alpatsize, 1)  # Initialize with 1s

    # Create alternating square pattern
    for layer in range(1, alpatsize // 2, 2):  # Step by 2 to maintain the pattern
        for i in range(layer, alpatsize - layer):
            for j in range(layer, alpatsize - layer):
                if (i == layer or i == alpatsize - layer - 1 or
                    j == layer or j == alpatsize - layer - 1):
                    Alignmentpat[i][j] = 0

    return Alignmentpat
        
# Main is only for testing
if __name__ == "__main__":
    if len(sys.argv) != 5:
        stdio.writeln("ERROR: Incorrect number of arguments. Usage: python script.py <encodingparm> <sizeOfQRCode> <sizeOfPospat> <sizeOfAlignmentPat>")
        sys.exit(1)

    encodingparm = int(sys.argv[1])
    sizeOfQRCode = int(sys.argv[2])
    sizeOfPospat = int(sys.argv[3])
    sizeOfAlignmentPat = int(sys.argv[4])

    stdio.writeln(encodingparm)

    if not validateInput(encodingparm, sizeOfQRCode, sizeOfPospat, sizeOfAlignmentPat):
        sys.exit(1)
    else:
        printQR(addPospatToQR(sizeOfQRCode,sizeOfPospat, sizeOfAlignmentPat))  # Corrected order
    
