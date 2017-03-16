# coding=UTF-8
import sys, math
from collections import defaultdict

def parse_sent(sent, transition, emission, tag_count):
	
	tokens = sent.rstrip("\n").split()

	# current_word = tokens[0][:-3].lower()
	current_word = tokens[0][:-3]
	current_tag = tokens[0][-2:]
	# print tokens
	vocabulary[current_word] = 1
	transition["start_state"][current_tag] += 1
	tag_count[current_tag] += 1

	for i in range(1,len(tokens)):
		next_tag = tokens[i][-2:]
		tag_count[next_tag] += 1
		# print current_word, current_tag, next_tag
		# print "!!!!!!!!!"
		transition[current_tag][next_tag] += 1
		emission[current_tag][current_word] += 1
		# current_word = tokens[i][:-3].lower()
		current_word = tokens[i][:-3]
		current_tag = next_tag
		vocabulary[current_word] = 1

	emission[current_tag][current_word] += 1

def smoothing_transition(matrix):

	tags = matrix.keys()

	for tag1 in tags:
		for tag2 in tags:
			if tag2 != "start_state":
				matrix[tag1][tag2] += 0.5
			# else:
			# 	matrix[tag1][tag2] += 1


def convert_to_probabilities(matrix):

	# print len(matrix)
	for key in matrix:
		total = sum(matrix[key].values())
		# print key, len(matrix[key])
		for k in matrix[key]:
			# matrix[key][k] /= total
			# if matrix[key][k]/total != 0:
			matrix[key][k] = math.log(matrix[key][k]/total)
			# else:
			# 	print key,k
			# 	matrix[key][k] = -99999

def convert_to_probabilities_trans(matrix, tag_count):
	alpha = 0.9
	total_tags = sum(tag_count.values())
	tag_list = matrix.keys()
	for tag1 in tag_list:
		total = sum(matrix[tag1].values())
		for tag2 in tag_list:
			if tag2 != "start_state":
				matrix[tag1][tag2] = math.log(alpha * (matrix[tag1][tag2]/total) + (1 - alpha) * (float(tag_count[tag2])/total_tags))




transition = defaultdict(lambda: defaultdict(float))
emission = defaultdict(lambda: defaultdict(float))
tag_count = defaultdict(float)
vocabulary = {}

train_file_path = sys.argv[1]
input_file = open(train_file_path)
# input_file = open("test.txt")
output_file = open("hmmmodel.txt","w")

for l in input_file:
	parse_sent(l, transition, emission, tag_count)
	# raw_input()



# smoothing_transition(transition)
convert_to_probabilities_trans(transition, tag_count )
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


output_file.write("~~~~~~~~~~~~~Vocabulary~~~~~~~~~~~~~~~~~~~~~~~~\n")
output_file.write(str(vocabulary))
print "DONE"

input_file.close()
output_file.close()