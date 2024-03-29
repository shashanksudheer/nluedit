#!/usr/bin/env python3

# Useful Data Massaging Functions
# Author: Shashank Sudheer

from ast import arg
import sys
import fileinput
import random
import os
import pandas as pd

# Code to replace every occurance of {variable} in a given file
# with a random choice from a given input list
#
# Input: 
#   varToRep ->  the word from file to replace 
#   filename ->  the path to the file that should be modified
# Output: 
#   a string saying finished
def randomReplace(varToRep, filename):
    print("What should I replace " + varToRep + " with?")
    textToSearch = str(input( "> " ))
    lstSearch = textToSearch.split(" ")

    print('Starting replacement...')
    for line in fileinput.input(filename, inplace=True):
        rng = random.randint(0, len(lstSearch) - 1)
        print(line.replace(varToRep, lstSearch[rng]), end='')
    
    return 'Finished replacing'

# Splits on whatever character is provided as input
# Input: 
#   inp -> character to replace one
# Output:
#   string saying finished
def converseSplit(inp):
    print('What character should I split on?')
    char = str(input("> "))
    print('---------------------------')
    newStr = inp.split(char)
    newStr = '\n'.join(newStr)
    print(newStr)

    return 'Finished massaging'

# Splits on whatever character is provided as input and extracts only one line
# Input: 
#   fn -> filename to split on
# Output:
#   string saying finished
def splitOut(filename):
    char = "||"
    print('what line # do you want?')
    lineNum = int(input("> "))
    lineNum -= 1
    print('if idk what line # do you want?')
    idkLineNum = int(input("> "))
    idkLineNum -= 1
    with open(filename, "r") as fn:
        with open("outfile.tsv", "w+") as outfile:       
            for line in fn:   
                convoLst = line.split(char)
                if (lineNum < len(convoLst)):
                    # if the user utterance is 'idk'
                    if (convoLst[lineNum][-3:]) == "idk":
                        if (convoLst[lineNum][-1] == "\n"):
                            outfile.write(convoLst[idkLineNum][42:] + '\n')
                            break
                    outfile.write(convoLst[lineNum][42:] + '\n')

    return 'Finished splitting'


# scripts that appends all files together into one output file 
# Input:
#   initDirPath -> the path to the directory with all the files that need
#                  to be combined
# Output:
#   A file called 'output.tsv' within the directory that was provided
def combineAll(initDirPath): 
    fileLst = []

    for (dirpath, dirnames, filenames) in walk(initDirPath):
        fileLst.extend(filenames)
        break
    
    outFilePath = initDirPath + "/output.tsv"
    with open(outFilePath, mode='w') as outfile:
        for file in fileLst:
            newFilePath = initDirPath + "/" + file
            with open(newFilePath) as infile:
                for line in infile:
                    outfile.write(line)            

    return 'Finished'



def addIDs(fnToGet, fnToPut):
    dict = {}
    with open(fnToGet, mode='r', encoding='utf-8-sig') as inFile:
        for line in inFile:
            splitLine = line.split('\t')
            replacedLine = splitLine[1].rstrip('\n')
            dict[replacedLine] = splitLine[0]
    with open(fnToPut, mode='r', encoding='utf-8-sig') as inFile2:
        with open("outfile.csv", "w+") as outFile:
            for line in inFile2:
                utteranceLst = line.split("\t")
                print(utteranceLst[0])
                utteranceLst[1] = utteranceLst[1].rstrip('\n')
                id = dict[utteranceLst[0]]
                utteranceLst.append(id)
                #print(utteranceLst[1])
                newLineStr = ','.join(utteranceLst)
                newLineStr += '\n'
                outFile.write(newLineStr)
            
        

    return 'Finished'


def choose(fnToGet, n):
    # ensure n is int
    n = int(n)

    # items will be stored in a map/dictionary 
    #       key --> intent name
    #       val --> list containing the first n utterances found for each intent
    utterDict = {}

    with open(fnToGet, mode='r', encoding='utf-8-sig') as file:
        for line in file:
            lineLst = line.split('\t')
            if lineLst[0] not in utterDict:
                utterDict[lineLst[0]] = [lineLst[1]]
            else:
                if len(utterDict[lineLst[0]]) < n:
                    utterDict[lineLst[0]].append(lineLst[1])
        
    with open("outfile.tsv", mode="w+", encoding="utf-8-sig") as outfile:
        for k, v in utterDict.items():
            for i in v:
                outfile.write(k + "\t" + i + "\n")


    return 'Finished choosing -- printed to outfile.tsv'


# function that prints out all filenames in a directory 
# input:
#   dirpath -> directory to pass in
# output:
#   comma-separated string of filenames
def printAllFileNamesInDir(dirPath):
    dirLst = os.listdir(dirPath)
    dirStr = ','.join(dirLst)
    return dirStr


def matchConvoIDsWithUtterance(fnToGet):



def main():
    
    args = sys.argv

    default = 'All Done :)'

    if args[1] == 'replace':
        default = randomReplace(args[2], args[3]) 
    elif args[1] == 'converse':
        default = converseSplit(args[2])
    elif args[1] == 'combine':
        default = combineAll(args[2])
    elif args[1] == 'addid':
        default = addIDs(args[2], args[3])
    elif args[1] == 'splitout':
        default = splitOut("massageInput.txt")
    elif args[1] == 'choose':
        default = choose(args[2], args[3])
    #elif args[1] == 'mapint':
    #    default = mapIntents(args[2])
    elif args[1] == '-h':
        print(
            'replace <variable to replace> <filename>\nconverse <character to split on>\ncombine <diectory path>\nsplitout <filename>'
        )
    elif args[1] == 'fnindir':
        default = printAllFileNamesInDir(args[2])
    
    return default

splitOut("C:\Users\shank\Projects\nluedit\massageInput.txt")