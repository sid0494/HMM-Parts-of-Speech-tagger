import sys, ast
from collections import defaultdict

hmm_model_path = "hmmmodel.txt"
test_file_path = sys.argv[1]

def load_model(hmm_path, transition, emission):
	file = open(hmm_path)

	file.readline()

	n = int(file.readline().rstrip("\n"))
	for i in range(0, n):
		tag = file.readline().rstrip("\n")
		transition[tag] = ast.literal_eval(file.readline().rstrip("\n"))

	file.readline()

	m = int(file.readline().rstrip("\n"))
	for i in range(0, m):
		tag = file.readline().rstrip("\n")
		emission[tag] = ast.literal_eval(file.readline().rstrip("\n"))



transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))
load_model(hmm_model_path, transition, emission)





