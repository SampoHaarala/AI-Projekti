import os
import input
import math
import numpy as np

# The plan is to create vectors with undefined dimensions. Those vectors symbolise items.
# The dimensions are the properties of the vector, such as "person" or "table".
# How much each dimension has weight on a vector is determined by it's lenght in that dimension.
# The lenght has to be compressed somehow. Certain limits must be placed on the possible lenght to
# limit unnecessary dimensions to attaching to the vectors. 

global dimensions 
dimensions = ["physical", "living", "visible"]

global knownWords
knownWords = {} # "word": [0.2,0,0.7,0.1,0,0] Each index in the list is representative
                # decided word type. Look at worddimensions for more.
global knownWordsReversed
knownWordsReversed = {} # [0.2,0,0.7,0.1,0,0]: "word"

global wordDimensions
wordDimensions = np.array() # Contains word types. 0: adjectives, 1: nouns, 2: pronouns, 
                            # 3: verbs, 4: adverbs, 5: conjunctions, 6: determiners, 7: prepositions

global emptyWordVector
emptyWordVector = np.array() # TODO: Fill later

global compareWithOtherSentences
compareWithOtherSentences = True

global knownSentences
knownSentences = np.array()

global knownSymbolVectors
knownSymbolVectors = {}
global symbolIndexes
symbolIndexes = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8,
                 "j": 9, "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16,
                 "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}

global blankSymbolVector
blankSymbolVector = np.array(size=len(knownSymbolVectors)).zeros()

### GLOBAL GETS AND SETS ###

def AddNewWord(word, vector):
    knownWords[word] = vector
    knownWordsReversed[vector] = word

### MATH FUNCTIONS ###

def Sigmoid(value):
    return 1 / (1 + np.power(np.e, value))

### TEXT VECTOR STUFF ###

def GetWordVector(word):
    if (knownWords.__contains__(word)): vector = knownWords[word]
    else: vector = None
    return vector

def GetSentenceVector(lenght):
    newVector = np.ones(size=lenght)
    newVector = newVector / np.linalg.norm(newVector)
    return newVector

def GetWordMatrix(words):
    containsUnknownWord = False
    unknownWordIndex = 0
    unknownWord = ""

    wordMatrix = np.array()
    i = 0
    for word in words:
        if GetWordVector(word) != None: wordMatrix.append(GetWordVector(word))
        else:
            if compareWithOtherSentences:
                wordMatrix.append(np.zeros_like(wordDimensions.size))
                containsUnknownWord = True
                unknownWordIndex = i
                unknownWord = word
        i += 1 

    if containsUnknownWord: 
        newVector = CompareWordVectorToSimilarSentences(wordMatrix, unknownWordIndex)
        if newVector == None: newVector = CompareSymbolVectorToSimilarWords(TurnWordIntoSymbolVector(unknownWord))
        AddNewWord(unknownWord, newVector)
        wordMatrix[unknownWordIndex] = newVector
    
    return wordMatrix

def GetMeaningVectorFromWordMatrix(wordMatrix):
    indexList, newVector = GetSentenceVector(np.ma.size(wordMatrix, 1))
    meaningVector = np.dot(wordMatrix, newVector)
    meaningVector = meaningVector / np.linalg.norm(meaningVector)
    return meaningVector

def TurnWordIntoSymbolVector(word):
    word = word.lower()
    vector = np.copy(blankSymbolVector)
    lenght = len(word)
    for i in range(lenght):
        vector[symbolIndexes[word[i]]] = lenght - i + 1
    vector = vector / np.linalg.norm(vector)
    return vector

def TryToDefineNewWord(word):
    vector = TurnWordIntoSymbolVector(word)
    mostSimilarWordVector = CompareSymbolVectorToSimilarWords(vector)
    return mostSimilarWordVector

def TurnTextIntoVector(text):
    sentenceMatrix = np.array()
    sentences = text.split('.|,|!|?')
    for sentence in sentences:
        if len(sentence) > 0:
            GetWordMatrix(sentence.split(" "))
            sentenceMatrix.append(GetMeaningVectorFromWordMatrix())
    textVector = np.ones(wordDimensions.size())
    textVector = np.dot(sentenceMatrix, textVector)
    return textVector

def GetProbableWordTypes(wordMatrix):
    wordTypes = []
    while len(wordTypes) > len(wordMatrix):
        wordTypes.append(GetMostProbableWordType(wordMatrix, wordTypes))
    return wordTypes

def GetMostProbableWordType(wordMatrix, wordTypes):
    index = np.argmax(wordMatrix, 1)
    if not wordTypes.__contains__(wordMatrix[index]): return wordMatrix[index]
    else:
        wordMatrix.pop(index)
        return GetMostProbableWordType(index, wordMatrix)


### COMPARISONS ###

def CompareWordVectorToSimilarSentences(wordMatrix, indexOfTheUnknownVector):
    similarVectors = np.array()
    for knownSentence in knownSentences:
        if knownSentence.size() == wordMatrix.size():
            similarVectors.append(knownSentence[indexOfTheUnknownVector])
    if similarVectors.size() == 0: return None
    else: return np.mean(similarVectors, 2)

def CompareSymbolVectorToSimilarWords(vector):
    similarVectorMatrix = np.array()
    for otherVector in knownSymbolVectors.keys():
        product = np.dot(vector, otherVector)
        if product > 0.7:
            similarVectorMatrix.append(knownSymbolVectors[otherVector])
    if similarVectorMatrix.size() != 0: return np.mean(similarVectorMatrix, 2)
    else: return np.zeros_like(emptyWordVector)

def CompareTextVectorToItsContent(textVector, sentenceMatrix):
    for i in range(len(sentenceMatrix)):
        product = np.dot(textVector, sentenceMatrix[i])
        if product > 0.7:
            pass

### ACTIONS ###

