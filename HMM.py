import re
from collections import Counter

class HMM():
	def __init__(self):
		reTag = re.compile(r" (.+)$", re.MULTILINE)
		reSym = re.compile(r"^(.+) ", re.MULTILINE)
		with open('segment.txt', 'r') as trfile:
			self.data = trfile.read()
		self.taglist = re.findall(reTag, self.data)
		self.symlist = re.findall(reSym, self.data)

		self.tagcount = dict(Counter(self.taglist))
		self.symcount = dict(Counter(self.symlist))

		self.tags = self.tagcount.keys()
		self.syms = self.symcount.keys()

#		self.build_transition()
		self.build_emission()

	def build_transition(self):
		tg_seq = " ".join(self.taglist)

		self.tr_matrix = {}
		for i in self.tags:
			self.tr_matrix[i] = {}
			for j in self.tags:
				N = tg_seq.count(i+" "+j+" ")
				D = tg_seq.count(i)
				self.tr_matrix[i][j] = N/float(D)
		print self.tr_matrix

	def build_emission(self):
		self.em_matrix = {}
		for j in self.tags:
			self.em_matrix[j] = {}
			for k in self.syms:
				N = self.data.count(k+" "+j) + 1
				D = self.data.count(j) + len(self.syms)
				self.em_matrix[j][k] = N/float(D)
		print self.em_matrix


hmm = HMM()
