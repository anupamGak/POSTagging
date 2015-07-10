import json

addrdump = []

with open('Zipprs.csv', 'r') as inp:
	count = 0
	for line in inp:
		count += 1
		if count == 51:
			break
		address = {}
		add = line.split("|")
		address['aptnum'] = add[3]
		address['buildingname'] = add[4]
		address['neighborhood'] = add[5]
		address['landmark'] = add[6]
		address['locality'] = add[7]
		address['sublocality'] = add[8]
		address['state_country'] = add[9]
		address['postal_code'] = add[10]

		addrdump.append(address)

with open('zippr_addr.json', 'w') as opt:
	json.dump(addrdump, opt, indent=1)