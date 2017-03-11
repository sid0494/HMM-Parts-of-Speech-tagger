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


def tag_data(sent, transition, emission, vocabulary):
	
	words = sent.split()
	probability = defaultdict(float)
	backpointer = defaultdict(str)
	tag_list = transition.keys()
	answer = ""
	counter = 1
	debug = 0
	for tag in tag_list:
		# print transition["start_state"][tag], emission[tag][words[0]]
		if vocabulary[words[0]] == 1:
			probability[(tag, counter)] = transition["start_state"][tag] * emission[tag][words[0]]
		else:
			probability[(tag, counter)] = transition["start_state"][tag]
		backpointer[(tag, counter)] = "start_state"
		# print probability[(tag, counter)], tag
		debug += 1
	counter += 1 
	# tag_list.remove("start_state")
	for w in words[1:]:
		# w = w.lower()
		current = 0
		for tag in tag_list:
			if vocabulary[w] == 1:
				print "Here", w, emission[tag][w], tag
				if w == "(" and tag == "FF":
					for tag2 in tag_list:
						temp = probability[(tag2, counter - 1)] * transition[tag2][tag] * emission[tag][w]
						# print temp, tag2, transition[tag2][tag], probability[(tag2, counter - 1)]
						if temp != 0:
							print tag2, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
							raw_input()
						print probability[(tag, counter)]
						probability[(tag, counter)] = max(probability[(tag, counter)], temp)
				else:
					probability[(tag, counter)] = max(probability[(tag2, counter - 1)] * transition[tag2][tag] * emission[tag][w] for tag2 in tag_list)
			else:
				# print "Here", w
				probability[(tag, counter)] = max(probability[(tag2, counter - 1)] * transition[tag2][tag] for tag2 in tag_list)
				# if probability[(tag, counter)] == 0:
				# 	# print tag, counter
				# 	# raw_input()
			backpointer[(tag, counter)] = max(tag_list, key = lambda tag2: probability[(tag2, counter - 1)] * transition[tag2][tag])
			print backpointer[(tag, counter)]
				# if tag == "NP":
				# 	print probability[(tag2, counter - 1)], transition[tag2][tag], emission[tag][w], tag, tag2, w , backpointer[(tag, counter)]
				# 	raw_input()
			if probability[(tag, counter)] == 0:
				probability[(tag, counter)], tag, w, backpointer[(tag, counter)], counter
			else:
				current += 1
		if current == 0:
			print w, "Boom boom shakalaka"
			raw_input()
		
		# raw_input()
		counter += 1
		# print w, counter
	
	most_likely_tags = []
	# print [probability[(tag, counter)] for tag in tag_list], len(words)
	raw_input()
	most_likely_tags.append(max(tag_list, key = lambda tag: probability[(tag, counter - 1)]))
	counter -= 1

	# print words

	while counter > 0:
		print backpointer[(most_likely_tags[-1], counter)], counter
		most_likely_tags.append(backpointer[(most_likely_tags[-1], counter)])
		counter -= 1
		# raw_input()

	most_likely_tags = most_likely_tags[::-1][1:]

	for i in range(0, len(words)):
		answer += words[i] + "/" + most_likely_tags[i] + " "

	return answer + "\n"

	






transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))
vocabulary = load_model(hmm_model_path, transition, emission)
test_file = open(test_file_path)
output_file = open("hmmoutput.txt", "w")
count = 1
for l in test_file:
	print count, " done"
	count += 1 
	output_file.write(tag_data(l.rstrip("\n"), transition, emission, vocabulary))



