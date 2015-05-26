import csv
from operator import itemgetter
def convertFile(fileName):
    # Index Const:
    DateIndex = 1
    OppTeamIndex = 2
    AtIndex = 3
    HomeTeamIndex = 4
    PA2Index = 11
    PA3Index = 14
    FTAIndex = 17
    PTSIndex = 19
    ORBIndex = 20
    DRBIndex = 21
    ASTIndex = 23
    STLIndex = 24
    BLKIndex = 25
    TOVIndex = 26
    HomeIndexOffset = 21
    # Game Weights:
    FirstWeight = 0.70
    FirstGameLine = 10
    SecondWeight = 0.30
    # Score Difference Levels:
    FirstScoreLine = 5
    SecondScoreLine = 15
    ScoreDifLvl0 = 1
    ScoreDifLvl1 = 2
    ScoreDifLvl2 = 3
    # Attribute Names Dictionary:
    AttrNamesDictionary = {PA2Index:'2PA',PA3Index:'3PA',FTAIndex:'FTA',PTSIndex:'PTS',ORBIndex:'ORB',DRBIndex:'DRB',ASTIndex:'AST',STLIndex:'STL',BLKIndex:'BLK',TOVIndex:'TOV'}
    # Get the Data from File:
    csvReader = csv.reader(open(fileName,"rb"),delimiter=',') 
    data = list(csvReader)
    firstRow = data.pop(0)
    gamesDictionary = {'TOR': [],'BOS': [],'BRK': [],'PHI': [],'NYK': [],'CLE': [],'CHI': [],'MIL': [],'IND': [],'DET': [],'ATL': [],'WAS': [],'MIA': [],'ORL': [],'POR': [],'OKC': [],'UTA': [],'DEN': [],'MIN': [],'GSW': [],'LAC': [],'PHO': [],'SAC': [],'LAL': [],'HOU': [],'SAS': [],'MEM': [],'DAL': [],'NOP': [],'NOH':[],'CHA': [],'CHO': []}  
    # Generate Games Hash Table with Team Name as Keys:
    for dataRow in data:
        (gamesDictionary[dataRow[OppTeamIndex]]).append(dataRow)
        (gamesDictionary[dataRow[HomeTeamIndex]]).append(dataRow)
    # Sort the Game List under Each Team Key:
    for teamKey in gamesDictionary:
        gamesDictionary[teamKey] = sorted(gamesDictionary[teamKey], key=itemgetter(DateIndex))
    # Generate Result Data List:
    firstResultLine = AttrNamesDictionary.values()
    firstResultLine.append('ScoreDifLvl')
    resultData = [firstResultLine]
    for dataRow in data:
        homeTeamKey = dataRow[HomeTeamIndex]
        oppTeamKey = dataRow[OppTeamIndex]
        date = dataRow[DateIndex]
        homeGameIndex = [index for index, game in enumerate(gamesDictionary[homeTeamKey]) if game[DateIndex] == date][0]
        oppGameIndex = [index for index, game in enumerate(gamesDictionary[oppTeamKey]) if game[DateIndex] == date][0]     
        if homeGameIndex < FirstGameLine or oppGameIndex < FirstGameLine:
            continue
        else:
            # Generate Attributes Line:
            resultLineDictionary = {PA2Index:0,PA3Index:0,FTAIndex:0,PTSIndex:0,ORBIndex:0,DRBIndex:0,ASTIndex:0,STLIndex:0,BLKIndex:0,TOVIndex:0}
            for i in range(homeGameIndex):
                currentWeight = SecondWeight if (homeGameIndex-i)>FirstGameLine else FirstWeight
                for attrKey in resultLineDictionary:
                    resultLineDictionary[attrKey] += int(gamesDictionary[homeTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[homeTeamKey][i][HomeTeamIndex] == homeTeamKey else 0)]) * currentWeight / homeGameIndex
            for i in range(oppGameIndex):
                currentWeight = SecondWeight if (oppGameIndex-i)>FirstGameLine else FirstWeight
                for attrKey in resultLineDictionary:
                    resultLineDictionary[attrKey] -= int(gamesDictionary[oppTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[oppTeamKey][i][HomeTeamIndex] == oppTeamKey else 0)]) * currentWeight / oppGameIndex
            # Generate Classified Result:
            scoreDif = int(dataRow[PTSIndex+HomeIndexOffset])-int(dataRow[PTSIndex])
            if scoreDif > SecondScoreLine:
                scoreDifLvl = 'ScoreDifLvl2'
            elif scoreDif < -SecondScoreLine:
                scoreDifLvl = '-ScoreDifLvl2'
            elif scoreDif > FirstScoreLine:
                scoreDifLvl = 'ScoreDifLvl1'
            elif scoreDif < -FirstScoreLine:
                scoreDifLvl = '-ScoreDifLvl1'
            elif scoreDif > 0:
                scoreDifLvl = 'ScoreDifLvl0'
            else:
                scoreDifLvl = '-ScoreDifLvl0'
            # Combine Two Things Together into Line List
            resultLineList = resultLineDictionary.values()
            resultLineList.append(scoreDifLvl)
            # Push the Line List into Result Data List
            resultData.append(resultLineList)
    with open(fileName[:len(fileName)-4]+"-result.csv", "wb") as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(resultData)
    return resultData, gamesDictionary

