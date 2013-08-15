import numpy as np
import qPCR_abi as qa

with open("data.txt","r") as f:
    lines=f.readlines()
    header=lines.pop(0)

    data_lines=[]
    for line in lines:
        newline=line.split('\t')
        if len(newline) > 5: #to get rid of general information lines
            data_lines.append(newline)

plate = qa.create_plate(24)
#creates a dictionary where each element responds to a row of a 16x24 plate
#{"row letter":[list of values in this row], ...}


for line in data_lines[1:]:
    row_letter = line[1][0] # line[1] == "A1"
    column_number = int(line[1][1:])
    Ct = line[5]
    plate[row_letter][column_number-1] = Ct


plate_tri = qa.create_plate(8)
#Number of columns after analyzing triplicates is reduced three times

for row in plate:
    for columns in range(0,25,3):
        triplicate = plate[row][columns:columns+3]
        if len(triplicate) == 3:
            plate_tri[row][columns/3] = qa.analyze_triplicate(triplicate)


#print plate_tri["A"][2]
qa.pp(plate_tri, arg = 6)
#qa.pp(plate)





