from parse import read_input_file, write_output_file
import os
import Task

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

def calc_task_heuristic(task):
    return (task.get_deadline - task.get_duration) + 0.2 * task.get_max_benefit

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    heuristic_list = 
    tasks = sorted(tasks, key=lambda x: calc_task_heuristic(x))
    tasks = zero_calibrate(tasks)
    tasks = remove_weak(tasks)

    print(sum([task.get_max_benefit() for task in tasks]))

    big_schedule = []
    big_benefit = 0
    leftovers = []

    for i in range(6):
        segment_end = 240 * (i+1)

        schedule, benefit, tasks = find_best_schedule(tasks, [], segment_end)
        big_schedule += schedule
        big_benefit += benefit
        duration = sum([task.get_duration() for task in schedule])

        leftovers.append(Task.Task(100 + i, 240*i + duration, int(duration), float(benefit)))
        while tasks and tasks[0].get_deadline() - tasks[0].get_duration() < segment_end:
            leftovers.append(tasks.pop(0))

    onion, ben = find_schedule(leftovers)

    dur = 0
    for task in onion:
        print(task)
        dur += task.get_duration()

    print(ben)
    print(dur)


    #print output
    schedule_ids = [task.get_task_id() for task in big_schedule]
    return schedule_ids

def main():
    for input_path in os.listdir('inputs/'):
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)

if __name__ == "__main__":
    main()




# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)