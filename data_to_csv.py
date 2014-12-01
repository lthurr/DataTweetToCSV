import re
import sys
from glob import glob

def extract_hashtags(st):
    return re.findall(r"#(\w+)", st)

def measure_pref(hashtag, list_hashtags):
	return list_hashtags.count(hashtag)/float(len(list_hashtags))

def main(argv):
	if len(argv) != 1:
		print "You need to pass a /directory\nExiting..."
		sys.exit()
	directory_path = argv[0]
	f_csv = open("data.csv", 'w')
	for filename in glob(directory_path + "/*/*"):
		f = open(filename, 'rb')
		user_name = f.readline()[1:-2]
		content_data = f.read()
		list_hashtags = extract_hashtags(content_data)
		for hashtag in list(set(list_hashtags)):
			pref = measure_pref(hashtag, list_hashtags)
			f_csv.write("%s,%s,%s\n" % (user_name, hashtag, pref))
		f.close()
	f_csv.close()


if __name__ == '__main__':
	main(sys.argv[1:])