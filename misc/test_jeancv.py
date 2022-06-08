import sys # for Command Line Arguments
from jeanCV import skinDetector


imageName = sys.argv[1]

detector = skinDetector(imageName)
detector.find_skin()