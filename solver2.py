from parse import read_input_file, write_output_file
import os
import Task
import heapq as hq

def find_best_schedule(tasks, schedule, start_time, total_time=0):
        if not tasks:
            return schedule, calc_benefit(schedule, start_time, start_time + 288), start_time + total_time

        task = tasks[0]

        return max(find_best_schedule(tasks[1:], schedule + [task], start_time, total_time + task.get_duration()), 
                   find_best_schedule(tasks[1:], schedule, start_time, total_time), 
                   key = lambda k: k[1])

def find_schedule(tasks, schedule=[]):
    if not tasks:
        return schedule, calc_benefit(schedule, 0, 1440)

    return max(find_schedule(tasks[1:], schedule + [tasks[0]]), 
               find_schedule(tasks[1:], schedule), 
               key = lambda k: k[1])

def calc_benefit(tasks, start_time, max_time=1440):
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

<<<<<<< HEAD
def checkDeadline(currTime, task2):
    if(task2.get_deadline()-task2.get_duration() < currTime):
        return False
    return True

def getInitialGreedySoln(tasks):
    currTime = 0;
    schedule = []
    notinschedule = []
    while(len(tasks)>0):
        if(checkDeadline(currTime, tasks[0])):
            schedule.append(tasks[0])
            currTime+=tasks[0].get_duration()
        else:
            notinschedule.append(tasks[0])
        del tasks[0]
    return schedule, notinschedule

def calcProfit(schedule):
    sum = 0
    for task in schedule: sum+=task.get_max_benefit()
    return sum

def calc_task_heuristic(task):
    return (task.get_deadline() - task.get_duration()) - 0.2 * task.get_max_benefit()


def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """

    tasks = sorted(tasks, key=lambda x: calc_task_heuristic(x))
    tasks = zero_calibrate(tasks)

    tasks = remove_weak(tasks)

    schedule_optimal, benefit_opt = find_schedule(tasks)
    print("OPTIMAL_SCHEDULE")
    printSchedule(schedule_optimal)
    print(benefit_opt)

    schedule, notinschedule = getInitialGreedySoln(tasks)

    print("SCHEDULE_GREEDY")
    printSchedule(schedule)
    print(calcProfit(schedule))

    heap = []
    for task in notinschedule: hq.heappush(heap, task)
    #print("HEAP")
    #printSchedule(heap)

    maxIter = 1000
    for i in range(0,maxIter):
        if(len(heap)==0):
            break;
        schedule_opt, popped = replace(schedule, hq.heappop(heap))
        if(calcProfit(schedule_opt) > calcProfit(schedule)):
            schedule = schedule_opt
            for t in popped:
                hq.heappush(heap, t)
        else:
            hq.heappop(heap)

    print("FINAL SCHEDULE")
    printSchedule(schedule)
    print(calcProfit(schedule))
    print(checkSchedule(schedule))

def printSchedule(schedule):
    for task in schedule: print(task)

def replace(schedule, task):
    currentTime = 0
    before = 0
    latest_Time = task.get_deadline()-task.get_duration()
    for t in schedule:
        if(currentTime + t.get_duration()>latest_Time):
            projectedTime = currentTime + task.get_duration()
            break;
        currentTime += t.get_duration()
        before += 1

    scheduleF = schedule[:before]
    scheduleF.append(task)
    poppedItems = []
    for i in range(before, len(schedule)):
        if(schedule[i].get_deadline() - schedule[i].get_duration() > projectedTime):
            scheduleF.append(schedule[i])
        else:
            poppedItems.append(schedule[i])

    return scheduleF, poppedItems


    #tasks = remove_weak(tasks)

    big_schedule = []
    big_benefit = 0
    leftovers = []
    start_time = 0

    for i in range(5):

        bucket = [tasks.pop(0) for i in range(17)]
        buffer = [tasks.pop(0) for i in range(3)]

        schedule, benefit, start_time = find_best_schedule(bucket, [], start_time)
        big_schedule += schedule
        big_benefit += benefit
        duration = sum([task.get_duration() for task in schedule])

        leftovers.append(Task.Task(100 + i, start_time, int(duration), float(benefit)))
        leftovers += buffer

        for task in schedule:
            print(task)
        print("dur:", duration)
        print("ben:", benefit)
        print()


    final_schedule, benefit = find_schedule(leftovers) 
    for task in final_schedule:
        print(task)
    print(benefit)
    print(sum([task.get_duration() for task in final_schedule]))


def checkSchedule(schedule):
    currTime = 0
    while(len(schedule)>1):
        currTime += schedule[0].get_duration()
        if(schedule[1].get_deadline()-schedule[1].get_duration()<currTime):
            return False
        del schedule[0]
    return True

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