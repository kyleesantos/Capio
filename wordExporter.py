from sys import argv
import numpy as np
import urllib2
import json
import time
from docx import Document

error_codes = { 301: 'Moved Permanently', 302: 'Found',
                304: 'Not Modified', 400: 'Bad Request',
                401: 'Unauthorized', 403: 'Unauthorized',
                404: 'Not Found', 405: 'Method Not Allowed',
                410: 'Gone', 415: 'Unsupported Media Type',
                422: 'Unprocessable Entity', 429: 'Too Many Requests',
                500: 'Internal Service Error' }

def readIDs(file_path):
    transcriptsFile = open(file_path, 'r')
    transcripts = transcriptsFile.read().splitlines()
    return set(transcripts) # converting to set makes lookup time faster

# checks the dictionary of errors and prints the appropriate error message
def handleErrors(status_code):
    if (status_code in error_codes):
        print(error_codes[status_code])
        return False
    return True

# function passes in a transcript and API key and accesses the Capio API
# returns the status code and the json object returned
def accessAPI(transcript, apiKey):
    url = 'https://api.capio.ai/v1/speech/transcript/' + transcript
    header = {'apiKey': apiKey} # uses the API key to access Capio API
    request = urllib2.Request(url,None,header)
    response = urllib2.urlopen(request)
    status_code = response.getcode()
    if (handleErrors(status_code)):
        contents = response.read()
        return (contents, status_code)
    else:
        return ([],0)

# converts seconds of type float to a string with format HH:mm:ss.ss
def timeToString(seconds):
    decimals = '%.2f' % (seconds % 1) # only keeps the decimals
    milliseconds = decimals[1:] # removes the prepending 0
    timestamp = time.strftime('%H:%M:%S', time.gmtime(seconds))
    timestamp += milliseconds
    return timestamp

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

# function takes in a transcript ID, file_path, and API key so the key is not
# committed in a public repository.
def main():
    transcriptID = argv[1]
    out_file = argv[2]
    api_key = argv[3]
    document = Document()
    transcripts = readIDs('transcriptIDs.txt')
    if (transcriptID in transcripts):
        (contents, status_code) = accessAPI(transcriptID, api_key)
        if (status_code != 0):
            writeToFile(contents, document)
    else:
        print("Invalid transcript ID.")
    document.save(out_file)

main()
