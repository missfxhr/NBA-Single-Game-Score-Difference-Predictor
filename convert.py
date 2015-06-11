import csv
import math
from operator import itemgetter
def convertFile(fileName):
    # Index Const:
    DateIndex = 1
    OppTeamIndex = 2
    HomeTeamIndex = 4
    GameInfoIndexLength = 7
    # Game Weights:
    MinGameNum = 10
    GameWeightOffset = 2
    # Score Difference Levels:
    # ScoreLine = [-10,-3,4,9,15]
    ScoreLine = [4]
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
    AttrNamesDictionary[AllAttrNamesDictionary['FG']] = 'FG'
    # AttrNamesDictionary[AllAttrNamesDictionary['FGA']] = 'FGA'
    # AttrNamesDictionary[AllAttrNamesDictionary['FG%']] = 'FGp'
    AttrNamesDictionary[AllAttrNamesDictionary['2P']] = '2P'
    AttrNamesDictionary[AllAttrNamesDictionary['2PA']] = '2PA'
    # AttrNamesDictionary[AllAttrNamesDictionary['2P%']] = '2Pp'
    # AttrNamesDictionary[AllAttrNamesDictionary['3P']] = '3P'
    AttrNamesDictionary[AllAttrNamesDictionary['3PA']] = '3PA'
    # AttrNamesDictionary[AllAttrNamesDictionary['3P%']] = '3Pp'
    AttrNamesDictionary[AllAttrNamesDictionary['FT']] = 'FT'
    AttrNamesDictionary[AllAttrNamesDictionary['FTA']] = 'FTA'
    # AttrNamesDictionary[AllAttrNamesDictionary['FT%']] = 'FTp'
    AttrNamesDictionary[AllAttrNamesDictionary['PTS']] = 'PTS'
    AttrNamesDictionary[AllAttrNamesDictionary['ORtg']] = 'ORtg'
    # AttrNamesDictionary[AllAttrNamesDictionary['FTr']] = 'FTr'
    # AttrNamesDictionary[AllAttrNamesDictionary['3PAr']] = '3PAr'
    # AttrNamesDictionary[AllAttrNamesDictionary['TS%']] = 'TSp'
    AttrNamesDictionary[AllAttrNamesDictionary['eFG%']] = 'eFGp'
    # AttrNamesDictionary[AllAttrNamesDictionary['FT/FGA']] = 'FT/FGA'
    # AttrNamesDictionary[AllAttrNamesDictionary['ORB']] = 'ORB'
    AttrNamesDictionary[AllAttrNamesDictionary['DRB']] = 'DRB'
    # AttrNamesDictionary[AllAttrNamesDictionary['TRB']] = 'TRB'
    AttrNamesDictionary[AllAttrNamesDictionary['AST']] = 'AST'
    AttrNamesDictionary[AllAttrNamesDictionary['STL']] = 'STL'
    AttrNamesDictionary[AllAttrNamesDictionary['BLK']] = 'BLK'
    # AttrNamesDictionary[AllAttrNamesDictionary['TOV']] = 'TOV'
    #AttrNamesDictionary[AllAttrNamesDictionary['PF']] = 'PF'
    gamesDictionary = {'TOR': [],'BOS': [],'PHI': [],'NYK': [],'CLE': [],'CHI': [],'MIL': [],'IND': [],'DET': [],'ATL': [],'WAS': [],'MIA': [],'ORL': [],'POR': [],'OKC': [],'UTA': [],'DEN': [],'MIN': [],'GSW': [],'LAC': [],'PHO': [],'SAC': [],'LAL': [],'HOU': [],'SAS': [],'MEM': [],'DAL': [],'NOP': [],'NOH':[],'CHA': [],'CHO': [],'BRK': [],'NJN':[]}  
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
        if homeGameIndex < MinGameNum or oppGameIndex < MinGameNum:
            continue
        else:
            # Generate Attributes Line:
            resultLineDictionary = {}
            for attrKey in AttrNamesDictionary:
                totalHomeWeight = 0
                homeTeamValue = 0
                totalOppWeight = 0
                oppTeamValue = 0
                percentFix = 100 if AttrNamesDictionary[attrKey][-1] == 'r' or AttrNamesDictionary[attrKey][-1] == 'p' else 1
                for i in range(homeGameIndex):
                    currentWeight = 1/(math.log(1.0+i+GameWeightOffset))
                    totalHomeWeight += currentWeight
                    homeTeamValue += float(gamesDictionary[homeTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[homeTeamKey][i][HomeTeamIndex] == homeTeamKey else 0)]) * currentWeight
                for i in range(oppGameIndex):
                    currentWeight = 1/(math.log(1.0+i+GameWeightOffset))
                    totalOppWeight += currentWeight
                    oppTeamValue += float(gamesDictionary[oppTeamKey][i][attrKey + (HomeIndexOffset if gamesDictionary[oppTeamKey][i][HomeTeamIndex] == oppTeamKey else 0)]) * currentWeight
                resultLineDictionary[attrKey] = percentFix*(homeTeamValue/(totalHomeWeight*homeGameIndex) - oppTeamValue/(totalOppWeight*oppGameIndex))
            # Generate Classified Result:
            scoreDif = int(dataRow[AllAttrNamesDictionary['PTS']+HomeIndexOffset])-int(dataRow[AllAttrNamesDictionary['PTS']])
            for i in reversed(range((len(ScoreLine)+1)/2)):
                if scoreDif >= ScoreLine[(len(ScoreLine)-1)/2+i]:
                    scoreDifLvl = 'ScoreDifLvl' + str(i)
                    break
                elif scoreDif < ScoreLine[(len(ScoreLine)-1)/2-i]:
                    scoreDifLvl = '-ScoreDifLvl' + str(i)
                    break
            # Combine Two Things Together into Line List
            resultLineList = resultLineDictionary.values()
            resultLineList.append(scoreDifLvl)
            # Push the Line List into Result Data List
            resultData.append(resultLineList)
    with open(fileName[:len(fileName)-4]+"-result.csv", "wb") as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(resultData)
    return resultData, gamesDictionary

