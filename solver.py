from parse import read_input_file, write_output_file
import os
import Task

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

def zero_calibrate(tasks):
    for task in tasks:
        latest_start = task.get_deadline() - task.get_duration()
        if latest_start < 0:
            task.perfect_benefit = task.get_late_benefit(-latest_start)
            task.deadline = task.get_duration()

    return tasks

def find_schedule(tasks, start_time=0, buckets=1):
    def find_schedule_helper(tasks, schedule=[], elapsed_time=0):
        if not tasks:
            return schedule, calc_benefit(schedule, start_time, start_time + (1440/buckets)), elapsed_time

        return max(find_schedule_helper(tasks[1:], schedule + [tasks[0]], elapsed_time + tasks[0].get_duration()), 
                   find_schedule_helper(tasks[1:], schedule, elapsed_time), 
                   key = lambda k: k[1])

    return find_schedule_helper(tasks)

def calc_task_heuristic(task):
    return (task.get_deadline() - task.get_duration()) - .5 * task.get_max_benefit()

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    tasks = sorted(zero_calibrate(tasks), key=lambda x: x.get_deadline() - x.get_duration())
    stack = []
    big_task_dict = {}
    num_buckets = 5
    end_time = 0

    for i in range(num_buckets):
        crabs = sorted(tasks[20*i:20*(i+1)], key=lambda x: calc_task_heuristic(x))
        bucket = crabs[:18]
        buffer = crabs[18:]

        schedule, benefit, end_time = find_schedule(bucket, end_time, num_buckets)
        duration = sum([task.get_duration() for task in schedule])

        big_task = Task.Task(100+i+1, (i+1) * 288, int(duration), float(benefit))
        big_task_dict[big_task] = schedule

        stack.append(big_task)
        stack += buffer

    final_schedule, final_benefit, final_duration = find_schedule(stack) 

    #print schedule
    for task in final_schedule:
        print(task)
    print()
    print("benefit:", final_benefit)
    print("duration:", final_duration)

    #convert big tasks to their individual tasks
    expanded_final_schedule = []
    for task in final_schedule:
        if task in big_task_dict:
            expanded_final_schedule += big_task_dict[task]
        else:
            expanded_final_schedule.append(task)

    return [task.get_task_id() for task in expanded_final_schedule]

def main():
    for input_path in os.listdir('inputs/'):
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file('inputs/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)

if __name__ == "__main__":
    main()
