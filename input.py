from classes import ItemNode, Process, allNodes, recentProcesses, unsureNodes
global assisted # Boolean that controls flow. If true, model will ask for input when lacking info.
assisted = True

def Read(text, language=None):
    newWords = []
    words = text.split()
    if language is None:
        # Figure out the language.
        pass
    else:
        knownWords = allNodes['words']
        specialSymbols = ['.', '?', '!']
        wordNodes = []
        for word in words:
            for specialSymbol in specialSymbols:
                if specialSymbol in word:
                    wordNode, specialSymbolNode = SeperateSpecialCharacterNodes(word, specialSymbol)
                    wordNodes.append(wordNode)
                    wordNodes.append(specialSymbolNode)

            if word in knownWords: wordNodes.append(knownWords[word])        
            elif '-' in word:
                if word not in knownWords:
                    word = word.replace('-', '')
                    if word in knownWords: wordNodes.append(knownWords[word])
                    elif not AskForAssistanceWithWord(word): NewUnsureWordNode(word)
            else: 
                if not AskForAssistanceWithWord(word): NewUnsureWordNode(word)

    if len(newWords) < len(words): return True # Something was received from the text.
    else: return False # Not a word was understood.

def FindMostImportantNodes():
    processes = recentProcesses
    for process in processes:
        pass

def CompactNodesAndFindRelations(nodes):
    for node in nodes:
        concepts = node.concept
        for concept in concepts:
            if concepts[concept] <= 0.2: concepts.pop(concept) # The angle between two points on two different axis is around 10 degrees when their division is equal to 0.2 or 5.
            else:
                for concept2 in concepts:
                    if concept == concept2: pass
                    else:
                        value = concepts[concept2] / concepts[concept]
                        if value <= 0.2: concepts.pop(concept2)
                        elif value >= 5: 
                            concepts.pop(concept)
                            break
    return nodes
                        # The angle between two points on two different axis is 45 degrees when their division is equal to 1.
                            

def NewUnsureWordNode(word):
    newNode = ItemNode([], [], word, [], 1)
    unsureNodes['words'].append(newNode)
    return newNode

def AskForAssistanceWithWord(word):
    if assisted:
        while True:
            print("What is the word: " + word + "? What concepts is it related to? Answer in format: 'concept1:(floatvalue) concept2:(floatvalue)'. If you don't want to answer simply press enter.")
            answer = input()
            if input == "": #TODO: Lisää else osa
                return False
            else:
                try:
                    newInputs = answer.split(' ')
                    concept = {}
                    for newInput in newInputs:
                        split = newInput.split(':')
                        concept[split[0]] = split[1]
                    ItemNode([],[], [word], concept, 1)
                    return True
                except:
                    print("Input in wrong format! Example: person:1 female:1")
    else: return False

def SeperateSpecialCharacterNodes(word, specialSymbol):
    word = word.replace(specialSymbol, '')
    return word, allNodes['words'][specialSymbol]

# create a function for processing shapes and images.

# create a function for self-reflection.