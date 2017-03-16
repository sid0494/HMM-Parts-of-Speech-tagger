counter = 0
total = 0

f1 = open("catalan_corpus_dev_tagged.txt")
f2 = open("hmmoutput.txt")

data_in = []
data_out = []

data_in += f1
data_out += f2


for i in range(0, len(data_in)):
	l1 = data_in[i].split()
	l2 = data_out[i].split()
	for j in range(0, len(l1)):
		if l1[j] == l2[j]:
			counter += 1
		total += 1

print "Total = {}\nCorrect = {}\nAccuracy = {}\n".format(counter, total, float(counter * 100)/total)