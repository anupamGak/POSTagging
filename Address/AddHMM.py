import re
from collections import Counter

class OuterHMM():
	def __init__(self):
		reEle = re.compile(r"([A-Z]{2})\/\/")
		reSym = re.compile(r"\/\/(.+)$", re.MULTILINE)
		with open('datasets/train_data3.txt', 'r') as trfile:
			self.data = trfile.read()
		self.elelist = re.findall(reEle, self.data)
		self.symlist = re.findall(reSym, self.data)

		self.elecount = dict(Counter(self.elelist))
		self.symcount = dict(Counter(self.symlist))

		self.eles = self.elecount.keys()
		self.syms = self.symcount.keys()

		print self.elecount
#		self.build_transition()
#		self.build_emission()

	def build_transition(self):
		ele_seq = " ".join(self.elelist)

		self.tr_matrix = {}
		for i in self.eles:
			self.tr_matrix[i] = {}
			for j in self.eles:
				N = ele_seq.count(i+" "+j+" ")
				D = ele_seq.count(i)
				self.tr_matrix[i][j] = N/float(D)
		print self.tr_matrix

	def build_emission(self):
		self.em_matrix = {}
		for j in self.eles:
			self.em_matrix[j] = {}
			for k in self.syms:
				N = self.data.count(j+"//"+k) + 1
				D = self.data.count(j) + len(self.syms)
				self.em_matrix[j][k] = N/float(D)
		print self.em_matrix


hmm = OuterHMM()