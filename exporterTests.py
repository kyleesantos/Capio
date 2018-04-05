import unittest
import argparse
import sys
from docx import Document
from wordExporter import readIDs, accessAPI, timeToString, writeToFile

# apiKey = < insert API key here >

class WordExporterTests(unittest.TestCase):
    # tests for wordExporter.py

    def test_read_IDs(self):
        # ensures that the function correctly reads from "transcriptIDs.txt"
        transcripts = readIDs('transcriptIDs.txt')
        length = len(transcripts)

        # checks if readIDs reads all transcripts from file
        self.assertEqual(length, 101, msg='Not reading all transcripts')

        # checks if the entire line is read into each element of the set
        for index in range(length):
            string_length = len(transcripts[index])
            self.assertEqual(string_length, 24, msg='Not reading transcript')

    def test_accessAPI(self):
        # ensures that the function correctly accesses the Capio API or returns
        # None if there is a status code error

        transcripts = readIDs('transcriptIDs.txt')
        # checks if the function successfully retrieves all valid transcripts
        for transcript in transcripts:
            contents = accessAPI(transcripts, transcript, apiKey)
            self.assertNotEqual(contents,None,
                                msg='Failed to retrieve valid transcript')

        # checks if the function correctly returns None if no transcript match
        # is inputted
        contents = accessAPI(transcripts, "no match", apiKey)
        self.assertEqual(contents,None,msg='Not catching invalid transcript ID')

    def test_time_to_string(self):
        # ensures that the function correctly converts a time in seconds to
        # HH:mm:ss.ss

        times = [0.0, 1, 2.34, 12.3456, 12.34321, 12.399, 62, 1312.7, 3681.2]
        timestamps = ["00:00:00.00", "00:00:01.00", "00:00:02.34",
                        "00:00:12.35", "00:00:12.34", "00:00:12.40",
                        "00:01:02.00", "00:21:52.70", "01:01:21.20"]

        # checks the function correctly output a string for above test cases
        for index in range(len(times)):
            output = timeToString(times[index])
            self.assertEqual(output,timestamps[index],
                                msg='Incorrect time string formatting')

    def test_writeToFile(self):
        # ensures that the function correctly writes contents of json to docx

        transcripts = readIDs('transcriptIDs.txt')
        # runs through all transcripts to check if
        for transcript in transcripts:
            document = Document()
            contents = accessAPI(transcripts, transcript, apiKey)
            writeToFile(contents, document)
            counter = 0
            for para in document.paragraphs:
                # check that doc isn't empty
                self.assertNotEqual(para.text, '', msg="Empty doc")
                counter += 1

            # since for each transcript all of the text is added to a single
            # paragraph of each document, check if counter is 1 to make ensure
            # documents are not being written over
            self.assertEqual(counter, 1, msg='Over-writing docs')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--transcriptionid')
    parser.add_argument('-o', '--output')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()
    sys.argv[1:] = args.unittest_args
    unittest.main()
