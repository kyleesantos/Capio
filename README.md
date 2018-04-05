# Capio
This program is a Word Exporter. It takes in a transcription ID and a docx file
to write to. It accesses the Capio API and writes the transcription results of
the inputted ID to the docx file. The repository includes: setup.py,
requirements.txt, wordExporter.py, exporterTests.py, exportedTranscript.docx,
and transcriptIDs.txt. In order to run my code, I used a virtual environment
not included in the repository with required installments listed in the
requirements.txt file. After creating and activating the virtual environment
one can just '$ pip install -r requirements.txt' in order to install the
necessary packages.

Before you run either the test suite or the task code, BE SURE to set the
environment variable API_KEY by calling '$ export API_KEY= <Your API Key>'.

Running the Test Suite:
In order to run the test suite, you must call the exporterTests file giving the
arguments expected in the task code which is an ID and output file. Since I do
not do any integration testing, these values should not matter. For the ID, you
may use '-id 593f237fbcae700012ba8fcd' and for output you may use the given
testing file '-o exportedTranscript.docx'. Please note that running
the test suite does print messages to the command line. This is because I am
testing error cases as well that print to the command line in the task code.

Running the Task Code:
Running the task code is similar in that you must call the wordExporter file
and also give the appropriate arguments. The arguments are a transcription ID
and an output file using the option argument flags -id (--transcriptionid) and
-o (--output), respectively.
