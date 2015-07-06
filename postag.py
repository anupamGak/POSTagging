import re
from collections import Counter

reTag = re.compile(r" (.+)$", re.MULTILINE)

with open('postrain.txt', 'r') as trfile:
	tags = re.findall(reTag, trfile.read())

print tags[:15]

