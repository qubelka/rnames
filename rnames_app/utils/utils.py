import sys
import datetime

#def YourClassOrFunction(request):
time=datetime.datetime.now()

output="Hi %s current time is: %s" % (sys.argv[1],time)

print(output)
