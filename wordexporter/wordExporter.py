import urllib2
import json
import time
import argparse
import os
from docx import Document

# function passes in a transcript and API key and accesses the Capio API
# returns the status code and the json object returned
def accessAPI(transcript, apiKey):
    url = 'https://api.capio.ai/v1/speech/transcript/' + transcript
    header = {'apiKey': apiKey} # uses the API key to access Capio API
    request = urllib2.Request(url,headers=header)
    try:
        # tries to access Capio API
        response = urllib2.urlopen(request)
        contents = response.read()
        return contents
    except urllib2.HTTPError, e:
        # exception is handled by printing error and return None
        print(e)
        return None

# converts seconds of type float to a string with format HH:mm:ss.ss
def timeToString(seconds):
    decimals = '%.2f' % (seconds % 1) # only keeps the decimals
    milliseconds = decimals[1:] # removes the prepending 0
    timestamp = time.strftime('%H:%M:%S', time.gmtime(seconds))
    timestamp += milliseconds
    return timestamp

# inputs the contents of the json and writes the timestamp and transcript in
# the inputted docx document
def writeToFile(contents, document):
    paragraph = ''
    readable = json.loads(contents)
    for index in range(len(readable)):
        sentence = readable[index] #turn json object to dictionary
        seconds = sentence['result'][0]['alternative'][0]['words'][0]['from']
        timestamp = timeToString(seconds)
        words = sentence['result'][0]['alternative'][0]['transcript']
        paragraph += timestamp + '\t' + words + '\n'
    document.add_paragraph(paragraph)

# function takes in a transcript ID and file_path and uses helper functions to
# access the Capio API and write the results of the ID's transcription to the
# inputted file.
def main():
    parser = argparse.ArgumentParser(description='Read transcript and docx')
    parser.add_argument('-id', '--transcriptionid', help='input transcript ID')
    parser.add_argument('-o', '--output', help='file name to write to')
    args = parser.parse_args()

    # check if arguments were passed in. if not, give appropriate message
    if (args.transcriptionid == None):
        print('Please enter a transcription ID.')
        return
    else:
        transcriptID = args.transcriptionid
    if (args.output == None):
        print('Please enter an output file.')
        return
    else:
        out_file = args.output

    apiKey = os.environ.get('API_KEY')
    if (apiKey == None):
        print('Please set the environment variable API_KEY to access the API.')
        return

    document = Document()
    contents = accessAPI(transcriptID, apiKey)
    if (contents != None): # checks if error occurred when accessing the API
        writeToFile(contents, document)
        document.save(out_file)

main()
