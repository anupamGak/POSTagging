import re
from collections import Counter

class OuterHMM():
	def __init__(self, sent):
		self.sent = sent.split()
		reEle = re.compile(r" ([A-Z,.:]+)$", re.MULTILINE)
		reSym = re.compile(r"^(.+) ", re.MULTILINE)
		with open('datasets/segment.txt', 'r') as trfile:
			self.data = trfile.read()
		self.elelist = re.findall(reEle, self.data)
		self.symlist = re.findall(reSym, self.data)

		self.elecount = dict(Counter(self.elelist))
		self.symcount = dict(Counter(self.symlist))

		self.eles = self.elecount.keys()
		self.syms = self.symcount.keys()
		print len(self.eles)

		self.build_transition()
		self.build_emission()

	def build_transition(self):
		ele_seq = " ".join(self.elelist)

		self.tr_matrix = {}
		for i in self.eles:
			self.tr_matrix[i] = {}
			for j in self.eles:
				if i == '.':
					self.tr_matrix[i][j] = 0
				else:
					N = ele_seq.count(i+" "+j+" ")
					D = ele_seq.count(i)
					self.tr_matrix[i][j] = N/float(D)
#		print self.tr_matrix
		print "Transition matrix built"

	def build_emission(self):
		self.em_matrix = {}
		for j in self.eles:
			self.em_matrix[j] = {}
			for k in self.syms:
				N = self.data.count(k+" "+j) + 1
				D = self.data.count(j) + len(self.syms)
				self.em_matrix[j][k] = N/float(D)
		print "Emission matrix built"
#		print self.em_matrix

	def v(self, s, i):
		if i == 0:
			return 1
		else:
			n = self.eles
			max = 0
			for r in n:
				x = self.tr_matrix[r][s] * self.v(r,i-1)
				if x > max:
					max = x
#			print s, self.sent[i-1]
			return max * self.em_matrix[s][self.sent[i-1]]

	def final(self):
		n = self.eles
		max = 0
		count = 0
		for r in n:
			print count
			count += 1
			x = self.tr_matrix[r]['.'] * self.v(r,6)
			if x > max:
				max = x
				maxres = res
		return max



sent = "to dive another show from deficits"
hmm = OuterHMM(sent)