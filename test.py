import csv
execfile("convert.py")
result = []
for i in range(11,15):
    result1, result2 = convertFile(str(i)+'-'+str(i+1)+'.csv')
    result += result1
with open("result.csv", "wb") as outputFile:
    writer = csv.writer(outputFile)
    writer.writerows(result)
#return a