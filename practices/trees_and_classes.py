
# Question 1

def int_power(b, e):
    if e == 0:
        return 1
    elif e == 1:
        return b
    else:
        return int_power(b * b, e // 2) * int_power(b, e % 2)

# Question 2

def make_change(amount, denominations):
    results = []
    for d in denominations:
        new_amount = amount - d
        if new_amount == 0:
            results += [[d]]
        elif new_amount > 0:
            new_in_d = make_change(new_amount, denominations)
            for n_d in new_in_d:
                n_d.insert(0, d)
            results += new_in_d
    return results

# For the rest:

class Tree:
    def __init__(self, key, value, children):
        self.key = key
        self.value = value
        self.children = children

tree1 = Tree("US", 4.6,
        [Tree("IL", 2.7,
            [Tree("Chicago", 2.7, [])]),
         Tree("PA", 1.9,
            [Tree("Pittsburgh", 0.3, []),
             Tree("Philadelphia", 1.6, [])])])
             
# Question 3

def get_population(T, node_keys):
    if T.key == node_keys[0]:
        if len(node_keys) == 1:
            return T.value
        else:
            for t in T.children:
                pop_t = get_population(t, node_keys[1:])
                if pop_t != None:
                    return pop_t
    return None
    
# Question 4

def path_to(T, key):
    if T.key  == key:
        return [key]
    for t in T.children:
        rest = path_to(t, key)
        if rest != []:
            return [T.key] + rest
    return []
    
# Question 5
            
def to_table(T):
    if len(T.children) == 0:
        return [[T.key, T.value]]
    result = []
    for t in T.children:
        sub_table = to_table(t)
        for i in sub_table:
            result.insert(0, [T.key] + i)
    return result
