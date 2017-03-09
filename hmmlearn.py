# coding=UTF-8
import math
from collections import defaultdict

def parse_sent(sent, transition, emission):
	
	tokens = sent.rstrip("\n").split()

	current_word = tokens[0][:-3]
	current_tag = tokens[0][-2:]
	print tokens
	transition["start_state"][current_tag] += 1

	for i in range(1,len(tokens)):
		next_tag = tokens[i][-2:]
		# print current_word, current_tag, next_tag
		# print "!!!!!!!!!"
		transition[current_tag][next_tag] += 1
		emission[current_tag][current_word] += 1
		current_word = tokens[i][:-3]
		current_tag = next_tag

	emission[current_tag][current_word] += 1

def smoothing_transition(matrix):

	tags = matrix.keys()

	for tag1 in tags:
		for tag2 in tags:
			matrix[tag1][tag2] += 1


def convert_to_probabilities(matrix):

	print len(matrix)
	for key in matrix:
		total = sum(matrix[key].values())
		print key, len(matrix[key])
		for k in matrix[key]:
			matrix[key][k] /= total




transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))

input_file = open("catalan_corpus_train_tagged.txt")
output_file = open("hmmmodel.txt","w")

for l in input_file:
	parse_sent(l, transition, emission)
	# raw_input()

smoothing_transition(transition)
convert_to_probabilities(transition)
print "Emission starts from here"
convert_to_probabilities(emission)
output_file.write("~~~~~~~~~~~~~Transition Probabilities~~~~~~~~~~~~~~~~~~~\n")
output_file.write(str(len(transition)) + "\n")

for key in transition:
	output_file.write(key + "\n" + str(dict(transition[key])) + "\n")

output_file.write("~~~~~~~~~~~~~Emission Probabilities~~~~~~~~~~~~~~~~~~~\n")
output_file.write(str(len(emission)) + "\n")

for key in emission:
	output_file.write(key + "\n" + str(dict(emission[key])) + "\n")


input_file.close()
output_file.close()