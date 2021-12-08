import tasks
from time import sleep

print("add 3+5")
ret = tasks.score_question.delay(3,5)
print("Task ID:")
print(ret)
sleep(10) #give SQS and your worker time enough to execute, so that you can check status on next line
print(ret.status) #this should say SUCCESS