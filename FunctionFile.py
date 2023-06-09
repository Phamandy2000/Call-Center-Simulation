
import csv
from multiprocessing.connection import answer_challenge
import datetime
import random
import numpy as np
from CustomerClass import Customer
from ServerClass import Server

servedCustomers = []
abandondedCustomers = []
baulkedCustomers = []
reneggedCustomers = []
completedCustomers = []
queue = []
serviceTimes = []


## take in time string formatted as 00:00:00 and convert it to total seconds
def toSeconds(time):
    time = str(time)
    numbers = time.split(":")
    hours = int(numbers[0])
    minutes = int(numbers[1])
    seconds = int(numbers[2])
    return hours*3600 + minutes*60 + seconds

## call tick on all of the customers in the queue
def customersTick(customerList):
    for customer in customerList:
        customer.tick()

## overarching tick function for the simulation
def tick(serverList, queue, max_queue_length, currentTick):
    
    reneggedCustomersToRemove = []
#    remove reneging customers
    for customer in queue:
        if customer.willRenege():
            customer.setRenegTime()
            customer.setServiceTime(0)
            reneggedCustomersToRemove.append(customer)
            reneggedCustomers.append(customer)
            completedCustomers.append(customer)
    for customer in reneggedCustomersToRemove:
        queue.remove(customer)

    # for each server 
    for server in serverList:
        # if they are severing a customer 
        if(server.serving):
                # check if they should have finished with the customer 
                if(server.time >= server.endTime):
                    # They should no longer be serving that customer 
                    server.serving = False
                    servedCustomers.append(server.cust)
                    completedCustomers.append(server.cust)
                    server.tick()
                else:
                    # increment the time the server is with the customer 
                    server.tick()
        # if they are not serving a customer 
        else:
                # if there still customers to help
                if(len(queue) != 0):
                    # start serving the next customer 
                    currentCus = queue.pop(0)
                    currentCus.setServiceStartTime(currentTick)
                    currentCus.setServiceEndTime(currentTick + currentCus.getServiceTime())
                    currentCus.removeMaxWaitingTime()
                    server.serving = True
                    server.newCust(currentCus)
    # tick the customers                
    customersTick(queue)
    # remove baulking customers
    if len(queue) > max_queue_length:
        baulked_cust = queue.pop()
        baulked_cust.setBaulkTime()
        baulked_cust.setServiceTime(0)
        baulkedCustomers.append(baulked_cust)
        completedCustomers.append(baulked_cust)

    for customer in servedCustomers:
        serviceTimes.append(customer.serviceTime)

## simulation driver 
def simulate(serverList, customerList, ticks, max_queue_length):
    resetSimulation()
    # make sure there are customers 
    queue = []
    if len(customerList) == 0:
        print("Error: No Customers Specified")
        quit()
    # make sure there are servers 
    if len(serverList) == 0:
        print("There are no servers")
        quit()

    # do as many ticks are requested
    for i in range(ticks):
        if len(customerList) > 0:
            if customerList[0].getEntryTime() <= i:
                queue.append(customerList.pop(0))
        tick(serverList, queue, max_queue_length, i)
        

    serviceTimeCounts = dict()
    for customer in servedCustomers:
        serviceTime = customer.serviceTime
        serviceTimeCounts[serviceTime] = serviceTimeCounts.get(serviceTime, 0) + 1


    for key in serviceTimeCounts.keys():
        serviceTimeCounts[key] = round(serviceTimeCounts.get(key) / len(servedCustomers), 3)
    return serviceTimeCounts

##
def callsPerDay(hours):
    return int(np.ceil((np.random.poisson(avgCalls) / 8 ) * hours))

def getCustomerCallTimes(hours):
    calls = callsPerDay(hours)
    seconds = hours * 3600
    callTimes = []
    for i in range (0, calls):
        callTimes.append(random.randint(0,seconds))
    callTimes.sort()
    return callTimes

def getCallLengths(callTimes):
    callLengths = []
    totalCallLength = 0
    for i in callTimes:
        length = np.random.poisson(avgLength)
        callLengths.append(length)
        totalCallLength = totalCallLength + length
    return callLengths  

def getBaulkedCustomers():
    return baulkedCustomers

def getReneggedCustomers():
    return reneggedCustomers

def getServedCustomers():
    return servedCustomers

def getCompletedCustomers():
    return completedCustomers

def resetSimulation():
    servedCustomers.clear()
    reneggedCustomers.clear()
    baulkedCustomers.clear()
    completedCustomers.clear()

index = []
incoming_calls = []
answer_calls = []
answer_rate = []
abandonded_calls = []
answer_speed = []
talk_duration = []
waiting_time =[]
service_level = []

#  CSV FORMAT
#  Index,Incoming Calls,Answered Calls,Answer Rate,Abandoned Calls,Answer Speed (AVG),Talk Duration (AVG),Waiting Time (AVG),Service Level (20 Seconds)
#  Open sample data file
with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)

    for row in reader:
        index.append(int(row[0]))
        incoming_calls.append(int(row[1]))
        answer_calls.append(int(row[2]))
        answer_rate.append(str(row[3]))
        abandonded_calls.append(int(row[4]))
        answer_speed.append(toSeconds(row[5]))
        talk_duration.append(toSeconds(row[6]))
        waiting_time.append(toSeconds(row[7]))
        service_level.append(str(row[8]))

avgCalls = np.average(incoming_calls)
avgLength=np.average(talk_duration)
avg = sum(abandonded_calls) / len(abandonded_calls)
avgWait = sum(waiting_time) / len(waiting_time)
numofA = len(abandonded_calls)
answerSpeedSecondList = list()
rand = random.randint(0, max(answer_speed))
#print(rand)

def getAvgWait():
    return avgWait
