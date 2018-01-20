import json 
import pdb
import operator


def histogram(list_concepts, confidence=None): 
	freq_count = {}
	for t in list_concepts:
		name = t[0]
		# If there is a confidence interval use it
		# count them all 
		if confidence: 
			if t[1] >= confidence:
				if name in freq_count.keys(): 
					freq_count[name] = freq_count[name] + 1
				else: 
					freq_count[name] = 1
		else: 
			if name in freq_count.keys(): 
				freq_count[name] = freq_count[name] + 1
			else: 
				freq_count[name] = 1
	
	return freq_count



if __name__ == '__main__': 

	print("Loading data")
	try: 
	    clarify_log = json.load(open('../data/clarify_log_lecon.txt'))        
	    print("Tracking files Loaded")
	except(ValueError, IOError) as e:
	    print("Exception on load: {}".format(e))

	list_concepts = []
	for i in range(len(clarify_log['data'])):
		for j in range(len(clarify_log['data'][i]['outputs'][0]['data']['concepts'])):
			concept = clarify_log['data'][i]['outputs'][0]['data']['concepts'][j]
			concept_t = (concept['name'], concept['value'])
			print(concept_t)
			list_concepts.append(concept_t)

thefile = open('../data/list_concepts.txt', 'w')
for item in list_concepts:
  thefile.write("{}\n".format(item))

# histogram count
hist = histogram(list_concepts)
hist_sorted = sorted(hist.items(), key=operator.itemgetter(1))[::-1]

thefile = open('../data/hist_sorted.txt', 'w')
for item in hist_sorted:
  thefile.write("{}\n".format(item))


print('\n \n')
# histogram count with confidence threshold 
hist_c = histogram(list_concepts, 0.95)
hist_sorted_c = sorted(hist_c.items(), key=operator.itemgetter(1))[::-1] 
# pdb.set_trace()
