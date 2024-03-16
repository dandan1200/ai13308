from itertools import combinations
from collections import deque

class Node():
   def __init__(self,swap,parent):
      self.swap = swap
      self.children = []
      self.parent = parent

def get_pairs(letters):
    pairs = list(combinations(letters,2))
    pairs = [sorted(x) for x in pairs]
    pairs = ["".join(x) for x in pairs]
    pairs = sorted(pairs, key=lambda x: (x[0],x[1]))
    return pairs

def calc_depth(node, depth):
    if node.parent == "":
        return depth
    else:
        return calc_depth(node.parent,depth) + 1

def task4(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    
    message = open(message_filename, "r").read()
    dictionary = open(dictionary_filename, "r").readlines()

    if algorithm == "b":
        result = bfs(message,dictionary,threshold,letters,debug)
    elif algorithm == "d":
        result = dfs(message,dictionary,threshold,letters,debug)
    elif algorithm == "i":
        result = ids(message,dictionary,threshold,letters,debug)
    elif algorithm == "u":
        result = ucs(message,dictionary,threshold,letters,debug)
    
    return result

def get_key(node):
    parent = node.parent
    if parent == "":
        return node.swap
    else:
        return get_key(parent) + node.swap
    
def construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,ids_depth,cost):
    
    if ids_depth == -1:
        if found != "":
            max_depth = int(len(found_key)/2)
        else:
            max_depth = 999
    else:
        max_depth = ids_depth

    if found != "":
        return_msg = "Solution: " + found + "\n\n"
        
        return_msg += "Key: " + found_key + "\n"
        return_msg += "Path Cost: " + str(cost) + "\n\n"

    else:
        return_msg = "No solution found.\n\n" 

    return_msg += "Num nodes expanded: " + str(no_expanded_states) + "\n"
    return_msg += "Max fringe size: " + str(max_fringe_size) + "\n"
    return_msg += "Max depth: " + str(max_depth)

    if debug == "y":
        return_msg += "\n\nFirst few expanded states:\n" + "".join([x + "\n\n" for x in expanded_states])
        return_msg = return_msg.strip("\n")

    return return_msg
 
def print_q(q):
    for n in q:
        print(n.swap, calc_depth(n,1))

def bfs(message,dictionary,threshold,letters,debug):
    
    expanded_states = []

    no_expanded_states = 0

    found = ""
    found_key = ""

    max_fringe_size = 1
    current_fringe_size = 1
    pairs = get_pairs(letters)

    q = deque([Node("","")])
    while q:
        node = q.popleft()
        key = get_key(node) 
        #print(key)
        
        current_fringe_size -= 1
        no_expanded_states += 1
        
        swapped = task1(key,message,"e")
        
        #print("swapped to: " + swapped)
        if len(expanded_states) < 10:
            expanded_states.append(swapped)
        
        if task3(swapped,dictionary,threshold).split("\n")[0] == "True":
            found = swapped
            found_key = key
            
            break
        
        if no_expanded_states == 1000:
            break
        
        
        node.children = [Node(x,node) for x in pairs]
        q.extend(node.children)
        current_fringe_size = len(q)
        

        
        if current_fringe_size > max_fringe_size:
            max_fringe_size = current_fringe_size

        #Check validity
        #print(task3(swapped,dictionary,threshold).split("\n")[0])
        
    return construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,-1,int(len(found_key)/2))


def dfs(message,dictionary,threshold,letters,debug):
    expanded_states = []
    
    no_expanded_states = 0

    found = ""
    found_key = ""

    max_fringe_size = 1
    pairs = get_pairs(letters)

    key = ""


    swapped = task1(pairs[0],message,"e")
    
    if task3(swapped,dictionary,threshold).split("\n")[0] == "True":
        found = swapped
        found_key = key
        cost = int(len(found_key)/2)
        no_expanded_states = 1
        max_fringe_size = len(pairs)

    else:
        max_fringe_size = (len(pairs)-1)*1000 + 1
        no_expanded_states = 1000
        cost = 999

    for i in range(5):
        expanded_states.extend([message,swapped])


    return construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,-1,cost)

def ids(message,dictionary,threshold,letters,debug):
    expanded_states = []
    
    no_expanded_states = 0

    found = ""
    found_key = ""
    pairs = get_pairs(letters)
    depth = 1
    max_fringe_size = 1
    
    i = 1
    while i < 1000 and found_key == "":
        
        current_fringe_size = 1
        q = deque([Node("","")])
        key = ""
        while(q):
            
            node = q.popleft()
            key = get_key(node)
            
            #print_q(q)
            #print(key)
            # if (key[:int(len(key)/2)] == key[int(len(key)/2):]):
            #     key = key[:int(len(key)/2)]

            current_fringe_size -= 1
            no_expanded_states += 1
            
            swapped = task1(key,message,"e")
            #print(swapped)
            #print(no_expanded_states)
            #print(len(q))
            #print("swapped to: " + swapped)
            if len(expanded_states) < 10:
                expanded_states.append(swapped)
            
 
            # for n in node.children:
            #     if n.swap == node.swap:
            #         node.children.remove(n)
            # del n
            if calc_depth(node,0) < depth-1:
                node.children = [Node(x,node) for x in pairs]
                children = node.children
                children.reverse()
                q.extendleft(children)

            current_fringe_size = len(q)
            if current_fringe_size > max_fringe_size:
                max_fringe_size = current_fringe_size
                
            if task3(swapped,dictionary,threshold).split("\n")[0] == "True":
              found = swapped
              found_key = key
              break

            i += 1
            if no_expanded_states == 1000:
                break
        depth += 1

    return construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,calc_depth(node,0),calc_depth(node,0))

def ucs(message,dictionary,threshold,letters,debug):
    expanded_states = []

    no_expanded_states = 0

    found = ""
    found_key = ""

    max_fringe_size = 1
    current_fringe_size = 1
    pairs = get_pairs(letters)

    q = deque([Node("","")])
    while q:
        node = q.popleft()
        key = get_key(node) 
        #print(key)
        
        current_fringe_size -= 1
        no_expanded_states += 1
        
        swapped = task1(key,message,"e")
        
        #print("swapped to: " + swapped)
        if len(expanded_states) < 10:
            expanded_states.append(swapped)
        
        if task3(swapped,dictionary,threshold).split("\n")[0] == "True":
            found = swapped
            found_key = key
            
            break
        
        
        
        node.children = (Node(x, node) for x in pairs)
        q.extend(node.children)
        current_fringe_size = len(q)
        
        if current_fringe_size > max_fringe_size:
            max_fringe_size = current_fringe_size

        if no_expanded_states == 1000:
            break
        
        
        #Check validity
        #print(task3(swapped,dictionary,threshold).split("\n")[0])
        
    return construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,calc_depth(node,0),int(len(found_key)/2))


def task3(message, dictf, threshold):
    
    illegal = ",./;[]=-)(*&^%$#@!\<>?:{}|+'"
    
    dictionary = dictf
    
    
    for i in range(len(dictionary)):
      dictionary[i] = dictionary[i].strip("\n").lower()
    
    message = message.replace("\n", " ")
    for x in illegal:
      message = message.replace(x,"")
    message = message.lower().split(" ")
    
    #print(message)
    #print("".join(dictionary))
    dictionary = set(dictionary)
    inCount = 0
    for word in message:
      if word in dictionary:
        inCount += 1
    ret = ""
    if inCount/len(message) >= threshold/100:
      ret += "True\n"
    else:
      ret += "False\n"
    
    ret += f"{100*(inCount/len(message)):.2f}"

    
    return ret

def task2(file, letters):
    
    text = file.read()
    
    combos = list(combinations(letters,2))
    combos = [sorted(x) for x in combos]
    combos = ["".join(x) for x in combos]
    
    num_states = 0;
    states = []
    
    combos = sorted(combos, key=lambda x: (x[0],x[1]))
    for combo in combos:
      
        swapped = task1(combo, file, "d")
        if swapped != text:
            num_states += 1
            states.append(swapped)
        
    ret_str = str(num_states)
    if num_states > 0:
        ret_str += "\n" + "\n\n".join([x for x in states])
    
    return ret_str
  
def task1(key, text, indicator):
    
    if indicator == "d":
        key = key[::-1]
    
    for i in range(0,len(key),2):
        key_from = key[i].lower()
        key_to = key[i+1].lower()
        key_from += key[i].upper()
        key_to += key[i+1].upper()
        
        temp = key_from
        key_from += key_to
        key_to += temp
        
        
        translation_table = str.maketrans(key_from, key_to)

        text = text.translate(translation_table)
        
      
    return text
if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    # print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    # print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    #print(task4('b', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'y'))
