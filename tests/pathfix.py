#Fixes pytest path problems
#May break the Python interpreter's ability to run this program
import sys
import os

def fixpath():
	corrected_path = os.path.dirname(os.path.abspath(__file__))
	sys.path.insert(0, corrected_path + '/../')
