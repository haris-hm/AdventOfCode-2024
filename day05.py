class Rule:
    def __init__(self, before: set[int]=set(), after: set[int]=set()):
        self.before = before
        self.after = after

    def __repr__(self) -> str:
        return str([self.before, self.after])

rules: dict[int, Rule] = {}
updates: list[list[int]] = []

with open('./inputs/day05/0.txt', 'r') as file:
    contents = file.read()
    inputs = contents.split('\n')
    sep_found: bool = False
    
    for i in inputs:
        if i == '':
            sep_found = True
            continue

        if sep_found:
            updates.append([int(k) for k in i.split(',')])
            continue

        left: int = int(i[0:2])
        right: int = int(i[3:5])
        
        if left in rules.keys():
            rules[left].after.add(right)
        else:
            rules[left] = Rule(after={right})

        if right in rules.keys():
            rules[right].before.add(left)
        else:
            rules[right] = Rule(before={left})

def follows_rules(update: list[int], rules: dict[int, Rule], incorrect_updates: list[list[int]] = []) -> bool:
    for i, page in enumerate(update):
        before = set(update[:i])
        after = set(update[i+1:])

        rule_before = set(rules[page].before)
        rule_after = set(rules[page].after)

        if ((before.issubset(rule_before) or len(before) == 0) and (after.issubset(rule_after) or len(after) == 0)):
            #print(f'Correct: {before} {page} {after}')
            continue
        else:
            incorrect_updates.append(update)
            return False
    return True

def check_updates(update_list: list[list[int]], rules: dict[int, Rule]):
    middle_page_sum: int = 0
    incorrect_updates: list[list[int]] = []

    for update in update_list:    
        if follows_rules(update, rules, incorrect_updates):
            middle_page_sum += update[len(update)//2]

    return middle_page_sum, incorrect_updates

for rule in rules.keys():
    print(f'{rule}: {rules[rule]}')

def fix_updates(updates: list[list[int]], rules: dict[int, Rule]) -> int:
    for update in updates:
        i: int = 0
        page: int = 0

        while i < len(update):
            before: list[int] = update[:i]
            after: list[int] = update[i:]
            before_correct: bool = follows_rules(before, rules)
            after_correct: bool = follows_rules(after, rules)
            page = update[i]

            if not before_correct:
                before_rule : list[int] = list(rules[page].before)
                difference = [k for k in before if k not in before_rule and k != page]
                
                if difference != []:
                    print(f'Page: {page}, rule: {before_rule}, before set: {before}, difference: {difference}')

            if not after_correct:
                after_rule: list[int] = list(rules[page].after)
                difference = [k for k in after if k not in after_rule and k != page]

                if difference != []:
                    print(f'Page: {page}, rule: {after_rule}, before set: {before}, difference: {difference}')

            i += 1

        print(update)

    return updates
            
mid_sum, incorrect_updates = check_updates(updates, rules)

print(f'Middle Page Sum: {mid_sum}')
print(f'Number of incorrect updates: {len(incorrect_updates)}')

fix_updates(incorrect_updates, rules)

