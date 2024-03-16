from itertools import combinations
from collections import deque
import heapq
from math import ceil

def print_q(q):
    print("Queue", len(q))
    for _,n in q:
        print(n.swap, calc_depth_(n,1))

class Node1():
    def __init__(self,swap,parent):
        self.swap = swap
        self.children = []
        self.parent = parent
        self.h = -1
    
    def set_h(self,h):
        self.h = h

    def __lt__(self, other):
        return self.h < other.h
def get_pairs_(letters):
    pairs = list(combinations(letters,2))
    pairs = [sorted(x) for x in pairs]
    pairs = ["".join(x) for x in pairs]
    pairs = sorted(pairs, key=lambda x: (x[0],x[1]))
    return pairs

def calc_depth_(node, depth):
    if node.parent == "":
        return depth
    else:
        return calc_depth_(node.parent,depth) + 1
    
def get_key_(node):
    parent = node.parent
    if parent == "":
        return node.swap
    else:
        return get_key_(parent) + node.swap

def construct_return_msg_(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,ids_depth,cost):
    
    if ids_depth == -1:
        if found_key:
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

def task5_(message, is_goal):
  
  frequencies = ['E', 'T', 'A', 'O', 'N', 'S']
  
  if is_goal == True:
    return 0
  else:
    message = message.upper()
      
    frequency_count = {}
      
    for char in message:
      if char in frequencies:
        if char in frequency_count:
          frequency_count[char] += 1
        else:
          frequency_count[char] = 1
      
    sorted_letters = sorted(frequency_count, key=lambda x : (-frequency_count[x],x,))
                               
      
    t = []
    for char in frequencies:
      if char in sorted_letters:
        t.append(char)
      
			# compare t to sorted_letters
    count = 0
      
    for num in range(len(t)):
      if t[num] != sorted_letters[num]:
        count += 1  
        
  return ceil(count/2)


def greedy(message,dictionary,threshold, letters, debug):

    original_msg = message


    for i in range(len(dictionary)):
      dictionary[i] = dictionary[i].strip("\n").lower()
    dictionary = set(dictionary)
    
    

    expanded_states = []

    no_expanded_states = 0

    found = ""
    found_key = ""

    max_fringe_size = 1
    current_fringe_size = 1
    found_key = ""
    q = []

    node = Node1("","")
    key = get_key_(node) 
    swapped = task1_(key,message,"e")
    h = task5_(swapped, task3_(swapped,dictionary,threshold).split("\n")[0] == "True")
    heapq.heappush(q,(h, node))

    
    while q:
        #print(no_expanded_states)
        # print_q(q)
        
        _, node = heapq.heappop(q)
        key = get_key_(node) 

        current_fringe_size -= 1
        
        
        #print(_, key)
        no_expanded_states += 1
        
        swapped = task1_(key,message,"e")

        if len(expanded_states) < 10:
            expanded_states.append(swapped)
        
        
        if task3_(swapped,dictionary,threshold).split("\n")[0] == "True":
            found = swapped
            found_key = key
            break
        
        node.children = [Node1(x,node) for x in get_pairs_(letters)]
        # for n in Node1.children:
        #     if n.swap == Node1.swap:
        #         Node1.children.remove(n)

        for child in node.children:
            child_key = get_key_(child)
            child_swapped = task1_(child_key,original_msg,"e")
            goal = task3_(child_swapped,dictionary,threshold).split("\n")[0]
            #print(goal)
            h = task5_(child_swapped, goal  == "True")
            #print(child_swapped)
            child.set_h(h)
            #print("h", h)
            heapq.heappush(q,(h, child))
            current_fringe_size += 1
        
        if current_fringe_size > max_fringe_size:
            max_fringe_size = current_fringe_size

        
        
        
        
        #print(swapped)
        
        
        if no_expanded_states == 1000:
            break

        
        # print("Q: ")
        # for x in q:
        #     print("current: ", x.swap)
        #     if x.parent != "":
        #         print("parent: ", x.parent.swap)

        

        #Check validity
        #print(task3_(swapped,dictionary,threshold).split("\n")[0])
        
    return construct_return_msg_(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,calc_depth_(node,0),int(len(found_key)/2))
    
def task3_(message, dictf, threshold):
    
    
    dictionary = dictf
    illegal = ",./;[]=-)(*&^%$#@!\<>?:{}|+'"

    message = message.replace("\n", " ")
    for x in illegal:
        message = message.replace(x,"")

    
    message = message.lower().split(" ")
    
    #print(message)
    #print("".join(dictionary))
    
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

def task1_(key, text, indicator):
    
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


class Node():
    def __init__(self, swap, parent=None, cost=0):
        self.swap = swap
        self.children = []
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.cost < other.cost

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.cost == other.cost

    def __ne__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.cost != other.cost


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
   
def construct_return_msg(found_key,found,no_expanded_states,max_fringe_size,expanded_states,debug,ids_depth,cost):
   
    if ids_depth == -1:
        if found_key:
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

def astar(message, dictionary, threshold, letters, debug):
    expanded_states = []

    no_expanded_states = 0

    found = ""
    found_key = ""

    max_fringe_size = 1
    current_fringe_size = 1
    pairs = get_pairs(letters)

    q = [Node("", "")]
    heapq.heapify(q)
    while q:
        node = heapq.heappop(q)

        key = node.swap

        current_fringe_size -= 1
        no_expanded_states += 1

        swapped = task1(key, message, "e")

        if len(expanded_states) < 10:
            expanded_states.append(swapped)

        if task3(swapped, dictionary, threshold).split("\n")[0] == "True":
            found = swapped
            found_key = key

            break

        node.children = []
        for pair in pairs:
            child = Node(key + pair, node)
            h = task5(task1(child.swap, message, "e"))
            try:
                child.cost = node.cost + h
            except Exception:
                child.cost = h
            node.children.append(child)

        # Sort children based on swap attribute in alphabetical order
        node.children.sort(key=lambda x: x.swap)

        # Add sorted children to the priority queue
        for child in node.children:
            heapq.heappush(q, child)

        current_fringe_size = len(q)


        if current_fringe_size > max_fringe_size:
            max_fringe_size = current_fringe_size

        if no_expanded_states == 1000:
            break

    return construct_return_msg(found_key, found, no_expanded_states, max_fringe_size, expanded_states, debug, calc_depth(node, 0), int(len(found_key) / 2))

def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    message = open(message_filename, "r").read()
    dictionaryl = open(dictionary_filename, "r").readlines()

    dictionary = "".join(dictionaryl)

    if algorithm == "g":
        result = greedy(message,dictionaryl,threshold,letters,debug)
    elif algorithm == "a":
        result = astar(message,dictionary,threshold,letters,debug)
    
    return result


def task5(message):
  
    message = message.upper()
    
    frequencies = {'E': 0, 'T': 0, 'A': 0, 'O': 0, 'N': 0, 'S': 0}

    for char in message:
        if char in frequencies:
            frequencies[char] += 1

    sorted_letters = sorted(frequencies, key=lambda x : (-frequencies[x],x,))
                                
        
    t = []
    for char in frequencies:
        if char in sorted_letters:
            t.append(char)
        
    count = 0
        
    for num in range(len(t)):
        if t[num] != sorted_letters[num]:
            count += 1  
        
    return ceil(count/2)

def task3(message, dictf, threshold):
   
    illegal = ",./;[]=-)(*&^%$#@!\<>?:{}|+'"
    
    dictionary = set(dictf.lower().split("\n"))

    message = message.replace("\n", " ")
    for x in illegal:
      message = message.replace(x,"")
    message = message.lower().split(" ")
   
    #print(message)
    #print("".join(dictionary))
    
    message_len = len(message)
    
    #print(message_len)
    
    
    inCount = 0
    count = 0
    for word in message:
      curr = (count/message_len)
      inv_requirement = round(1-(threshold/100),2)
      if curr > inv_requirement:
        break
      if word in dictionary:
        inCount += 1
      else:
        count += 1
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
    # Example function calls below, you can add your own to test the task6 function
    # print(task6('g', 'cabs.txt', 'common_words.txt', 90, 'ABC', 'y'))
    print(task6('g', 'quokka.txt', 'common_words.txt', 80, 'AENOST', 'y'))
    # print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))

    
    