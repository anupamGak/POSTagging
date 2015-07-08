import re

regex = re.compile(r"(.*)\/\/([A-Z]{2})")

infile = open("datasets/train_data2.txt", 'r')
outfile = open("datasets/train_data4.txt", 'w')

curtag = ""
for line in infile:
	sym = re.search(regex, line).groups()[0].lower()
	tag = re.search(regex, line).groups()[1]

	if not curtag == tag:
		outfile.write("\n%s//%s_S" % (tag, sym))
		curtag = tag
	else:
		outfile.write(" %s_C" % sym)

infile.close()
outfile.close()