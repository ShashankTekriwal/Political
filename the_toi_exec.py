import os

print 'Starting toi data scrap'
for x in range(3,6):
	run = 'python the_toi.py {0}'.format(x)
	os.system(run)
print "---------DONE-------"