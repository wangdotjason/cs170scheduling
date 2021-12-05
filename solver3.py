from parse import read_input_file, write_output_file
import os
import Task
import random

def find_best_schedule(tasks, schedule, max_time):
        if not tasks:
            return schedule, calc_benefit(schedule, max_time - 240, max_time), tasks

        task = tasks[0]

        if task.get_deadline() >= max_time: 
            return schedule, calc_benefit(schedule, max_time - 240, max_time), tasks

        return max(find_best_schedule(tasks[1:], schedule + [task], max_time), 
                   find_best_schedule(tasks[1:], schedule, max_time), 
                   key = lambda k: k[1])

def find_schedule(tasks, schedule=[]):
    if not tasks:
        return schedule, calc_benefit(schedule, 0, 1440)

    return max(find_schedule(tasks[1:], schedule + [tasks[0]]), 
               find_schedule(tasks[1:], schedule), 
               key = lambda k: k[1])


def calc_benefit(tasks, start_time, max_time):
    benefit = 0
    time = start_time
    for task in tasks: 
        if time + task.get_duration() < max_time:
            latest_start = task.get_deadline() - task.get_duration()
            mins_late = max(0, time - latest_start)
            benefit += task.get_late_benefit(mins_late)
            time = time + task.get_duration()
        else:
            return 0

    return benefit

def zero_calibrate(tasks):
    for task in tasks:
        latest_start = task.get_deadline() - task.get_duration()

        if latest_start >= 0:
            break
        else: 
            task.perfect_benefit = task.get_late_benefit(-latest_start)
            task.deadline = task.get_duration()
    return tasks

def remove_weak(tasks):
    benefit = 0
    for task in tasks:
        benefit += task.get_max_benefit()

    average_benefit = benefit/len(tasks)

    return [task for task in tasks if task.get_max_benefit() > average_benefit * .1]

def checkDeadline(currTime, task2):
    if(task2.get_deadline()-task2.get_duration() < currTime):
        return False
    return True

def greedy(tasks, a, b, c):
    tasks = sorted(tasks, key=lambda x: a*(x.get_deadline() - x.get_duration()) - c*x.get_max_benefit() - b*x.get_max_benefit()/x.get_duration())
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


def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    tasks = zero_calibrate(tasks)
    tasks = remove_weak(tasks)
    max = 0
    iter = 10000
    final_sched = []
    a_f = 0
    b_f = 0
    c_f = 0
    for i in range(0,iter):
        a = 1*random.random()
        b = 20*random.random()
        c = 1*random.random()
        schedule, sum = greedy(tasks, a ,b, c)
        if(sum>max):
            max = sum
            final_sched = schedule
            a_f = a
            b_f = b
            c_f = c
    checkSchedule(final_sched)
    print(a_f)
    print(b_f)
    print(c_f)

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

def main():
    for input_path in os.listdir('inputs/'):
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/' + input_path)
        output = solve(tasks)
        #write_output_file(output_path, output)

if __name__ == "__main__":
    main()




# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)