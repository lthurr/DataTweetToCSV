import re
import sys
from glob import glob
from collections import defaultdict

def extract_hashtags(st):
	hashtag_list = re.findall(r"#(\w+)", st)
	return [hashtag.lower() for hashtag in hashtag_list]

def measure_pref(hashtag, list_hashtags):
	return list_hashtags.count(hashtag)/float(len(list_hashtags))

def main(argv):
	if len(argv) != 1:
		print "You need to pass a /directory\nExiting..."
		sys.exit()
	directory_path = argv[0]
	f_csv = open("data.csv", 'w')
	d_ids = open("ids.txt", "w")
	hashtags_ids = open("hashtags_ids.txt", 'w')
	hashtags_per_user_f = open("hashtags_per_user.txt", 'w')
	user_id = 1
	hashtag_id = 1
	users_ids_dict = defaultdict(int)
	hashtags_ids_dict = defaultdict(int)
	hashtags_per_user_dict = defaultdict(list)
	for filename in glob(directory_path + "/*/*"):
		f = open(filename, 'rb')
		user_name = f.readline()[1:-2]
		users_ids_dict[user_name] = user_id
		content_data = f.read()
		list_hashtags = extract_hashtags(content_data)
		hashtags_per_user_dict[user_name] = list(set(list_hashtags))
		for hashtag in list(set(list_hashtags)):
			if hashtags_ids_dict[hashtag] == 0:
				hashtags_ids_dict[hashtag] = hashtag_id
				hashtag_id += 1
		f.close()
		user_id += 1
	for k, d in users_ids_dict.iteritems():
		d_ids.write("%s\t%s\n" % (k, d))
	d_ids.close()
	for k, d in hashtags_ids_dict.iteritems():
		hashtags_ids.write("%s\t%s\n" % (d, k))
	hashtags_ids.close()
	for k, d in hashtags_per_user_dict.iteritems():
		hashtags_per_user_f.write("%s\t%s\n" % (k, d))
	hashtags_per_user_f.close()
	for filename in glob(directory_path + "/*/*"):
		f = open(filename, 'rb')
		user_name = f.readline()[1:-2]
		content_data = f.read()
		list_hashtags = extract_hashtags(content_data)
		for hashtag in list(set(list_hashtags)):
			pref = measure_pref(hashtag, list_hashtags)
			if ("%.2f" % pref) == "0.00":
				f_csv.write("%s,%s,0.1\n" % (users_ids_dict[user_name], hashtags_ids_dict[hashtag]))
			else:
				f_csv.write("%s,%s,%.2f\n" % (users_ids_dict[user_name], hashtags_ids_dict[hashtag], pref))
		f.close()

	f_csv.close()


if __name__ == '__main__':
	main(sys.argv[1:])
