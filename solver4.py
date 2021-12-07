from parse import read_input_file, write_output_file
import os
import random
import Task
import copy

def zero_calibrate(tasks):
    for task in tasks:
        latest_start = task.get_deadline() - task.get_duration()
        if latest_start < 0:
            task.perfect_benefit = task.get_late_benefit(-latest_start)
            task.deadline = task.get_duration()
            task.start = 0
            task.end = task.get_duration()

    return tasks

def calcProfit(schedule):
    profit = 0
    duration=0
    for task in schedule:
        #print(task)
        duration += task.get_duration()
        profit+=task.get_max_benefit()
    return profit

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

def checkSchedule(schedule):
    currTime = 0
    for task in schedule:
        if(task.get_deadline() - task.get_duration() < currTime):
            print("False")
            break
        currTime += task.get_duration()
    print("True")

def shiftable(space, task, slot):
    return slot.get_end() - task.get_start() <= space

def shift(schedule, i, amount):
    while amount > 0 and i >= 0:
        if i == 0:
            ispace = schedule[i].get_start()
        else:
            ispace = schedule[i].get_start() - schedule[i-1].get_end()
        schedule[i].shift_left(amount)
        i -= 1
        amount -= ispace
    return schedule

def overlap(task1, task2):
    return task1.get_end() > task2.get_start() and task1.get_start() < task2.get_end()

def build_schedule(tasks, a, b):

    def heuristic(task):
        latest_start = task.get_deadline() - task.get_duration()
        benefit_rate = task.get_max_benefit() / task.get_duration()
        return a*latest_start - b*benefit_rate 
    
    tasks = sorted(tasks, key=heuristic)
    schedule = [tasks[0]]
    profit = tasks[0].get_max_benefit()

    for task in tasks[1:]:
        space = 0
        prev_space = 0
        end = 0
        for i, slot in enumerate(schedule): 
            space += slot.get_start() - end
            if i > 0:
                prev_slot = schedule[i-1]

            if len(schedule) == 1:
                if task.get_end() <= slot.get_start():
                    schedule.insert(0, task)
                    profit += task.get_max_benefit()
                    break

                elif overlap(task, slot):
                    if shiftable(space, task, slot):
                        schedule = shift(schedule, i, slot.get_end() - task.get_start())
                        schedule.append(task)
                        profit += task.get_max_benefit()
                        break
                else: 
                    schedule.append(task)
                    profit += task.get_max_benefit()
                    break

            elif (i+1) == len(schedule):
  
                if overlap(task, slot): 

                    if shiftable(space, task, slot):
                        schedule = shift(schedule, i, slot.get_end() - task.get_start())
                        schedule.insert(i+1, task)
                        profit += task.get_max_benefit()
                    break
                elif task.get_start() >= slot.get_end():

                    schedule.append(task)
                    profit += task.get_max_benefit()
                    break
                else:
                    if prev_slot.get_end() > task.get_start():
                        if shiftable(prev_space, task, prev_slot):
                            schedule = shift(schedule, i-1, prev_slot.get_end() - task.get_start())
                            schedule.insert(i, task)
                            profit += task.get_max_benefit()
                        break
                    else:
                        schedule.insert(i, task)
                        profit += task.get_max_benefit()
                    break

            elif slot.get_start() > task.get_end():
                if i == 0:
                    schedule.insert(0, task)
                    profit += task.get_max_benefit()
                    break
                elif overlap(task, prev_slot) and shiftable(prev_space, task, prev_slot):
                    schedule = shift(schedule, i-1, prev_slot.get_end() - task.get_start())
                    schedule.insert(i, task)
                    profit += task.get_max_benefit()
                    break
            end = slot.get_end()
            prev_space = space


    return schedule, profit 


def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing
    """

    tasks = zero_calibrate(tasks)
    max_profit = 0
    iterations = 1000
    final_sched = []

    for i in range(iterations):
        a = 1*random.random()
        b = 10*random.random()

        schedule, sum_profit = build_schedule(copy.deepcopy(tasks), a, b)
        #sum_profit = calc_benefit(schedule)
        if(sum_profit > max_profit):
            max_profit = sum_profit
            final_sched = schedule

    print(calcProfit(final_sched))
    print(max_profit)
    print(sum([task.get_duration() for task in final_sched]))

    for task in final_sched:
        print(task)

    return [task.get_task_id() for task in final_sched]

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