def task1(key, text, indicator):
    text = open(text,"r").read()
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
    print(task1('AOATET',"secret_msg.txt", "e"))