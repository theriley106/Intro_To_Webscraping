import re

def extract_number(string):
	return [round(float(x), 2) for x in re.findall("([0-9]+\.[0-9][0-9]?)?", string) if len(x) > 2]