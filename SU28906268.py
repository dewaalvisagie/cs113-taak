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
#checks to see if the inputted values from user is a string or int and if its not it gives an error
def isinteger(value):
    try:
        int(value)  # Try converting to an integer
        return True
    except ValueError:
        return False

#validates all possible negative inputs from the user and gives outputs regarding that.
def validateInput(Encodingparm, sizeOfQRCode, sizeOfPospat, sizeOfAlignmentPat):
    #________ValidatingSizeOfQRCode___________
    if Encodingparm == None or sizeOfQRCode == None or sizeOfPospat == None or sizeOfAlignmentPat == None:
        stdio.writeln("ERROR: Too few arguments")
        return False
    if not isinteger(Encodingparm):
        stdio.writeln("ERROR: Invalid encoding argument: "+Encodingparm)
        return False
    if not isinteger(sizeOfQRCode):
        stdio.writeln("ERROR: Invalid size argument: "+sizeOfQRCode)
        return False
    if not isinteger(sizeOfPospat):
        stdio.writeln("ERROR: Invalid position pattern size argument: "+sizeOfPospat)
        return False
    if not isinteger(sizeOfAlignmentPat):
        stdio.writeln("ERROR: Invalid alignment pattern size argument: "+sizeOfAlignmentPat)
        return False
    # making the variables ints so other validations can happen 
    Encodingparm = int(Encodingparm)
    sizeOfQRCode = int(sizeOfQRCode)
    sizeOfAlignmentPat= int(sizeOfAlignmentPat)
    sizeOfPospat = int(sizeOfPospat)
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
        stdio.writeln("ERROR: Invalid position pattern size argument: "+str(sizeOfPospat))
        return False
    if sizeOfPospat*2 >= sizeOfQRCode:
        stdio.writeln("ERROR: Alignment/position pattern out of bounds")
        return False
    #__________Validating sizeofallignmentpattern_____________
    if sizeOfAlignmentPat < 1 or (sizeOfAlignmentPat - 1) % 4 != 0: #not in the patttern 1 5 9 13 ...
        stdio.writeln("ERROR: Invalid alignment pattern size argument: "+str(sizeOfAlignmentPat))
        return False
    if sizeOfAlignmentPat >= sizeOfQRCode:
        stdio.writeln("ERROR: Invalid alignment pattern size argument: "+str(sizeOfAlignmentPat))
        return False
    if sizeOfQRCode - sizeOfPospat - 1 < sizeOfAlignmentPat:
        stdio.writeln("ERROR: Invalid alingment pattern argument: "+str(sizeOfAlignmentPat))
        return False
    start_x = sizeOfQRCode - sizeOfPospat - 1
    start_y = sizeOfQRCode - sizeOfPospat - 1

    if start_x + sizeOfAlignmentPat > sizeOfQRCode or start_y + sizeOfAlignmentPat > sizeOfQRCode:# if the alignment pattern does overlap with any of the pp or goes out of bounds.
        stdio.writeln("ERROR: Invalid alignment pattern arugment: "+str(sizeOfAlignmentPat))
        return False
    
    #___________________Encoding paramater validation______________________________________
    if Encodingparm<0 or Encodingparm>32:
        stdio.writeln("ERROR: Invalid encoding argument: "+str(encodingparm))
        return False
    
    return True

#__________________________Making the snake pattern______________________________
def encode_message(message,sizeOfQRCode,sizeOfPospat,sizeOfAlingmentpats):
    # Step 1: Byte mode indicator (always 0100)
    bit_sequence = "0100"

    # Step 2: Message length (8-bit binary)
    num = len(message)
    length_bits = ""
    for i in range(7, -1, -1):
        length_bits += "1" if (num & (1 << i)) else "0"
    bit_sequence += length_bits

    # Step 3: Convert message to ASCII binary
    for char in message:
        ascii_value = ord(char)
        char_bits = ""
        for i in range(7, -1, -1):
            char_bits += "1" if (ascii_value & (1 << i)) else "0"
        bit_sequence += char_bits

    # Step 4: Terminator pattern (4-bit)
    bit_sequence += "0000"

    # Calculate available space in the QR grid
    

    # Ensure the message fits within the QR code
    if len(bit_sequence) > calculate_available_space(sizeOfQRCode,sizeOfPospat,sizeOfAlignmentPat):
        raise ValueError("Encoded message is too large for the given QR code size!")

    # Step 5: Add padding bits
    padding_bits = ["11101100", "00010001"]
    index = 0
    max_bits = calculate_available_space(sizeOfQRCode, sizeOfPospat, sizeOfAlignmentPat)
    while len(bit_sequence) <= max_bits:  # Only add full padding bytes if space allows
        bit_sequence += padding_bits[index]
        index = 1 - index  
    bit_sequence = bit_sequence[:max_bits] 

    return bit_sequence

def calculate_available_space(qr_size, pos_size, align_size):
    qr_size = int(qr_size)
    pos_size = int(pos_size)
    align_size = int(align_size)
    total_cells = qr_size * qr_size  # Total number of cells in the grid
    
 
    pos_pattern_cells = 3 * (pos_size * pos_size)
    
    
    align_pattern_cells = align_size * align_size
    
    # Available space for encoding
    available_cells = total_cells - (pos_pattern_cells + align_pattern_cells)
    
    return available_cells

def insert_snake_pattern(qr_matrix, bit_sequence):
    gridsize = len(qr_matrix)
    tracker = 0
    for row in range(gridsize):
        if row %2 == 0 :# even rows from left to right
            for col in range(gridsize):
                if qr_matrix[row][col] == 2 and tracker < len(bit_sequence):
                    qr_matrix[row][col] = bit_sequence[tracker]
                    tracker += 1
        else:
            for col in range(gridsize-1,-1,-1):
                if qr_matrix[row][col] == 2 and tracker<len(bit_sequence):
                    qr_matrix[row][col] = bit_sequence[tracker]
                    tracker +=1
    return qr_matrix

    


#_________________________Finished with the snake pattern______________________________






# __________________________Build QR components______________________

# This is the main function that generates the 
# pospat for the QR code
def genBasePosPat(inputArray, n):
    n = int(n)
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
    target = int(target)
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
    n  = int(n)
    baseVal = 4
    pospattern = stdarray.create2D(baseVal,baseVal,0)
    currentPosPat = genBasePosPat(pospattern,baseVal)
    n = int(n)
    for i in range(5, n+1):
        if (i % 2) == 0:
            currentPosPat = buildRight(currentPosPat)
        else:
            currentPosPat = buildLeft(currentPosPat)

    return currentPosPat

def MakeAlignmentPattern(alpatsize):
    alpatsize = int(alpatsize)
    Alignmentpat = stdarray.create2D(alpatsize, alpatsize, 1)  # Initialize with 1s

    # Create alternating square pattern
    for layer in range(1, alpatsize // 2, 2):  # Step by 2 to maintain the pattern
        for i in range(layer, alpatsize - layer):
            for j in range(layer, alpatsize - layer):
                if (i == layer or i == alpatsize - layer - 1 or
                    j == layer or j == alpatsize - layer - 1):
                    Alignmentpat[i][j] = 0

    return Alignmentpat

def MakeCleanQR(size):
    size = int(size)
    
    CleanQR = stdarray.create2D(size,size,2) #Makes a clean array of size n that we are going to populate with the other elements.
    return CleanQR

def reflect_x_axis(array):
    
    n = len(array)
    reflected = stdarray.create2D(n, n, 0)  # Create an empty nxn array

    for i in range(n):
        for j in range(n):
            reflected[i][j] = array[n - 1 - i][j]  # Swap rows

    return reflected

def reflect_y_axis(array):
    
    n = len(array)
    reflected = stdarray.create2D(n, n, 0)  # Create an empty nxn array

    for i in range(n):
        for j in range(n):
            reflected[i][j] = array[i][n - 1 - j]  # Swap columns

    return reflected

def addPospatToQR(size , n, alsize):
    
    size = int(size)
    n = int(n)
    alsize = int(alsize)
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


        
# Main is only for testing
if __name__ == "__main__":
    if len(sys.argv) < 5:
        stdio.writeln("ERROR: Too few arguments ")
        sys.exit(1)
    if len(sys.argv) > 5:
        stdio.writeln("ERROR: Too many arguments ")
        sys.exit(1)
    encodingparm = sys.argv[1]
    sizeOfQRCode = sys.argv[2]
    sizeOfPospat = sys.argv[3]
    sizeOfAlignmentPat = sys.argv[4]
    
    message = "123456"

    

    if not validateInput(encodingparm, sizeOfQRCode, sizeOfPospat, sizeOfAlignmentPat):
        sys.exit(1)
        # pass
    else:
        encodingparm = int(encodingparm)
        sizeOfQRCode = int(sizeOfQRCode)
        sizeOfPospat = int(sizeOfPospat)
        sizeOfAlignmentPat= int(sizeOfAlignmentPat)
        
        #printQR(InsertSnakeIntoQR(addPospatToQR(sizeOfQRCode,sizeOfPospat, sizeOfAlignmentPat),encode_message(message,sizeOfQRCode,sizeOfPospat,sizeOfAlignmentPat),sizeOfPospat,sizeOfAlignmentPat,sizeOfQRCode))  # Corrected order
        bitsequence  = encode_message(message,sizeOfQRCode,sizeOfPospat,sizeOfAlignmentPat)
        QRCodewithoutsnake = addPospatToQR(sizeOfQRCode,sizeOfPospat,sizeOfAlignmentPat)
        pospat = buildToTargetPosPat(sizeOfPospat)
        alpat = MakeAlignmentPattern(sizeOfAlignmentPat)
        #stdio.writeln(bitsequence)
        printQR(insert_snake_pattern(QRCodewithoutsnake,bitsequence))