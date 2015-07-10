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



class MyHMM:
	pairs = []
	def __init__(self, sent):
		self.sent = sent.split()
		self.sent.insert(0, '>')
		self.sent2 = self.sent
		self.N = len(self.sent)
		reSt = re.compile(r"\/\/([A-Z]+)")
		reSy = re.compile(r"(?:^|[\s])(.+?)\/\/")
		reg = re.compile(r"(.+?)\/\/([A-Z]+)")
		with open('datasets/refined_data.txt', 'r') as trfile:
			self.data = trfile.read()
		with open('datasets/refined_data.txt', 'r') as trfile:
			for line in trfile:
				ps = line.split()
				for p in ps:
					pr = re.search(reg, p).groups()
					self.pairs.append(list(pr))

		self.stlist = re.findall(reSt, self.data)
		self.sylist = re.findall(reSy, self.data)

		self.input_handle()
		self.sparce_handle()

		self.stcount = dict(Counter(self.stlist))
		self.sycount = dict(Counter(self.sylist))

		self.sts = self.stcount.keys()
		self.sys = self.sycount.keys()

		self.build_transition()
		self.build_emission()

	def input_handle(self):
		for i in range(len(self.sent)):
			if re.search("\d{6}", self.sent[i]):
				self.sent[i] = "pincode"
		for i in range(len(self.sent)):
			if re.search(r"[-\d.:\/]+", self.sent[i]):
				self.sent[i] = "number"
		for i in range(len(self.sent)):
			if self.sylist.count(self.sent[i]) < 2 and not self.sent[i] == "pincode" and not self.sent[i] == "number":
				self.sent[i] = "name"






	def sparce_handle(self):
		for i in range(len(self.sylist)):
			if re.search("\d{6}", self.sylist[i]):
				self.sylist[i] = "pincode"
		for i in range(len(self.sylist)):
			if re.search(r"[-\d.:\/]+", self.sylist[i]):
				self.sylist[i] = "number"
		for i in range(len(self.sylist)):
			if self.sylist.count(self.sylist[i]) < 2:
				self.sylist[i] = "name"

		for i in range(len(self.pairs)):
			if re.search("\d{6}", self.pairs[i][0]):
				self.pairs[i][0] = "pincode"
		for i in range(len(self.pairs)):
			if re.search(r"[-\d.:\/]+", self.pairs[i][0]):
				self.pairs[i][0] = "number"

		for i in range(len(self.pairs)):
			if self.data.count(self.pairs[i][0]) < 2 and not self.pairs[i][0] == 'pincode':
				self.pairs[i][0] = "name"


	def build_transition(self):
		st_seq = " ".join(self.stlist)

		self.tr_matrix = {}
		for i in self.sts:
			self.tr_matrix[i] = {}
			for j in self.sts:
				if i == 'SO':
					self.tr_matrix[i][j] = 0
				else:
					N = st_seq.count(i+" "+j+" ")
					D = st_seq.count(i)
					self.tr_matrix[i][j] = N/float(D)
#		print self.tr_matrix

	def build_emission(self):
		self.em_matrix = {}
		for j in self.sts:
			self.em_matrix[j] = {}
			for k in self.sys:
				N = self.pairs.count([k,j]) + 1
				D = self.data.count(j) + len(self.sys)
				self.em_matrix[j][k] = N/float(D)
#		print self.em_matrix

	def v(self, s, i):
		if s == 'SR':
			if i == 0:
				return 1
			else:
				return 0
		else:
			max = 0
			for r in self.sts:
				x = self.tr_matrix[r][s] * self.v(r,i-1)
				if x > max:
					max = x
			return max * self.em_matrix[s][self.sent[i]]

	def v2(self, s, i):
		if i == 0:
			return 1
		else:
			n = self.sts
			max = 0
			for r in n:
				x = self.tr_matrix[r][s] * self.v2(r,i-1)
				if x > max:
					max = x
#			print s, self.sent[i-1]
			return max * self.em_matrix[s][self.sent[i]]

	def final(self):
		ans = ""
		for i in [1,2,3,4,5,6]:
			max = 0
			for s in self.sts:
				x = self.v2(s, i)
				if x > max:
					max = x
					ans = s
			print (i,ans)



hmm = MyHMM("6d gokulam road shenoy nagar chennai 600033")
hmm.final()