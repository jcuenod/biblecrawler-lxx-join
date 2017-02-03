import cProfile
import csv
import re
from betacode import decode

ketiv = 0
qere = 0
rafe = 0
line = ""
tf_content = []
print("Reading tfdata ...")
# RecordId, HebrewText, HebLemma, SDBH, LexDomain, GLemma
verses = {}
recordid_map = {}
with open('tfdata.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		tf_content.append(row)
		v = re.match(r'(^.*),', row["RecordId"])
		if v:
			vid = v.group(1)
			if vid not in verses:
				verses[vid] = []
			verses[vid].append(row["RecordId"])
			recordid_map[row["RecordId"]] = len(tf_content) - 1
		# to_decode = re.sub(r'[\d\/]', '', row['HebrewText'])
		# to_decode = re.sub(r'~', ' ', to_decode)
		# if re.search(r'\*\*', to_decode):
		# 	qere += 1
		# 	# continue
		# if re.search(r'\*', to_decode):
		# 	ketiv += 1
		# 	to_decode = re.sub(r'\*', '', to_decode)
		# if re.search(r',', to_decode):
		# 	to_decode = re.sub(r'\,', '', to_decode)
		# 	rafe += 1
		# decoded = decode(to_decode) if to_decode != "_" else "_"
		# tf_content.append({
		# 	"id": row["RecordId"],
		# 	"betacode": row["HebrewText"],
		# 	"hebrew": decoded,
		# 	"lemma": row["HebLemma"],
		# 	"sdbh": row["SDBH"],
		# 	"domain": row["LexDomain"],
		# 	"glemma": row["GLemma"],
		# })
		if len(tf_content) % 50000 == 0:
			print(" |", len(tf_content), "lines processed")
print(" ^", len(tf_content), "lines processed")
print("Completed tfdata prep\n")


# HebLemma, MTVerseID, MTSTartSequence, MTEndSequence, GrkLemma, LXXVerseID, LXXPhrase
og_content = []
emptylemma = 0
print("Reading ogdata ...")
with open('parallelsearch.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		og_content.append(row)
		if row["GrkLemma"] == "":
			emptylemma += 1
		if len(og_content) % 50000 == 0:
			print(" |", len(og_content), "lines processed")
print(" ^", len(og_content), "lines processed")
print("Completed ogdata prep ({} empty lemmas)\n".format(emptylemma))

def id_in_range(rid, lower, upper):
	m = re.search("(^\w+ \d+:\d+,)(\d+.\d+)", rid)
	pos_float = float(m.group(2))
	return pos_float >= lower and pos_float <= upper

def partial_match_id_range(abbreviated_map_ids, id_partial_start, id_partial_end):
	lower = float(id_partial_start)
	upper = float(id_partial_end)
	return list(filter(lambda x: id_in_range(x,lower,upper), abbreviated_map_ids))


def process_everything():
	# inject greek stuff...
	failures = 0
	oldid = ""
	ids_done = 0
	print("Processing parallels ({})".format(len(og_content)))
	for i, og in enumerate(og_content):
		if i % 50000 == 0:
			print(" |", i, "matched rows")

		if og["MTSTartSequence"] == "" or og["MTSTartSequence"] == "MTSTartSequence":
			continue

		if og["MTSTartSequence"] == og["MTEndSequence"]:
			rid = og["MTVerseID"] + "," + og["MTSTartSequence"]
			tf_content[ recordid_map[rid] ]["GLemma"] = og["GrkLemma"]
		else:
			success = False
			rr = partial_match_id_range(verses[og["MTVerseID"]], og["MTSTartSequence"], og["MTEndSequence"])
			if rr is None:
				print("None?", og["MTVerseID"], og["MTSTartSequence"], og["MTEndSequence"])

			for j, rid in enumerate(rr):
				tfid = recordid_map[rid]
				if tf_content[tfid]["HebLemma"] == og["HebLemma"]:
					success = True
					tf_content[tfid]["GLemma"] = og["GrkLemma"]

			if not success:
				failures += 1

	print(" ^ DONE:", failures, "words without greek lemmas\n")

# cProfile.run('process_everything()')
process_everything()

print ("Writing csv file...")
filename = "processed_tfdata.csv"
with open(filename, mode='wt', encoding='utf-8') as out:
	csvout = csv.DictWriter(out, ["RecordId", "HebrewText", "HebLemma", "SDBH", "LexDomain", "GLemma"])
	csvout.writeheader()
	csvout.writerows(tf_content)
print ("done")
