from classes import ItemNode, Process
from classes import nodes
global allItems
allItems = nodes # Key: concept # Value: list of nodes

def Read(text, language=None):
    if language is None:
        # Figure out the language.
        pass
    else:
        sentences = text.split('. | ,')
        for sentence in sentences:
            newProcess = Process(FindNodesFromSentece(sentence), 'read').process()


def FindNodesFromSentece(sentence, language=None):
    items = []
    if language is None:
        pass
    else:
        words = sentence.lower().split()
        knownWords = allItems['words'] # Words has mmultiple values for a single word. Filter by language to get language precise nodes.

        for word in words:
            if word in knownWords:
                items.append(knownWords[word])
            elif word in allItems[word]:
                    #create a new word item
                    break
            else:
                #create a new item and a word for it.
                break
    return items

# create a function for processing shapes and images.

# create a function for self-reflection.