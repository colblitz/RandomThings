for word in open('/usr/share/dict/words'):
	word = word.strip()
	if len(filter(lambda p: p > 0.5, map(lambda l: word.count(l) / float(len(word)), "".join(set(word))))) > 0 and len(word) > 5:
		print word