import csv
from multiprocessing.connection import answer_challenge
import CustomerClass


## take in time string formatted as 00:00:00 and convert it to total seconds
def toSeconds(time):
    time = str(time)
    numbers = time.split(":")
    hours = int(numbers[0])
    minutes = int(numbers[1])
    seconds = int(numbers[2])
    return hours*3600 + minutes*60 + seconds

incoming_calls = []
answer_calls = []
abandonded_calls = []
answer_speed = []

#  CSV FORMAT
#  Index,Incoming Calls,Answered Calls,Answer Rate,Abandoned Calls,Answer Speed (AVG),Talk Duration (AVG),Waiting Time (AVG),Service Level (20 Seconds)
#  Open sample data file
with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)

    for row in reader:
        incoming_calls.append(int(row[1]))
        answer_calls.append(int(row[2]))
        abandonded_calls.append(int(row[4]))
        answer_speed.append(toSeconds(row[5]))
avg = sum(incoming_calls) / len(incoming_calls)
#print(incoming_calls)
print(avg)
#print(answer_calls)
#print(abandonded_calls)
#print(answer_speed)