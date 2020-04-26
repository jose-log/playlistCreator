#!/usr/bin/env python3

import re	# regular expressions

re_sec = r'^P.*[TM](\d+)S$'
re_min = r'^P.*[TH](\d+)M.*S$'
re_h = r'^P.*[T](\d+)H.*M.*S$'
re_day = r'^P(\d+)DT.*H.*M.*S$'

def get_time(time):

	seconds = re.search(re_sec, time)
	minutes = re.search(re_min, time)
	hours = re.search(re_h, time)
	days = re.search(re_day, time)

	s = 0
	if seconds is not None: s = int(seconds[1])
	if minutes is not None: s += int(minutes[1]) * 60
	if hours is not None: s += int(hours[1]) * 3600
	if days is not None: s += int(days[1]) * 86400

	#if seconds is not None: print('seconds: ' + seconds[1])
	#if minutes is not None: print('minutes: ' + minutes[1])
	#if hours is not None: print('hours: ' + hours[1])
	#if days is not None: print('days: ' + days[1])

	return s