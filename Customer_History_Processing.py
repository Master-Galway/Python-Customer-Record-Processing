##Author: Wei(Galway) Gao

import pandas as pd
import datetime
from datetime import datetime

diction = {}
output = {'DATE': {}, 'ID': {}, 'RECORD': {}}
stop = False;
outputRow = 0;

while stop == False:
    day = ''
    id = ''
    act = ''
    userResponse = input('Enter a single customer record (Press S), or enter a file (Press F)\nEnter "CSV" to export your curretn result\nEnter "stop" to exit the program anytime\n')

    if userResponse == 'S' or userResponse == 's':  ### single entry ###
        try:
            raise SystemExit('Program Terminated')  # Print the termination message for invalid inputs
        except:
            day, id, act = map(str, input("Enter formatted Data, ID, Action. No space between commas:\n").split(','))
            if (id in diction):
                if diction[id].get(1) == 'fraud':  # identified as fraud customer
                    temp = diction[id].get(2)  # get prevous fraut count
                    diction[id] = {1: 'fraud', 2: (temp + 1)}  # increment fraud count
                    output['DATE'][outputRow] = day  # output corresponding attributes to another nested dictionary
                    output['ID'][outputRow] = id
                    fraudString = 'FRAUD_HISTORY: ' + str(diction[id].get(2))
                    output['RECORD'][outputRow] = fraudString
                    outputRow += 1;  # move to the next line of the dataframe
                else:  # not fraud yet, evaluate customer history
                    if act == 'FRAUD_REPORT':  # fraud for the first time
                        output['DATE'][outputRow] = day
                        output['ID'][outputRow] = id
                        fraudString = 'FRAUD_HISTORY: ' + str(1)
                        output['RECORD'][outputRow] = fraudString
                        outputRow += 1;
                    else:
                        iterator = 1  # first index of a customer's purchase hisotry
                        while (diction[id].get(iterator) != None):  # find the next open spot in the nest to add a new date/purchase history
                            iterator += 1;  # increment
                        diction[id][iterator] = day  # add a new date/purchase record of the customer
                        output['DATE'][outputRow] = day
                        output['ID'][outputRow] = id
                        dateObject1 = datetime.strptime(diction[id].get(1),'%Y-%m-%d')  # create a date object from the earliest pruchase history
                        dateObject2 = datetime.strptime(diction[id].get(iterator), '%Y-%m-%d')
                        dateDifference = (dateObject2.year - dateObject1.year) * 365 + (dateObject2.month - dateObject1.month) * 30 + (dateObject2.day - dateObject1.day)
                        # assuming every month is 30 days. calculate the biggest date difference of the customer
                        if dateDifference > 90:
                            output['RECORD'][outputRow] = 'GOOD_HISTORY'
                        else:
                            output['RECORD'][outputRow] = 'UNCOMFIRMED_HISTORY'
                            outputRow += 1
                        iterator = 1  # reset iteraotr to 1 for a different customer next time

            else:  # costomer record doesn't exist yet
                if act == 'FRAUD_REPORT':  # new fraud customer
                    diction[id] = {1: 'fraud', 2: 1}
                    output['DATE'][outputRow] = day
                    output['ID'][outputRow] = id
                    fraudString = 'FRAUD_HISTORY: ' + str(1)
                    output['RECORD'][outputRow] = fraudString
                    outputRow += 1;

                else:  # new non-fraud customer
                    diction[id] = {1: day}  # add customer purchase history with date
                    output['DATE'][outputRow] = str(day)
                    output['ID'][outputRow] = str(id)
                    output['RECORD'][outputRow] = 'NO_HISTORY'
                    outputRow += 1;


    elif userResponse == 'F' or userResponse == 'f':  ### file entry ###
        fileName = input('Put your input file in the folder, and enter your file name(.csv):')
        if fileName == 'STOP' or fileName == 'stop':
            print('Program Terminated')
            break;
        df = pd.read_csv(fileName, names=['date', 'ID', 'action'])

        for i in range(len(df)):

            if (df.ID[i] in diction):  # customer record already exists
                if diction[df.ID[i]].get(1) == 'fraud':  # identified as fraud customer
                    temp = diction[df.ID[i]].get(2)  # get prevous fraut count
                    diction[df.ID[i]] = {1: 'fraud', 2: (temp + 1)}  # increment fraud count
                    output['DATE'][outputRow] = df.date[
                        i]  # output corresponding attributes to another nested dictionary
                    output['ID'][outputRow] = df.ID[i]
                    fraudString = 'FRAUD_HISTORY: ' + str(diction[df.ID[i]].get(2))
                    output['RECORD'][outputRow] = fraudString
                    outputRow += 1;  # move to the next line of the dataframe

                else:  # not fraud, evaluate customer history
                    if df.action[i] == 'FRAUD_REPORT':  # fraud for the first time
                        output['DATE'][outputRow] = df.date[i]
                        output['ID'][outputRow] = df.ID[i]
                        fraudString = 'FRAUD_HISTORY: ' + str(1)
                        output['RECORD'][outputRow] = fraudString
                        outputRow += 1;
                    else:
                        iterator = 1  # first index of a customer's purchase hisotry
                        while (diction[df.ID[i]].get(iterator) != None):  # find the next open spot in the nest to add a new date/purchase history
                            iterator += 1;  # increment
                        diction[df.ID[i]][iterator] = df.date[i]  # add a new date/purchase record of the customer
                        output['DATE'][outputRow] = df.date[i]
                        output['ID'][outputRow] = df.ID[i]
                        dateObject1 = datetime.strptime(diction[df.ID[i]].get(1),
                                                        '%Y-%m-%d')  # create a date object from the earliest pruchase history
                        dateObject2 = datetime.strptime(diction[df.ID[i]].get(iterator), '%Y-%m-%d')
                        dateDifference = (dateObject2.year - dateObject1.year) * 365 + (
                                    dateObject2.month - dateObject1.month) * 30 + (dateObject2.day - dateObject1.day)
                        if dateDifference > 90:
                            output['RECORD'][outputRow] = 'GOOD_HISTORY'
                        else:
                            output['RECORD'][outputRow] = 'UNCOMFIRMED_HISTORY'
                        outputRow += 1
                        iterator = 1  # reset iterator to 1 for a different customer next time

            else:  # costomer record doesn't exist yet
                if df.action[i] == 'FRAUD_REPORT':  # fraud customer
                    diction[df.ID[i]] = {1: 'fraud', 2: 1}
                    output['DATE'][outputRow] = df.date[i]
                    output['ID'][outputRow] = df.ID[i]
                    fraudString = 'FRAUD_HISTORY: ' + str(1)
                    output['RECORD'][outputRow] = fraudString
                    outputRow += 1;

                else:
                    diction[df.ID[i]] = {1: df.date[i]}  # add customer purchase history with date
                    output['DATE'][outputRow] = df.date[i]
                    output['ID'][outputRow] = df.ID[i]
                    output['RECORD'][outputRow] = 'NO_HISTORY'
                    outputRow += 1;
        print('CSV file read complete')

    elif userResponse == 'STOP' or userResponse == 'stop':  ### user wants to stop ###
        print('Program Terminated')
        break;

    elif userResponse == 'CSV' or userResponse == 'csv':  # export current evaluation into an csv file
        csv = input('Type your file path:\n')
        if csv == 'STOP' or csv == 'stop':
            print('Program Terminated')
            break;
        dfOut = pd.DataFrame.from_dict(output)
        dfOut.to_csv(csv, index=True, header=False)


    else:  ### handles invalid entry ###
        print('Invalid entry, please try again')

dfOut = pd.DataFrame.from_dict(output)
print(dfOut)