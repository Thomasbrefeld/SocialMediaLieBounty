import csv

TOPIC_FILE = 'topic_catigorize.csv'
WEBSITE_FILE = 'topic_to_website.csv'

def readFile(fileName):
    '''
    This function takes a filename as input and returns
    the contents in a usable data format. 
    '''
    fileInput = []
    with open (fileName, 'r', encoding='utf-8-sig') as file: #opens the file
        lineNum = 0
        for line in csv.reader(file, delimiter=','): #parses the file and creates a list of lines
            fileInput.append([])
            for word in line: #loops through each word in the line
                fileInput[lineNum].append(str(word).strip().lower()) # appends the word after cleaning up the word
            lineNum += 1

    return fileInput # returns the list of topics

def reveiwText(inputText):
    '''
    reveiwText takes in a string as returns a list of
    topics that are in that string. topics are defined
    within the topic_catigorize.csv file
    '''
    inputText = str(inputText).strip().lower() #cleans the input data
    fileInput = readFile(TOPIC_FILE) #get the topcs in form of a list
    
    topicsFound = []
    for topic in fileInput: #loop through the topics 
        for discriptor in topic: #loop through the discriptors of the topics
            if (inputText.find(discriptor) > -1 and len(discriptor) > 0): # check if the discriptor is found within the string
                if (topic[0] not in topicsFound): #check if the topic is already in the list
                    topicsFound.append(topic[0]) #add the topic to the list
    
    return topicsFound # return the list of topics

def constructTweet(topics):
    '''
    This function takes the topics as a list, and
    returns a tweet to be posted with the topic and
    links to information about the topics. The links are 
    taken from topic_to_website.csv file.
    '''
    msg = " This tweet has topics involving "

    num = 0 
    for topic in topics: #loop through the topics
        msg += topic # add the topic to the tweet
        if (len(topics) - 1 == num): #add proper grammar following the topic
            msg += ". "
        elif (len(topics) >= 1 and len(topics) - num == 2):
            msg += ", and "
        else:
            msg += ", "

        num += 1
    
    msg += "This might include missleading information, ensure you do you own reasearch at the following website(s): "

    fileInput = readFile(WEBSITE_FILE) # get the topic links

    for topic in topics: # loop throught the topics
        for line in fileInput: #loop through the lines
            if (topic == line[0]): #if the topic is in the lines
                msg += line[1] + " " #append the link to the message
    
    return msg #return the message
        

topics = reveiwText("Almost half a million Americans contract COVID-19 in past week as infections surge") #creates a test tweet
if (len(topics) > 0): #if topics are found within the tweet
    print(constructTweet(topics)) #print the tweet about missleading infomation
else:
    print("clean") #if no topics are found say the tweet is clean
