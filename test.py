import csv
execfile("convert.py")
result = []
firstLine = []
for i in range(11,15):
    print "training file "+str(i)+'-'+str(i+1)+'.csv'
    result1, result2 = convertFile(str(i)+'-'+str(i+1)+'.csv')
    result += result1[1:]
    firstLine = result1[0]
result.insert(0,firstLine)
with open("result.csv", "wb") as outputFile:
    writer = csv.writer(outputFile)
    writer.writerows(result)
#return a