from parse import read_input_file, write_output_file
import os
import random

def checkDeadline(currTime, task2):
    if(task2.get_deadline()-task2.get_duration() < currTime):
        return False
    return True

def greedy(tasks, a, b):

    def heuristic(task):
        latest_start = task.get_deadline() - task.get_duration()
        benefit_rate = task.get_max_benefit()/task.get_duration()
        relben = task.get_late_benefit(-latest_start)/task.get_duration()

        return a *latest_start  - b * relben

    tasks = sorted(tasks, key=heuristic)
    currTime = 0
    schedule = []
    sum = 0
    while (len(tasks) > 0):
        if (checkDeadline(currTime, tasks[0])):
            schedule.append(tasks[0])
            sum+=tasks[0].get_max_benefit()
            currTime += tasks[0].get_duration()
        del tasks[0]
    return schedule, sum

def zero_calibrate(tasks):
    for task in tasks:
        latest_start = task.get_deadline() - task.get_duration()

        if latest_start >= 0:
            break
        else:
            task.perfect_benefit = task.get_late_benefit(-latest_start)
            task.deadline = task.get_duration()
    return tasks

def calc_benefit(tasks, start_time=0, max_time=1440):
    benefit = 0
    for task in tasks: 
        if start_time + task.get_duration() < max_time:
            latest_start = task.get_deadline() - task.get_duration()
            mins_late = max(0, start_time - latest_start)
            benefit += task.get_late_benefit(mins_late)
            start_time = start_time + task.get_duration()
        else:
            return 0

    return benefit

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing
    """

    tasks = zero_calibrate(tasks)
    max = 0
    iter = 10000
    final_sched = []
    for i in range(0,iter):
        a = 1*random.random()
        b = 20*random.random()
        schedule, sum = greedy(tasks, a ,b)
        if(sum>max):
            max = sum
            final_sched = schedule

    print(calc_benefit(final_sched))
    return [task.get_task_id() for task in final_sched]

def calcProfit(schedule):
    sum = 0
    for task in schedule:
        print(task)
        sum+=task.get_max_benefit()
    return sum

def checkSchedule(schedule):
    print(calcProfit(schedule))
    currTime = 0
    while(len(schedule)>1):
        currTime += schedule[0].get_duration()
        if(schedule[1].get_deadline()-schedule[1].get_duration()<currTime):
            print("False")
            break
        del schedule[0]
    print("True")


# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for size in os.listdir('inputs/'):
#         if size not in ['small', 'medium', 'large']:
#             continue
#         for input_file in os.listdir('inputs/{}/'.format(size)):
#             if size not in input_file:
#                 continue
#             input_path = 'inputs/{}/{}'.format(size, input_file)
#             output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
#             print(input_path, output_path)
#             tasks = read_input_file(input_path)
#             output = solve(tasks)
#             write_output_file(output_path, output)

def main():
    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if size not in input_file:
                continue
            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            print(input_path, output_path)
            tasks = read_input_file(input_path)
            output = solve(tasks)
            write_output_file(output_path, output)

if __name__ == "__main__":
    main()