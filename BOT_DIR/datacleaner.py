def cleansql(data): #this script is here to clean data from additionnal character, to make it usable as a list
    newdata = []
    for sample in data:
        tempdata = str(sample)
        tempdata = tempdata.replace('(','')
        tempdata = tempdata.replace(')','')
        tempdata = tempdata.replace(',','')
        tempdata = tempdata.replace('\'','')
        newdata.append(tempdata)

    return newdata


def cleanstring(data): #this function is here to clean string from additionnal characters and make it usable for a condition 
    tempdata = str(data)
    tempdata = tempdata.replace('(','')
    tempdata = tempdata.replace(')','')
    tempdata = tempdata.replace(',','')
    tempdata = tempdata.replace('\'','')
    return tempdata

def cleanroulette(data): #this script is here to clean data from additionnal character, to make it usable as a list
    newdata = []
    for sample in data:
        tempdata = str(sample)
        tempdata = tempdata.replace('(','')
        tempdata = tempdata.replace(')','')
        tempdata = tempdata.replace(',','')
        tempdata = tempdata.replace('\'','')

        
        newdata.append(tempdata)
