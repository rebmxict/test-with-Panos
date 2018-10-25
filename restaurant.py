import csv, datetime

VIP = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
default_info = {}
for vip in VIP:
	default_info[vip] = None

def get_vip_index(find_vip):
	for i, vip in enumerate(VIP):
		if vip == find_vip:
			return i
	return None

def get_datetime(timestr):
	fss = '%I:%M%p'
	fs = '%I%p'
	if ':' in timestr:
		return datetime.datetime.strptime(timestr, fss).time()
	else:
		return datetime.datetime.strptime(timestr, fs).time()

def find_open_restaurants(filename, day, time):
	restaurants = {}
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			restaurants[row[0]] = row[1]
	
	parsed_restaurants = {}
	restaurant_names = list(restaurants.keys())
	for restaurant_name in restaurant_names:
		restaurant_info = []
		restaurant_info_str = restaurants[restaurant_name]
		index = 0
		start_vip = None
		end_vip = None
		for c in restaurant_info_str:
			if index < len(restaurant_info_str) - 2:
				if index == 0:
					vip_index = get_vip_index(c + restaurant_info_str[index + 1] + restaurant_info_str[index + 2])
					if vip_index != None:
						start_vip = vip_index
						if restaurant_info_str[index + 3] != '-':
							end_vip = vip_index
					else:
						return 'Wrong VIP input'
				else:
					vip_index = get_vip_index(c + restaurant_info_str[index + 1] + restaurant_info_str[index + 2])
					if vip_index != None:
						if restaurant_info_str[index - 1] == '-':
							end_vip = vip_index
						elif restaurant_info_str[index - 1] == ' ':
							start_vip = vip_index
							if restaurant_info_str[index + 3] != '-':
								end_vip = vip_index
				if start_vip != None and end_vip != None:
					restaurant_info.append([start_vip, end_vip])
					start_vip = None
					end_vip = None
				index += 1
		parsed_restaurants[restaurant_name] = restaurant_info

	for restaurant_name in restaurant_names:
		parsed_restaurant = parsed_restaurants[restaurant_name]
		restaurant_info_str = restaurants[restaurant_name]
		restaurant_info_datetimes = restaurant_info_str.split('/')
		for restaurant_info_datetime in restaurant_info_datetimes:
			index = 0
			for parsed_restaurant_days in parsed_restaurant:
				if VIP[parsed_restaurant_days[1]] in restaurant_info_datetime:
					restaurant_info_times = restaurant_info_datetime.split(VIP[parsed_restaurant_days[1]])
					if ',' not in restaurant_info_times[1]:
						restaurant_info_times = restaurant_info_times[1].split('-')
						start_time = get_datetime(restaurant_info_times[0].replace(' ', ''))
						end_time = get_datetime(restaurant_info_times[1].replace(' ', ''))
						parsed_restaurants[restaurant_name][index].append([start_time, end_time])
				index += 1

	for restaurant_name in restaurant_names:
		parsed_restaurant = parsed_restaurants[restaurant_name]
		index = 0
		for day_info in parsed_restaurant:
			if len(day_info) < 3:
				for i in range(index, len(parsed_restaurant)):
					if(len(parsed_restaurant[i])) > 2:
						parsed_restaurants[restaurant_name][index].append(parsed_restaurant[i][2])
						break
			index += 1 

	find_day_index = get_vip_index(day)
	find_time = get_datetime(time)
	open_restaurants = []
	for restaurant_name in restaurant_names:
		parsed_restaurant = parsed_restaurants[restaurant_name]
		for day_info in parsed_restaurant:
			if find_day_index >= day_info[0] and find_day_index <= day_info[1]:
				if find_time >= day_info[2][0] and find_time <= day_info[2][1]:
					open_restaurants.append(restaurant_name)

	print('\n'.join(open_restaurants))

find_open_restaurants('restaurant_hours.csv', "Sat", "10:21pm")