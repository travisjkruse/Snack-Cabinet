import os

while 1:
    todo = raw_input('Enter ID number? [y/n] ')
    print todo
    if str(todo) == 'y':
        idnum = raw_input('ID Number? ')
	try:
		val = int(idnum)
	        if str(idnum) in open('/home/pi/SnackStats/Permissions.txt').read():
			print('ID already entered.')
	        else:
			with open('/home/pi/SnackStats/Permissions.txt', 'a') as f:
	                	f.write('\n'+str(idnum))
        	    
	except ValueError:
            print('Only integers.')
    if str(todo) == 'n':
        os.system('sudo python /home/pi/SimpleSerial.py')
        
