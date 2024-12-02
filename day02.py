input_1: list[str] = []

with open('./inputs/input0201.txt', 'r') as file:
    contents = file.read()
    for i in contents.split('\n'):
        if (len(i) > 0):
            report = [int(j) for j in i.split(' ')]
            input_1.append(report)

def is_safe(report: list[int]) -> bool:
    decreasing: bool = True if report[0] > report[1] else False
    safe: bool = True

    for level in range(len(report)-1):
        lvl = report[level]
        next_lvl = report[level + 1]
        if ((lvl < next_lvl and decreasing) \
            or (lvl > next_lvl and not decreasing)):
            safe = False

        if abs(report[level]-report[level + 1]) > 3 or lvl == next_lvl:
            safe = False
    
    return safe

def dampen_problems(report: list[int]) -> bool:
    safe: bool = False

    for i in range(len(report)):
        dampened_report = report.copy()
        dampened_report.pop(i)

        if is_safe(dampened_report):
            safe = True
            break

    return safe

def determine_safety(input: list[list[int]]) -> int:
    safe_reports: int = 0

    for report in input:
        safe: bool = is_safe(report)

        if not safe:
            safe = dampen_problems(report)
        
        if safe:
            print(f'{report = }')
            safe_reports += 1
            

    return safe_reports


print(f'Safe Reports: {determine_safety(input_1)}')