from math import ceil
def task5(message_filename, is_goal):
  
  frequencies = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
  
  if is_goal == True:
    return 0
  else:
    message = open(message_filename, "r").read().upper()
      
    frequency_count = {}
      
    for char in message:
      if char.isalpha() == False:
        continue
          
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
    
if __name__ == '__main__':
  # Example function calls below, you can add your own to test the task5 function
  print(task5('test.txt', False))
  # print(task5('cabs.txt', True))
  # print(task5('freq_eg2.txt', False))
