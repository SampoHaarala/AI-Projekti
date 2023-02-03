import os
import input
import math

# My humble attempt at a general AI. Language based.
# Description of how it should work:
# My idea was to have a class of nodes and processes to represent data and relation between different data.
# This is not a neural network!
# The input file is used to get input and the classes file presents the functionality to process the input.
# Define a list of starting Item Nodes that will be construct the behaviour of the AI.
# New data is constructed using processes. Processes can be math functions like +/- or actions like reading a certain file.
# The overall behaviour should have the goal of finding out more information from the data learned.
# Depending on the start nodes, values can be set using polarities(positive or negative values).

# The "classes" file has the internal workings of the model. Input contains the methods of receiving input.

global allNodes
allNodes = {}
global unsureNodes
unsureNodes = {}
global processes
processes = {}
global recentProcesses
recentProcesses = []


class ItemNode:
    def __init__(self, parentNodes, parentProcesses, names=[], concept = {}, value=float(0)): # !!!Remember to define new variables to __getattribute__!!!!
        self.parentNodes = parentNodes # List of parents # Only one generation
        # Item nodes with number concept don't have parent nodes
        self.parentProcesses = parentProcesses # List of processes operators
        self.childNodes = [] # Item nodes with number concept don't have child nodes
        self.names = names
        self.concept = concept # Words have eight categories: noun, pronoun, verb, adverb preposition, conjunction, and interjection.
                               # Sentences have three parts: subject, verb, and complement.
                               # Therefore the parent nodes of sentences and words must have those concepts.
        self.value = value # Polarity is decided by a positive or negative value.
        # The complexity of an item node is determined by the value. The closer it's to zero, the simpler it is. Value should never be zero.

        self.addToAllNodes()

    def addToAllNodes(self):
        for concept in self.concept:
            if concept in allNodes:
                if self not in allNodes[concept]: allNodes[concept].append(concept)
            else: allNodes[concept] = [self]

    def getID(self):
        id = str(self.concept) + str(self.value)
        return id
    
    def defineConceptValues(node):
        parents = node.parentNodes
        conceptValues = {}
        for parent in parents:
            conceptValues[parent.concept] += parent.value
        return conceptValues

    def __getattribute__(self, __name: str):
        if __name == 'parentNodes':
            return self.parentNodes
        elif __name == 'parentProcesses':
            return self.parentProcesses
        elif __name == 'childNodes':
            if len(self.childNodes) == 0: return [self]
            else: return self.childNodes
            return self.childNodes
        elif __name == 'names':
            return self.names
        elif __name == 'concept':
            return self.concept
        elif __name == 'value':
            return self.value
        else:
            raise KeyError(__name)

    def createItemParentListFromParents(parents):
        pList = []
        for parent in parents:
            pList.extend(parent.parentNodes)
        return pList

    def addChild(self, child):
        self.children.append(child)

    def getPronouns(self):
        pronouns = []
        for parent in self.parentNodes:
            if 'location' in parent.concept or 'object' in parent.concept: pronouns.append('it')
            elif 'sex' in parent.concept:
                if parent.value < 0: pronouns.append('she')
                else: return pronouns.append('he')
            elif 'person' in parent.concept: pronouns.extend(['they', 'she', 'he'])
        
        return pronouns

    def getConceptListOfParents(self):
        concepts = []
        for parent in self.parentNodes:
            concepts.extend(parent.concept.keys())
        return concepts

    def getConceptDictionaryOfParents(self):
        concepts = {}
        for parent in self.parentNodes:
            for concept in parent.concept:
                concepts[concept] = parent
        return concepts

    def getWordCategoryConcept(self):
        categories = ['noun', 'pronoun', 'verb', 'adverb', 'adjective,' 'preposition', 'conjunction', 'interjection']
        for category in categories:
            if category in self.concept:
                return category
        return "None"
        
                
class Process:
    def __init__(self, startNodes, operator, parentProcesses = [], endNodes = []):
        self.startNodes = startNodes
        self.operator = operator
        self.parentProcesses = parentProcesses
        self.endNodes = endNodes

        if processes[operator]: processes[operator].append(self)
        else: processes[operator] = [self]

    def process(self):
        if self.operator == '+':
            startNodes = self.checkForDuplicateConcepts(self.startNodes)
            mergingPoint = self.findMergingPoint(startNodes)
            names = self.findNames(startNodes)

            self.endNodes.append(ItemNode(startNodes, self, names, mergingPoint, 1))
            
        elif self.operator == 'read':
            sentences = []
            sentence = []
            text = ""
            for node in self.startNodes:
                text += node.name[0]
                text += " "
                if 'punctuation' in node.concept:
                    sentences.append(self.readSentence(sentence))
                    sentence = []
                else:
                    sentence.append(node)
            if len(sentence) > 0:
                sentences.append(self.readSentence(sentence))
            
            concept = self.findMergingPoint(sentences)

            self.endNodes.append(ItemNode(self.startNodes, self, [text, "paragraph"], concept, 1))

        elif self.operator == '*':
            startNodes = self.checkForDuplicateConcepts(self.startNodes)
            startNode = startNodes[0]
            startNodes.pop(0)
            for node in startNodes:
                for concept in node.concept:
                    if concept in startNode.concept: startNode.concept[concept] *= node.concept[concept]
                    else: 
                        startNode.concept[concept] = node.concept[concept]
                        allNodes[concept].append(startNode)
                    if startNode.concept[concept] < 0.1: startNode.concept.pop(concept)
            self.endNodes.append(startNode)
                
        return self.endNodes

    def checkForDuplicateConcepts(self, startNodes):
        for node1 in startNodes:
                for node2 in startNodes:
                    if node1 == node2:
                        pass
                    elif node1.concept == node2.concept:
                        newNode = self.doConceptSum(node1, node2)
                        startNodes.pop(node1)
                        startNodes.pop(node2)
                        startNodes.append(newNode)
        return startNodes
    
    def readSentence(self, nodes):
        text = ""
        for node in nodes:
            text += node.names[0]
            text += " "

        parts = []
        unsureWordNodes = []
        currentNodes = nodes
        while len(nodes) != 0:
            part, currentNodes, unsureNodes = self.readPartFromSentence(currentNodes)
            parts.extend(part)
            unsureWordNodes.extend(unsureNodes)
        
        parts = self.processWordParts(parts)
        concept = Process(parts, '+', self).process()
        if len(unsureWordNodes) != 0:
            newStartNodes = nodes
            for node in unsureWordNodes:
                newStartNodes.pop(node)
                s = [node]
                s.extend(parts)
                Process(s, '*', self).process()
                self.read

        return ItemNode(parts, self, [text, 'sentence'], concept, 1)

    def processWordParts(self, parts): # Condense parts of a sentence into a subject, action, and object.
        newNodes = []
        for wordNodeDict in parts:
            if 'noun' in wordNodeDict:
                for node in wordNodeDict['noun']:
                    newNode = node
                    a = [node]
                    if 'adjective' in wordNodeDict:
                        a.extend(wordNodeDict['adjective'])
                        newNode = Process(a, '+', self).process()
                    if 'preposition' in wordNodeDict:
                        a.extend(wordNodeDict['preposition'])
                        newNode = Process(a, '+', self).process()

                    if len(a) > 1: newNode = Process(a[0], '+', self).process()
    
                    newNodes.append(newNode)
    
            if 'pronoun' in wordNodeDict:
                for node in wordNodeDict['pronoun']:
                    newNode = node
                    a = [node]
                    if 'adjective' in wordNodeDict:
                        a.extend(wordNodeDict['adjective'])
                        newNode = Process(a, '+', self).process()
                    if 'preposition' in wordNodeDict:
                        a.extend(wordNodeDict['preposition'])
                        newNode = Process(a, '+', self).process()
    
                    newNodes.append(newNode)
    
            if 'verb' in wordNodeDict:
                for node in wordNodeDict['verb']:
                    newNode = node
                    a = [node]
                    if 'adverb' in wordNodeDict:
                        a.append(wordNodeDict['adverb'])
                        newNode = Process(a, '+', self).process()
                
                    newNodes.append(newNode)

        return newNodes

    def processParagraphs(self): # Take in sentences and find essential actors and actions.
        actors = {}

        sentences = self.startNodes
        for sentence in sentences:
            sdict = sentence.getConceptDictionaryOfParents()
            currentActor = None
            if 'noun' in sdict:
                if sdict['noun'] not in actors: actors[sdict['noun']] = []
                currentActor = sdict['noun']
            if 'pronoun' in sdict:
                pronouns = sdict['pronoun'].getPronouns()
                for pronoun in pronouns:
                    for actor in actors.__reversed__():
                        if pronoun in actor.getPronouns(): 
                            currentActor = actor
            if 'verb' in sdict:
                if currentActor is not None:
                    actors[currentActor].append(sdict['verb'])

        commonActorConceptProcess = Process(actors.keys(), '+', [self])               
                        
    def readPartFromSentence(nodes): # Take in a collection of word nodes in the order of a sentence and construct sentence parts from them.
        keyCategories = ['noun', 'pronoun', 'verb']
        keyCount = 0
        foundWords = {}
        foundUnsureWords = []
        for node in nodes:
            categories = ['noun', 'pronoun', 'verb', 'adverb', 'adjective,' 'preposition', 'conjunction', 'interjection']
            if 'conjunction' in node.concept and keyCount == 1:
                keyCount -= 1
            if node.getWordCategory() in categories:
                for category in keyCategories:
                    if category in keyCategories:
                        keyCount += 1
                        if keyCount > 1:
                            break
                if node.getWordCategory() in foundWords:
                    foundWords[node.getWordCategory()].append(node)
                else:
                    foundWords[node.getWordCategory()] = [node]
            else:
                if len(node.concept) == 0:
                    if node in input.unsureWords:
                        foundUnsureWords.append(node)
                print("Word type not defined!: " + node.name)
            nodes.pop(node)
        return foundWords, nodes, foundUnsureWords
            
    def findCommonConcept(nodes = []):
        conceptAppearances = {}
        i = 0
        for node in nodes:
            for concept in node.concept.keys():
                if concept not in conceptAppearances:
                    conceptAppearances[concept] = [node]
                else:
                    conceptAppearances[concept].append(node)
        
        generationList = [nodes]
        childParent = {}
        foundConcept = ""
        conceptValues = {}
        i = 0

        while foundConcept == "":
            for node in generationList[i]:
                if foundConcept == "":
                    parents = node.parentNodes
                    for parent in parents:
                        childParent[parent] = node
                    if len(generationList) < i + 1:
                        generationList.append(parents)
                    else:
                        generationList[i + 1].extend(parents)
                
                    concepts = Process.makeConceptDictionary(parents)
                    for pconcept in concepts:
                        item = concepts[pconcept]
                        value = 0
                        while True:
                            value += item.value
                            if item in nodes:
                                if pconcept in conceptAppearances:
                                    if item not in conceptAppearances[pconcept]:
                                        conceptAppearances[pconcept].append(item)
                                        conceptValues[pconcept] += value

                                        if conceptAppearances[pconcept] == nodes:
                                            foundConcept = pconcept # Common concept found!
                                else:
                                    conceptAppearances[pconcept] = item
                                break
                            if item in childParent.keys():
                                item = childParent[item]
                            else: break
                else: break
                i += 1
        
        value = conceptValues[foundConcept]
        return foundConcept, value,         

    def makeConceptList(nodes = []):
        list = []
        for node in nodes:
            for concept in node.concept:
                if concept not in list:
                    list.append(concept)
        return list

    def makeConceptDictionary(nodes = []):
        dicto = {}
        for node in nodes:
            for concept in node.concept:
                if concept in dicto: pass #TODO: tää ei toimi enää
                else: dicto[node.concept] = node
        return dicto
    
    def doConceptSum(self, node1, node2):
        if node1.concept == node2.concept:
            value = node1.value + node2.value
            newItem = ItemNode([node1, node2], self, [node1.names[0], node2.names[0]], node1.concept, value)    
            return newItem
        else:
            print("doConceptSum: improper use!")
            raise(SyntaxError)
    
    def doDoubleConceptSum(self, node1, node2):
        if 'number' in node1.concept or 'number' in node2.concept:
            numberNode = None
            noneNumberNode = None
            if 'number' in node1.concept:
                numberNode = node1
                noneNumberNode = node2
            elif 'number' in node2.concept:
                numberNode = node2
                noneNumberNode = node1
            
            noneNumberNode.value = noneNumberNode.value + numberNode.value
            return noneNumberNode

        else:
            concept, value = self.findCommonConcept(node1, node2)
            
            endNode = ItemNode([node1, node2], ItemNode.createItemNameListFromParents((node1, node2)), concept, value)

            return endNode

    def findMergingPoint(self, nodes = []):
        conceptDict = {}
        for node in nodes:
            for concept in node.concept:
                if concept not in conceptDict: conceptDict[concept] = node[concept]
                else: 
                    conceptDict[concept] += node[concept]
                    if conceptDict[concept] == 0:
                        conceptDict.pop(concept)
        
        newConceptDict = {}
        for concept in conceptDict:
            newConceptDict[concept] = conceptDict[concept] / 2 # Tästä laskusta saatiiin piste, jolla oli sama etäisyys kaikkiin muihin pisteihin.
                                                               # Toimi ainakin kolmessa ja kahdessa ulottovuudessa.
        return newConceptDict

    def getFirstNames(nodes = []):
        names = []
        for node in nodes:
            names.append(node.names[0])
        return names