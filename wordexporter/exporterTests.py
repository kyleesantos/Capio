import unittest
import argparse
import sys
from docx import Document
from wordExporter import accessAPI, timeToString, writeToFile

# manually inputting list as to prevent dependencies in test cases
transcriptIDs = ['593f237fbcae700012ba8fcd', '591a6212afb4c4000e152a5f',
                    '591a62121c61b0000f045b90', '591a6211401d770011d4e284',
                    '591a62109e5063001856ab77', '591a6210afb4c4000e152a5d',
                    '591a620f1c61b0000f045b8e', '591a620b9e5063001856ab75',
                    '591a620b95d2db000d22b0a0', '591a6207e2428b0023ebd8bf',
                    '591a620795d2db000d22b09e', '591a6207e2428b0023ebd8be',
                    '591a62079e5063001856ab73', '591a6201e1ca18001073f761',
                    '591a620095d2db000d22b09c', '591a61ff1452a00012013deb',
                    '591a61ffafb4c4000e152a5b', '591a61fe1c61b0000f045b8c',
                    '591a61fc9e5063001856ab71', '591a61f91c61b0000f045b8a',
                    '591a61f51c61b0000f045b88', '591a616895d2db000d22b099',
                    '591a616795d2db000d22b098', '591a61669e5063001856ab6f',
                    '591a6165e1ca18001073f75f', '591a61651c61b0000f045b85',
                    '591a616595d2db000d22b096', '591a6161e1ca18001073f75d',
                    '591a615e95d2db000d22b094', '591a615e1c61b0000f045b83',
                    '591a615eafb4c4000e152a59', '591a615e9e5063001856ab6d',
                    '591a615ce1ca18001073f75b', '591a615795d2db000d22b092',
                    '591a6156afb4c4000e152a57', '591a6154afb4c4000e152a55',
                    '591a61541452a00012013de9', '591a615495d2db000d22b090',
                    '591a6152e2428b0023ebd8bc', '591a61509e5063001856ab6b',
                    '591a614b9e5063001856ab69', '591a60ff401d770011d4e281',
                    '591a60ff9e5063001856ab67', '591a60ff401d770011d4e280',
                    '591a60feafb4c4000e152a53', '591a60fde1ca18001073f759',
                    '591a60fa401d770011d4e27e', '591a60f79e5063001856ab64',
                    '591a60f79e5063001856ab63', '591a60f7e1ca18001073f757',
                    '591a60f59e5063001856ab61', '591a60f4e1ca18001073f755',
                    '591a60f1afb4c4000e152a51', '591a60f01452a00012013de6',
                    '591a60ef1c61b0000f045b81', '591a60edafb4c4000e152a4f',
                    '591a60eae1ca18001073f753', '591a60eaafb4c4000e152a4d',
                    '591a60e9e2428b0023ebd8b9', '591a60e795d2db000d22b08e',
                    '591a60e51452a00012013de4', '591a60a6afb4c4000e152a4b',
                    '591a60a61452a00012013de2', '591a60a6e2428b0023ebd8b7',
                    '591a60a49e5063001856ab5f', '591a60a4401d770011d4e27c',
                    '591a60a29e5063001856ab5c', '591a60a19e5063001856ab5b',
                    '591a609f401d770011d4e27a', '591a609d1452a00012013de0',
                    '591a609cafb4c4000e152a49', '591a609ce1ca18001073f751',
                    '591a6099e1ca18001073f74f', '591a6094401d770011d4e278',
                    '591a60949e5063001856ab59', '591a60941c61b0000f045b7f',
                    '591a60931452a00012013dde', '591a6093e2428b0023ebd8b5',
                    '591a6091afb4c4000e152a47', '591a608dafb4c4000e152a45',
                    '591a608ae1ca18001073f74c', '591a5011afb4c4000e152a40',
                    '591a50111c61b0000f045b7a', '591a50101452a00012013dda',
                    '591a500fe1ca18001073f749', '591a500f1452a00012013dd8',
                    '591a500dafb4c4000e152a3e', '591a50099e5063001856ab55',
                    '591a5008afb4c4000e152a3c', '591a50071c61b0000f045b78',
                    '591a5007e1ca18001073f747', '591a50051452a00012013dd6',
                    '591a5004401d770011d4e275', '591a5001e1ca18001073f745',
                    '591a50001452a00012013dd4', '591a4ffd9e5063001856ab53',
                    '591a4ffc95d2db000d22b087', '591a4ffbe2428b0023ebd8b1',
                    '591a4ffbe2428b0023ebd8b0', '591a4ff79e5063001856ab51',
                    '591a4ff4afb4c4000e152a3a']

class WordExporterTests(unittest.TestCase):
    # tests for wordExporter.py

    def test_accessAPI(self):
        # ensures that the function correctly accesses the Capio API or returns
        # None if there is a status code error

        # checks if the function successfully retrieves all valid transcripts
        for transcript in transcriptIDs:
            contents = accessAPI(transcriptIDs, transcript, apiKey)
            self.assertNotEqual(contents,None,
                                msg='Failed to retrieve valid transcript')

        # checks if the function correctly returns None if no transcript match
        # is inputted
        contents = accessAPI(transcriptIDs, "no match", apiKey)
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

        # runs through all transcripts to check if
        for transcript in transcriptIDs:
            document = Document()
            contents = accessAPI(transcriptIDs, transcript, apiKey)
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
