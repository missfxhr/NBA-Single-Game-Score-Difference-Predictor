import csv
from operator import itemgetter
def convertFile(fileName):
    # Index Const:
    DateIndex = 1
    OppTeamIndex = 2
    HomeTeamIndex = 4
    GameInfoIndexLength = 7
    # Game Weights:
    FirstWeight = 0.70
    FirstGameLine = 10
    SecondWeight = 0.30
    # Score Difference Levels:
    FirstScoreLine = 5
    SecondScoreLine = 15
    # Attribute Names Dictionary:
    AllAttrNamesDictionary = {}
    AttrNamesDictionary = {}
    # Get the Data from File:
    csvReader = csv.reader(open(fileName,"rb"),delimiter=',') 
    data = list(csvReader)
    firstRow = data.pop(0)
    # Initialize Some Const Value and Dictionaries
    HomeIndexOffset = (len(firstRow)-GameInfoIndexLength)/2
    for i in range(GameInfoIndexLength,GameInfoIndexLength+HomeIndexOffset):
        AllAttrNamesDictionary[firstRow[i]] = i
    AttrNamesDictionary[AllAttrNamesDictionary['2PA']] = '2PA'
    AttrNamesDictionary[AllAttrNamesDictionary['3PA']] = '3PA'
    AttrNamesDictionary[AllAttrNamesDictionary['FTA']] = 'FTA'
    AttrNamesDictionary[AllAttrNamesDictionary['PTS']] = 'PTS'
    AttrNamesDictionary[AllAttrNamesDictionary['ORB']] = 'ORB'
    AttrNamesDictionary[AllAttrNamesDictionary['DRB']] = 'DRB'
    AttrNamesDictionary[AllAttrNamesDictionary['AST']] = 'AST'
    AttrNamesDictionary[AllAttrNamesDictionary['STL']] = 'STL'
    AttrNamesDictionary[AllAttrNamesDictionary['BLK']] = 'BLK'
    AttrNamesDictionary[AllAttrNamesDictionary['TOV']] = 'TOV'
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
            resultLineDictionary = {}
            for attrKey in AttrNamesDictionary:
                resultLineDictionary[attrKey] = 0
            for i in range(homeGameIndex):
                currentWeight = SecondWeight if (homeGameIndex-i)>FirstGameLine else FirstWeight
                for attrKey in resultLineDictionary:
                    resultLineDictionary[attrKey] += int(gamesDictionary[homeTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[homeTeamKey][i][HomeTeamIndex] == homeTeamKey else 0)]) * currentWeight / homeGameIndex
            for i in range(oppGameIndex):
                currentWeight = SecondWeight if (oppGameIndex-i)>FirstGameLine else FirstWeight
                for attrKey in resultLineDictionary:
                    resultLineDictionary[attrKey] -= int(gamesDictionary[oppTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[oppTeamKey][i][HomeTeamIndex] == oppTeamKey else 0)]) * currentWeight / oppGameIndex
            # Generate Classified Result:
            scoreDif = int(dataRow[AllAttrNamesDictionary['PTS']+HomeIndexOffset])-int(dataRow[AllAttrNamesDictionary['PTS']])
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

