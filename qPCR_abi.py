import numpy as np
import string


def create_plate(nr_of_columns):
    plate = {}
    letters="ABCDEFGHIJKLMNOP"
    for row in letters:
        plate[row] = []
        for column in range(1,nr_of_columns+1):
            plate[row].append(0)
    return plate

def pp(plate,**kw):
    #prints out values of a plate, one row at a time,
    #or only one value from each list if additional arguments are given
    if kw:
        for row in plate:
            accumulator = []
            for element in plate[row]:
                accumulator.append(element[kw["arg"]])
            print accumulator
    else:
        for row in plate:
            print row, plate[row]

def test_value(value):
    try:
        result = float(value)
        if result != 0:
            return result
        else:
            return ""
    except:
        return ""

def calculate(values,fn):
   for i in values:
       if i:
           continue
       else:
           return ""
   return fn(values)

def analyze_triplicate(triplicate, allowed_std = 0.5 ,std_difference = 2):
    # get's triplicate data (three Ct values), returns list of elements:
    # 0. Average of three ("", if some values are missing)
    # 1. Standard deviation of three ("", if some values are missing)
    # 2. Average of best pair ("", if not possible)
    # 3. Standard deviation of best pair
    # 4. Existing values
    # 5. Values taken into account
    # 6. Final average (see details below)
    # 7. Final std
    # 8. list of all the values in triplicate

    a,b,c = triplicate
    a,b,c = map(test_value,[a,b,c])

    existing_values = ""
    if a: existing_values += "A"
    if b: existing_values += "B"
    if c: existing_values += "C"

    if a and b and c:
        #if all three values are present find average of three and standard deviation
        av3 = round(calculate([a,b,c],np.average),2)
        std3 = round(calculate([a,b,c],np.std),2)

        #find averages and standard deviations for all the possible pairs
        pairs = [a,b], [a,c], [b,c]
        pairs_av = [round(calculate(x,np.average),2) for x in pairs]
        pairs_std = [round(calculate(x,np.std),2) for x in pairs]
        pairs_combined = zip(pairs_std,pairs_av,["ab","ac","bc"])

        #sort pairs based on standard deviations (first element in list)
        pairs_combined = sorted(pairs_combined)
        std2, av2, pair_vtia = pairs_combined[0]

    else:
        #if some values from the triplicate are missing do the following
        av3, std3 = "", ""
        pair_dict = {"AB":[a,b], "AC":[a,c], "BC":[b,c]}
        if existing_values in pair_dict:
            #if two values are present
            av2 = round(np.average(pair_dict[existing_values]),2)
            std2 = round(np.std(pair_dict[existing_values]),2)
        else:
            #if more than one value is missing, then set values to "":
            av2, std2 = ["",""]


#Following code is necessary to find final average and std and values taken into account
    if existing_values == "ABC":
        #if all three values are present
        if std3 < allowed_std:
            final_av, final_std, vtia = av3, std3, "abc"
        elif std2 < allowed_std and std3/std_difference > std2:
            final_av, final_std, vtia = av2, std2, pair_vtia
        else:
            final_av, final_std, vtia = "", "", ""
    elif av2:
        if std2 < allowed_std:
            final_av, final_std, vtia = av2, std2, existing_values.lower()
        else:
            final_av, final_std, vtia = "", "", ""
    else:
        final_av, final_std, vtia = "", "", ""

    return [av3, std3, av2, std2, existing_values, vtia, final_av, final_std,[a,b,c]]

#print cal_tri (['22.966892', '20.785282', '22.531816'])

#for i in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
 #   print cal_tri([(22+i),22.5,21.5])








