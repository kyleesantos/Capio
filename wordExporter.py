import numpy as np
import urllib2
import json
import time
import argparse
from docx import Document

# apiKey = < insert API key here >

# reads in all transcript IDs and returns them in a list
def readIDs(file_path):
    transcriptsFile = open(file_path, 'r')
    transcripts = transcriptsFile.read().splitlines()
    return transcripts

# function passes in a transcript and API key and accesses the Capio API
# returns the status code and the json object returned
def accessAPI(transcripts, transcript, apiKey):
    if (transcript not in transcripts):
        print("Invalid transcript ID.")
        return None
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

# function takes in a transcript ID, file_path, and API key so the key is not
# committed in a public repository.
def main():
    parser = argparse.ArgumentParser(description='Read transcript and docx')
    parser.add_argument('-id', '--transcriptionid', help='input transcript ID')
    parser.add_argument('-o', '--output', help='file name to write to')
    args = parser.parse_args()
    if (args.transcriptionid == None):
        print('Please enter a transcription ID.')
        return
    else:
        transcriptID = args.transcriptionid
    if (args.output == None):
        print('Please enter an output file')
        return
    else:
        out_file = args.output
    document = Document()
    transcripts = readIDs('transcriptIDs.txt')
    contents = accessAPI(transcripts, transcriptID, apiKey)
    if (contents != None):
        writeToFile(contents, document)
        document.save(out_file)

main()
