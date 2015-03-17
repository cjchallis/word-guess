from random import randint
from os import listdir
import os.path

class MasterList (object):
	def __init__(self, lp, cp):
		self.length = 0
		self.word_lists = []
		self.active = []
		self.list_path = lp
		self.count_path = cp
		self.create_lists(lp, cp)
		
	def create_lists(self, lp, cp):
		names = listdir(lp)
		for n in names:
			self.word_lists.append(WordList(lp +  n, cp + n))
					
	def update(self):
		self.length = 0
		self.active = []
		for l in self.word_lists:
			if l.selected:
				self.length += l.len()
				self.active.append(l)
		
	def get_word(self):
		self.update()
		r = randint(0, self.length)
		i = 0
		total = self.active[0].len()
		while r > total:
			i += 1
			total += self.active[i].len()
		if i >= len(self.active):
			f = open('length_bug.txt', 'a')
			f.write(' '.join(map(str, [i, len(self.active), r, total, self.length])))
			f.write('\n')
			f.close()
			i = len(self.active)-1
		return self.active[i].get_word()

class WordList (object):
	def __init__(self, lf, nf):
		self.selected = False
		self.list_file = lf
		lf = open(lf, 'r')
		self.topic = lf.readline()
		self.list = lf.readlines()
		lf.close()
		
		self.idx_file = nf
		if os.path.isfile(nf):
			nf = open(nf, 'r')
			self.idx = int(nf.readline())
		else:
			nf = open(nf, 'w')
			nf.write(str(0))
			self.idx = 0
		nf.close()
	
	def len(self):
		return len(self.list)
	
	def get_word(self):
		word = self.list[self.idx]
		self.idx = (self.idx + 1) % len(self.list)
		f = open(self.idx_file, 'w')
		f.write(str(self.idx))
		f.close()
		
		return word
		
		
lis = MasterList('./Lists/', './Counts/')
