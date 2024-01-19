'''
Team Members: Jolin Lin and Amy Havill
'''

class Counter:

  # Constructor 
  def __init__(self):
    self.__count = 0  

  # Accessors
  def get_count(self):
    return self.__count
  
  # Mutators
  def increment(self):
    self.__count += 1

  def decrement(self):
    self.__count -= 1
  
  def reset(self):
    self.__count = 0
 
  def set_count(self, count):
    self.__count = count

  def can_decrement(self):        #accessor
    return self.__count > 0

  def decrement_with_limit(self):   #mutator- modifies info.
    if can_decrement(self) == True:
      self.__count -= 1

  def __str__(self):
    return f'count = {self.__count}'

def main():
  
  counter1 = Counter()
  counter1.increment()
  print(counter1.get_count())
  counter1.set_count(10)
  print(counter1.get_count())
  counter1.decrement()
  print(counter1.get_count())
  counter1.reset()
  print(counter1)

if __name__ == '__main__':
  main()
  
