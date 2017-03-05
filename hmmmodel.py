# coding=UTF-8

import math

from collections import defaultdict

def parse_sent(sent, transition, emission):
	
	tokens = sent.rstrip("\n").split()

	current_word = tokens[0][:-3]
	current_tag = tokens[0][-2:]
	print tokens

	for i in range(1,len(tokens)):
		next_tag = tokens[i][-2:]
		print current_word, current_tag, next_tag
		print "!!!!!!!!!"
		transition[current_tag][next_tag] += 1
		emission[current_tag][current_word] += 1
		current_word = tokens[i][:-3]
		current_tag = next_tag

	emission[current_tag][current_word] += 1


def convert_to_probabilities(matrix):

	for key in matrix:
		total = sum(matrix[key].values())
		for k in matrix[key]:
			matrix[key][k] /= total




transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))

input_file = open("test.txt")

for l in input_file:
	parse_sent(l, transition, emission)
	# raw_input()

convert_to_probabilities(transition)
convert_to_probabilities(emission)
print "~~~~~~~~~~~~~Transition Probabilities~~~~~~~~~~~~~~~~~~~"

for key in transition:
	print key + " " + str(transition[key])

print "~~~~~~~~~~~~~Emission Probabilities~~~~~~~~~~~~~~~~~~~"

for key in emission:
	print key + " " + str(emission[key])
# parse_sent(s, transition, emission)

# print transition,emission