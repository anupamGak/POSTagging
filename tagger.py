import re
from collections import Counter

class HMM():
	def __init__(self):
		reTag = re.compile(r" (.+)$", re.MULTILINE)
		with open('postrain.txt', 'r') as trfile:
			self.data = trfile.read()
		self.tagorder = re.findall(reTag, self.data)
		self.tagcount = dict(Counter(self.tagorder))
		self.tags = self.tagcount.keys()
		self.ntag = 44

	def q(self,v,w,u):
		tag = self.tagorder
		c1N = 0
		c1D = 1
		c2N = 0
		c2D = 0
		c3N = 0
		c3D = len(tag)

		tag.append('.')
		tag.append('.')
		for i in range(c3D):
			if tag[i]==w and tag[i+1]==u and tag[i+2]==v:
				c1N += 1
			if tag[i]==w and tag[i+1]==u:
				c1D += 1
			if tag[i]==u and tag[i+1]==v:
				c2N += 1
			if tag[i]==u:
				c2D += 1
		c3N = self.tagcount[v]

		return 0.4*c1N/float(c1D) + 0.3*c2N/float(c2D) + 0.3*c3N/float(c3D)

	def e(self,x,v):
		N = self.data.count(x + " " + v)
		D = self.tagcount[v]

		return N/float(D)








class POStagger:
	def __init__(self, sent, hmm):
		self.x = sent.split()
		self.n = len(self.x)
		self.hmm = hmm

	def pi(self, k, u, v,ini):
		if k == 0:
			return 1
		else:
			print "k", k
			maxi = 0
			for w in self.hmm.tags:
				r = self.pi(k-1, w, u, 0) * hmm.q(v,w,u) * hmm.e(self.x[k-1],v)
				#print "x", self.x[k-1]
				if r > maxi:
					maxi = r
			return maxi


	# def viterbi():
	# 	n = self.n
	# 	tags = self.hmm.tags

	# 	for k in range(n):
	# 		for v in tags:
	# 			for u in tags:

hmm = HMM()

t = POStagger("to fail another drive", hmm)
#print hmm.tags
print t.pi(3, 'VB', 'DT', 1)






	# def pi(k, u, v):
	# 	if k == 0:
	# 		return 1
	# 	else:
	# 		for 