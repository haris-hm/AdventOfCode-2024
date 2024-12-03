input_1: list[str] = []
input_2: list[str] = []

with open('./inputs/day01/1.txt', 'r') as file:
    contents = file.read()
    for i in contents.split('\n'):
        if (len(i) > 0):
            ids = i.split('   ')
            input_1.append(ids[0])
            input_2.append(ids[1])

# Part 1
def find_total_distance(input_list_1: list[str], input_list_2: list[str]) -> int:
    input_list_1.sort()
    input_list_2.sort()
    sum: int = 0

    input_list_1 = [int(i) for i in input_list_1]
    input_list_2 = [int(i) for i in input_list_2]

    for i in range(len(input_list_1)):
        sum += abs(input_list_1[i]-input_list_2[i])

    return sum

# Part 2
def find_similarity_scores(input_list_1: list[str], input_list_2: list[str]) -> int:
    input_list_1 = [int(i) for i in input_list_1]
    input_list_2 = [int(i) for i in input_list_2]
    number_frequency: dict[int, int] = {}
    score: int = 0

    for i in input_list_2:
        if i in number_frequency.keys():
            number_frequency[i] += 1
        else:
            number_frequency[i] = 1

    for i in input_list_1:
        score += i*number_frequency[i] if i in number_frequency.keys() else 0

    return score

print(f'Total Distance: {find_total_distance(input_1.copy(), input_2.copy())}.')
print(f'Similarity Score: {find_similarity_scores(input_1.copy(), input_2.copy())}.')
