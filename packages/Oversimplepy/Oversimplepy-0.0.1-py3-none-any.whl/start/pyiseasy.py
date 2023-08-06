def calculator(num1,num2,operator):
    if operator=='+':
        return num1+num2
    elif operator=='-':
        if num1>num2:
            return num1-num2
        else:
            return num2-num1
    elif operator=='*':
        return num1*num2
    elif operator=='/':
        if num1>num2:
            return num1/num2
        else:
            return num2/num1
    elif operator.lower()=='exp':
        return num1**num2
    elif operator.lower()=='sqroot':
        return num1**(1/num2)

def openfile(filename,mode):
    if mode.lower()=='read':
        return open(filename,'r')
    elif mode.lower()=='write':
        return open(filename,'w')
    elif mode.lower()=='append':
        return open(filename,'a')

def readfile(filehandle):
    return filehandle.read()

def writetofile(filehandle,value):
    return filehandle.write(value)

def closefile(filehandle):
    return filehandle.close()

def declaredatatpye(value,vtype):
    if vtype.lower()=='integer':
        return int(value)
    elif vtype.lower()=='string':
        return str(value)
    elif vtype.lower()=='decimal':
        return float(value)
    elif vtype.lower()=='list':
        return list(value)
    elif vtype.lower()=='tuple':
        return tuple(value)
    elif vtype.lower()=='dictionary':
        return dict(value)
    elif vtype.lower()=='factorial':
        n=1
        for i in range(1,value+1):
            n=n*i
        return n
    elif vtype.lower()=='is true' and value.lower()=='bool':
        value=True
        return value
    elif vtype.lower()=='is false' or vtype.lower()=='is not true' and value.lower()=='bool':
        value=False
        return value

def printbackwards(string):
    return string[-1:]

def removeduplicate(listvalue):
    afdup=list()
    for i in listvalue:
        if i not in afdup:
            afdup.append(i)
    return afdup

def giveduplicates(listvalue):
    d=list()
    for i in listvalue:
        if listvalue.count(i)==2:
            d.append(i)
    return d

def addDict(d,key,value):
    d[key]=value
    return d[key]

def addtuple(t,value):
    t=t+(value,)
    return t

def findASCII(char):
    return chr(char)

def findvalchar(val):
    return ord(val)

def probability(noutcomes,toutcomes):
    return noutcomes/toutcomes

def findvowels(text):
    count=0
    for i in text:
        if i.lower() in ['a','e','i','o','u']:
            count+=1
    return count

def paragraph(parahere):
    a=str(parahere)
    return a.title()
