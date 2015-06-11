import os
no_of_days = [31,28,31,30,31]
for x in range(1,6):
	for y in range(1,no_of_days[x-1]+1):
		i = 'python the_hindu.py {0} {1}'.format(x,y)
		os.system( i )

print "DONE"