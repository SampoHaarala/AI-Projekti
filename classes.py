import os
import logic
import math

# My humble attempt at a general AI. Language based.
# Description of how it should work:
# Define a list of starting Item Nodes that will be construct the behaviour of the AI.
# Data is constructed using processes. Processes can be math functions like +/- or reading a certain file.
# The overall behaviour should have the goal of expanding. By this I mean finding out more information.
# Depending on the start nodes, values can be set using polarities(positive or negative values).

global nodes
nodes = []
global processes
processes = []


class ItemNode:
    def __init__(self, parentNodes, parentProcesses, names=[], concept="None", value=0): # !!!Remember to define new variables to __getattribute__!!!!
        self.parentNodes = parentNodes # List of parents # Only one generation
        # Item nodes with number concept don't have parent nodes
        self.parentProcesses = parentProcesses # List of processes operators
        self.childNodes = [] # Item nodes with number concept don't have child nodes
        self.names = names
        self.concept = concept # Words have eight categories: noun, pronoun, verb, adverb preposition, conjunction, and interjection.
                               # Sentences have three parts: subject, verb, and complement.
                               # Therefore the parent nodes of sentences and words must have those concepts.
        self.value = value # Polarity is decided by a positive or negative value.
        # The complexity of an item node is determined by the value. The closer it's to zero, the simpler it is.

        nodes.append(self)

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


class Process:
    def __init__(self, startNodes, operator, parentProcesses = [], endNodes = []):
        self.startNodes = startNodes
        self.operator = operator
        self.parentProcesses = parentProcesses
        self.endNodes = endNodes

        processes.append(self)
    
    def getId(self):
        id = ''
        for node in self.startNodes:
            id += node.concept[0]
        id += self.operator
        return id

    def process(self):
        if self.operator == '+':
            node0 = self.startNodes[0]
            for node in self.startNodes:
                if node == node0:
                    pass
                elif node0.concept == node.concept:
                    node0 = self.doConceptSum(node0.value, node0, node)
                else:
                    concept, value = self.findCommonConcept([node0, node])

            self.endNodes.append(node0)
            
        elif self.operator == 'read':
            nodes = self.startNodes

            text = ""
            value = 0
            for node in nodes:
                text += node.name[0]
                value += node.value

            parts = []
            while len(nodes) != 0:
                part, nodes = self.readSentenceToParts(nodes)
                parts.extend(part)
            self.endNodes.append(ItemNode(self.processWordParts(parts), self, ['sentence', text], 'sentence', value))
            
            # TODO: Jatka tätä
                
        return self.endNodes

    def processWordParts(self, parts):
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

    def readPartFromSentence(nodes):
        keyCategories = ['noun', 'pronoun', 'verb']
        keyCount = 0
        foundWords = {}
        for node in nodes:
            categories = ['noun', 'pronoun', 'verb', 'adverb', 'adjective,' 'preposition', 'conjunction', 'interjection']
            if node.concept == 'conjunction' and keyCount == 1:
                keyCount -= 1
            if node.concept in categories:
                if node.concept in keyCategories:
                    keyCount += 1
                    if keyCount > 1:
                        break
                if node.concept in foundWords:
                    foundWords[node.concept].append(node)
                else:
                    foundWords[node.concept] = [node]
                nodes.pop(node)
            else:
                print("Word type not defined!: " + node.name)
        return foundWords, nodes
            
    def findCommonConcept(nodes = []):
        conceptAppearances = {}
        i = 0
        for node in nodes:
            if node.concept not in conceptAppearances:
                conceptAppearances[node.concept] = [node]
            else:
                conceptAppearances[node.concept].append(node)
        
        generationList = [nodes]
        childParent = {}
        concept = ""
        conceptValues = {}
        i = 0

        while concept == "":
            for node in generationList[i]:
                if concept == "":
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
                                            concept = pconcept
                                else:
                                    conceptAppearances[pconcept] = item
                                break
                            if item in childParent.keys():
                                item = childParent[item]
                            else:
                                break
        
        value = conceptValues[concept]
        return concept, value        

    def makeConceptList(nodes = []):
        list = []
        for node in nodes:
            if node.concept not in list:
                list.append(node.concept)
        return list

    def makeConceptDictionary(nodes = []):
        dicto = []
        for node in nodes:
            dicto[node.concept] = node
        return dicto
    
    def doConceptSum(self, concept, node1, node2):
        if concept == 'number':
            value = node1.value + node2.value
            parents = [(node1, node2)]
            parents.extend(node1.parentNodes)
            parents.extend(node2.parentNodes)

            newItem = ItemNode(parents, self, value, "number", value)    
            return newItem
    
    def doDoubleConceptSum(self, node1, node2):
        if node1.concept == 'number' or node2.concept == 'number':
            numberNode = None
            noneNumberNode = None
            if node1.concept == 'number':
                numberNode = node1
                noneNumberNode = node2
            elif node2.concept == 'number':
                numberNode = node2
                noneNumberNode = node1
            
            noneNumberNode.value = noneNumberNode.value + numberNode.value
            return noneNumberNode

        else:
            concept, value = self.findCommonConcept(node1, node2)
            
            endNode = ItemNode([node1, node2], ItemNode.createItemNameListFromParents((node1, node2)), concept, value)

            return endNode
