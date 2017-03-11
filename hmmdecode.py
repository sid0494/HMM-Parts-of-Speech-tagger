import sys, ast, math, timeit
from collections import defaultdict

hmm_model_path = "hmmmodel.txt"
test_file_path = sys.argv[1]
MIN_VALUE = -99999

def load_model(hmm_path, transition, emission):
	file = open(hmm_path)

	file.readline()

	n = int(file.readline().rstrip("\n"))
	for i in range(0, n):
		tag = file.readline().rstrip("\n")
		transition[tag] = defaultdict(float, ast.literal_eval(file.readline().rstrip("\n")))

	file.readline()

	m = int(file.readline().rstrip("\n"))
	for i in range(0, m):
		tag = file.readline().rstrip("\n")
		emission[tag] = defaultdict(float, ast.literal_eval(file.readline().rstrip("\n")))

	file.readline()

	vocabulary = defaultdict(int, ast.literal_eval(file.readline().rstrip("\n")))
	return vocabulary
	# print vocabulary
	# raw_input()

def get_log_emission(value):
	if value != 0.0:
		return math.log(value)
	else:
		return MIN_VALUE


def tag_data(sent, transition, emission, vocabulary):
	
	words = sent.split()
	probability = defaultdict(float)
	backpointer = defaultdict(str)
	tag_list = transition.keys()
	answer = ""
	counter = 1
	debug = 0
	tag_list.remove("start_state")
	for tag in tag_list:
		# print transition["start_state"][tag], emission[tag][words[0]]
		if vocabulary[words[0]] == 1:
			probability[(tag, counter)] = transition["start_state"][tag] + emission[tag][words[0]]
		else:
			probability[(tag, counter)] = transition["start_state"][tag]
		backpointer[(tag, counter)] = "start_state"
		# print probability[(tag, counter)], tag
		debug += 1
	counter += 1 
	# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	for w in words[1:]:

		for tag in tag_list:
			if vocabulary[w] == 1:
				probability[(tag, counter)] = max([probability[(tag2, counter - 1)] + transition[tag2][tag] + emission[tag][w] for tag2 in tag_list])
			else:
				probability[(tag, counter)] = max([probability[(tag2, counter - 1)] + transition[tag2][tag] for tag2 in tag_list])
			
			backpointer[(tag, counter)] = max(tag_list, key = lambda tag2: probability[(tag2, counter - 1)] + transition[tag2][tag])
			# print probability[(tag, counter)], backpointer[(tag, counter)], tag
		counter += 1
		# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		# raw_input()
	
	most_likely_tags = []
	# print [probability[(tag, counter)] for tag in tag_list], len(words)
	# raw_input()
	# for tag in tag_list:
	# 	print probability[(tag, counter - 1)], tag
	most_likely_tags.append(max(tag_list, key = lambda tag: probability[(tag, counter - 1)]))
	counter = len(words)

	# print words

	while counter > 0:
		# print backpointer[(most_likely_tags[-1], counter)], counter
		most_likely_tags.append(backpointer[(most_likely_tags[-1], counter)])
		counter -= 1
		# raw_input()



	most_likely_tags = most_likely_tags[::-1][1:]

	for i in range(0, len(words)):
		answer += words[i] + "/" + most_likely_tags[i] + " "

	# print answer

	return answer + "\n"

	



start = timeit.default_timer()



transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(lambda: -99999))
vocabulary = load_model(hmm_model_path, transition, emission)
test_file = open(test_file_path)
output_file = open("hmmoutput.txt", "w")
count = 1
for l in test_file:
	# print count, " done"
	# count += 1 
	output_file.write(tag_data(l.rstrip("\n"), transition, emission, vocabulary))

stop = timeit.default_timer()

print stop - start

