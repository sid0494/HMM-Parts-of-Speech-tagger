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
		transition[tag] = defaultdict(lambda: -99999.0, ast.literal_eval(file.readline().rstrip("\n")))

	file.readline()

	m = int(file.readline().rstrip("\n"))
	for i in range(0, m):
		tag = file.readline().rstrip("\n")
		emission[tag] = defaultdict(lambda: -99999.0, ast.literal_eval(file.readline().rstrip("\n")))

	file.readline()

	vocabulary = defaultdict(int, ast.literal_eval(file.readline().rstrip("\n")))
	return vocabulary


def tag_data(sent, transition, emission, vocabulary, tag_list):
	
	words = sent.split()
	probability = defaultdict(float)
	backpointer = defaultdict(str)
	answer = ""
	counter = 1

	for tag in tag_list:

		if vocabulary[words[0]] == 1:
			probability[(tag, counter)] = transition["start_state"][tag] + emission[tag][words[0]]
		else:
			probability[(tag, counter)] = transition["start_state"][tag]

		backpointer[(tag, counter)] = "start_state"
	
	counter += 1 
	next_tag_list = tag_list
	
	for w in words[1:]:
		tag_list1 = next_tag_list if len(next_tag_list) > 0 else tag_list
		next_tag_list = []
		for tag in tag_list:

			emission_value = emission[tag][w] if vocabulary[w] == 1 else 0
			backpointer[(tag, counter)] = max(tag_list1, key = lambda tag2: probability[(tag2, counter - 1)] + transition[tag2][tag])
			prev_tag = backpointer[(tag, counter)]
			probability[(tag, counter)] = probability[(prev_tag, counter - 1)] + transition[prev_tag][tag] + emission_value

			if probability[(tag, counter)] >= MIN_VALUE:
				next_tag_list.append(tag)
		
		counter += 1
	
	most_likely_tags = []
	most_likely_tags.append(max(tag_list, key = lambda tag: probability[(tag, counter - 1)]))
	counter = len(words)

	while counter > 0:
		most_likely_tags.append(backpointer[(most_likely_tags[-1], counter)])
		counter -= 1

	most_likely_tags = most_likely_tags[::-1][1:]

	for i in range(0, len(words)):
		answer += words[i] + "/" + most_likely_tags[i] + " "

	return answer + "\n"
	



start = timeit.default_timer()



transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(lambda: -99999))
vocabulary = load_model(hmm_model_path, transition, emission)
test_file = open(test_file_path)
output_file = open("hmmoutput.txt", "w")
output_data = ""
tag_list = transition.keys()
tag_list.remove("start_state")

for l in test_file:
	output_data += tag_data(l.rstrip("\n"), transition, emission, vocabulary, tag_list)

stop = timeit.default_timer()
output_file.write(output_data)


print stop - start