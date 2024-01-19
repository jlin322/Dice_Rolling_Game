'''
Team Members: Jolin Lin, Amy Havill
'''

import random
import tkinter.messagebox

class BadArgument(Exception):
  def __init__(self):
    self.__title = 'Bad Argument'
    self.__message = 'Sides must be greater than or equal to four'
    
  def get_title(self):
    return self.__title

  def __str__(self):
    return self.__message

#raise BadArgument()

class DieMultiSided():
  MIN_SIDES = 4 # each die must have 4 or more sides
  NOT_YET_ROLLED = -1 # initial value before rolling

  def __init__(self, sides = 6):
    if self.is_valid(sides):
      self.__sides = sides
      self.__value = DieMultiSided.NOT_YET_ROLLED
    else:
      raise BadArgument()
   
  def is_valid(self, sides):
    return True if (int(sides)>= DieMultiSided.MIN_SIDES) else False

  def get_sides(self):
    return self.__sides

  def get_value(self):
    return self.__value

  def roll(self):
    self.__value = random.randint(1, self.__sides)
    
  def reset(self):
    self.__value = DieMultiSided.NOT_YET_ROLLED

  def __str__(self):
    return '' if (self.__value == DieMultiSided.NOT_YET_ROLLED) else str(self.__value)
                  
DieMultiSided()

# Tester for DieMultiSided class
def main():
  print("Create default die")
  die = DieMultiSided()
  print(f"Number Sides: {die.get_sides()}")
  print(f"Value (int): {die.get_value()}")
  print(f"Value (str): {die}")
  print()
  inputStr = ''
  while not inputStr:
    die.roll()
    print(f"Value (int): {die.get_value()}")
    print(f"Value (str): {die}")
    inputStr = input("Press any key to exit loop: ")
  print()
  
  print("\nCreate 12-sided die")
  die = DieMultiSided(12)
  print(f"Number Sides: {die.get_sides()}")
  print(f"Value (int): {die.get_value()}")
  print(f"Value (str): {die}")
  print()
  inputStr = ''
  while not inputStr:
    die.roll()
    print(f"Value (int): {die.get_value()}")
    print(f"Value (str): {die}")
    inputStr = input("Press any key to exit loop: ")
  print()
  
  print("\nCreate die with invalid state")
  try:
    die = DieMultiSided(3)
    print(f"Number Sides: {die.get_sides()}")
    print(f"Value (int): {die.get_value()}")
    print(f"Value (str): {die}")
    print()
    inputStr = ''
    while not inputStr:
      die.roll()
      print(f"Value (int): {die.get_value()}")
      print(f"Value (str): {die}")
      inputStr = input("Press any key to exit loop: ")
  except BadArgument as e:
    tkinter.messagebox.showerror(e.get_title(), str(e)) 
  
if __name__ == '__main__':
  main()
  