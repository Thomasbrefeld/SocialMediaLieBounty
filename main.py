import csv
import os
import json
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

proirTweetsFile = 'logs/proirTweets.txt'
jsonFile = "logs/tweets.json"
topicFile = 'topic_catigorize.csv'
websiteFile = 'topic_to_website.csv'

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
    fileInput = readFile(topicFile) #get the topcs in form of a list
    
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
    
    msg += "This might include misleading information, ensure you do your own research at the following website(s): "

    fileInput = readFile(websiteFile) # get the topic links

    for topic in topics: # loop throught the topics
        for line in fileInput: #loop through the lines
            if (topic == line[0]): #if the topic is in the lines
                msg += line[1] + " " #append the link to the message
    
    return msg #return the message

def getTweets():
    os.system("snscrape --json --max-results 1 twitter-hashtag softwareengineeringliebounty >" + jsonFile)

    if not os.path.exists(jsonFile):
        return None

    with open(jsonFile) as file:
        return json.load(file)

def isnew(link):
    link = str(link)

    with open(proirTweetsFile) as file:
        for line in file:
            if (link == line[:-1]):
                return False
    
    with open(proirTweetsFile, 'a+') as file:
        file.write(link + "\n")
    
    return True

def publishTweet(url, tweet):
    try:
        driver=webdriver.Chrome("chromedriver.exe")
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@aria-label='Reply']"))).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/a[1]/div"))).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@data-testid='LoginForm_Login_Button']")))
        driver.find_element_by_xpath("//input[@name='session[username_or_email]']").send_keys("SoftwareBot")
        driver.find_element_by_xpath("//input[@name='session[password]']").send_keys("}7mdr~7Xa*,$LVn9XY~B.d!")
        driver.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@aria-label='Reply']"))).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME,'DraftEditor-root'))).click()
        element=driver.find_element_by_class_name('public-DraftEditorPlaceholder-root')
        ActionChains(driver).move_to_element(element).send_keys(str(tweet)).perform()
        driver.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
    except Exception as e:
        print(e)
    finally:
        print("Tweet publishing finished!")
        time.sleep(1)
        driver.close()

if __name__ == "__main__":
    firstRun = True
    while True:
        if not firstRun is True:
            for x in range(20):
                if (x % 10 == 0):
                    print("Refreshing in", str(20 - x), "seconds")
                time.sleep(1)
        else:
            firstRun = False

        tweet = getTweets()
        if not isnew(tweet['url']):
            print('no new tweet, skipping')
            continue
        
        topics = reveiwText(tweet['content'])
        if (len(topics) > 0): 
            publishTweet(tweet['url'], constructTweet(topics))
        else:
            print("The tweet: \"" + str(tweet['content']) + "\" does not contain missleading information")
