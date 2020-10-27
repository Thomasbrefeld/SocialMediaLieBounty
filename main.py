import csv

TOPIC_FILE = 'topic_catigorize.csv'
WEBSITE_FILE = 'topic_to_website.csv'

def readFile(fileName):

    fileInput = []
    with open (fileName, 'r', encoding='utf-8-sig') as file:
        lineNum = 0
        for line in csv.reader(file, delimiter=','):
            fileInput.append([])
            for word in line:
                fileInput[lineNum].append(str(word).strip().lower())
            lineNum += 1

    return fileInput

def reveiwText(inputText):
    inputText = str(inputText).strip().lower()
    fileInput = readFile(TOPIC_FILE)
    
    topicsFound = []
    for topic in fileInput:
        for discriptor in topic:
            if (inputText.find(discriptor) > -1 and len(discriptor) > 0):
                if (topic[0] not in topicsFound):
                    topicsFound.append(topic[0])
    
    return topicsFound

def constructTweet(topics):
    msg = " This tweet has topics involving "

    num = 0
    for topic in topics:
        msg += topic
        if (len(topics) - 1 == num):
            msg += ". "
        elif (len(topics) >= 1 and len(topics) - num == 2):
            msg += ", and "
        else:
            msg += ", "

        num += 1
    
    msg += "This might include missleading information, ensure you do you own reasearch at the following website(s): "

    fileInput = readFile(WEBSITE_FILE)

    for topic in topics:
        for line in fileInput:
            if (topic == line[0]):
                msg += line[1] + " "
    
    return msg
        

topics = reveiwText("Almost half a million Americans contract COVID-19 in past week as infections surge")
if (len(topics) > 0):
    print(constructTweet(topics))
else:
    print("clean")