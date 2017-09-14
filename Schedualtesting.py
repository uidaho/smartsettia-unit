import schedule
import time
import sensors

count = 2

def job():
    print("I'm working...")

def job2(mystr):
    print("arg: %r") % mystr

def job3(mycount):
    print("count: %r") % mycount
    global count
    count = count + 1
    #return count += 1

def job4():
    global count
    print("count: %r") % count
    count = count + 1
    #return count += 1

#schedule.every(5).seconds.do(job)
schedule.every(10).seconds.do(job2,"hello")
#schedule.every(1).seconds.do(job3,*count) # not working
#schedule.every(1).seconds.do(job4)
#schedule.every(1).seconds.do(sensors.getTemp)

while True:
    schedule.run_pending()
    time.sleep(1)
    print "main count: %r" % count
    #job3(count)
    #print "Temp: ", sensors.getTemp()
