'''
Team Members: Jolin Lin and Amy Havill
'''

'''
Provides control and view GUI for set of dice
that can be rolled and summed once per turn in a game

Note:  all names start with self.
       all private instance variables start with self.__

Output to DiceGUI labels:
  sum (StringVar)

Input to DiceGUI:
  number_dice (Entry)
  reset (Button)

Modules imported:
  tkinter
  diegui
  diemultisided
  counter
Classes Used:
  DieGUI
  DieMultiSided
  Counter
'''
from tkinter import *
from tkinter import messagebox
import counter 
from diemultisided import *
from diegui import *

class DiceGUI(object):

  #-- Constructor --------------------------------------------------------
  def __init__(self):   
    self.main_window = Tk()

    # Created model, count variables, and counter
    self.__dice = []  # model
    self.__number_dice = 0
    self.__number_created = 0
    self.__roll_counter = counter.Counter()
    self.input_frame = Frame(self.main_window)

    self.input_label = Label(self.input_frame, text = 'Number of Dice: ')
    self.entry = Entry(self.input_frame, width = 2)
    self.entry.bind('<Return>', self.create_dice)

    self.input_label.pack(side = 'left')
    self.entry.pack(side = 'left')
    self.input_frame.pack()

    self.result_frame = Frame(self.main_window)

    # Create reset button, set its event handler to clear_rolls and its
    #  current state to 'disabled'
    self.reset = Button(self.result_frame, text = 'Reset', command = self.clear_rolls)
    self.reset.config(state = 'disabled')
    
    # Create static result Label: ' You rolled: '
    self.result_label = Label(self.result_frame, text = ' You rolled: ')

    # Create sum IntVar and initialize to 0
    self.sum = IntVar()
    self.sum.set(0)

    # Create dynamic result value label and set to IntVar
    self.result_value = Label(self.result_frame, textvariable = self.sum)
    
    # Pack widgets into the result frame
    self.reset.pack(side = 'left')
    self.result_label.pack(side = 'left')
    self.result_value.pack(side = 'left')

    # Pack result frame into the main window, run to check display, go to # 39.
    self.result_frame.pack()

    # Create dice label frame
    self.__dice_label_frame = Frame(self.main_window)

    # Create static dice labels
    self.__dice_separator = Label(self.__dice_label_frame,
      text = '---------------------------')
    self.__dice_label = Label(self.__dice_label_frame, \
                       text = 'DICE')

    self.__dice_separator.pack()
    self.__dice_label.pack()
    self.__dice_label_frame.pack()

    self.dice_frame = Frame(self.main_window)  
  
    mainloop()
    
#-- Predicates ---------------------------------------------------------
  # Check number of dice and number created count variables 
  def all_dice_have_been_created(self):
    return (self.__number_dice == self.__number_created)

  # Compare roll count with number of dice
  # invoke get_value() (Counter)
  def all_dice_have_been_rolled(self):
    return (self.__number_dice == self.__roll_counter.get_count())

#-- Accessors ----------------------------------------------------------
  # return dice_frame (Frame) - contains all dice  
  def get_dice_frame(self):
    return Parent.get_dice_frame(self)

  # invoke get_value() (Counter)
  # return count (int) of rolls this turn
  def get_roll_counter_value(self):
    count = self.__roll_counter.get_count()
    return count

#-- Mutators -----------------------------------------------------------

  def increment_number_created(self):
    self.__number_created += 1

  def increment_roll_counter(self):
    self.__roll_counter += 1

  def enable_roll_buttons(self):
    for die in range(self.__number_dice):
      die.DieGUI.enable_roll()

  def sum_rolls(self):
    # Sum of all rolls by iterating over each die in collection
    roll_value_str = DieGUI.get_roll_value()
    roll_value = int(roll_value_str)
    
    # Set IntVar to sum
    self.sum.set(roll_value)
    
    # Enable reset button (configure it to 'normal')
    self.reset.config(state = 'normal')

  #-- EVENT HANDLERS ---------------------------------------------------
  def create_dice(self, event):

    # Get number of dice (as string) requested by user from entry box
    self.__number_dice_str = self.entry.get()

    # Check that number of dice string is all digits
    if self.__number_dice_str.isdigit():
      self.__number_dice = int(self.__number_dice_str)
      self.entry.config(state = 'disable')
      
      # Loop for number of dice to be created
      for die in range(self.__number_dice):
        frame = DieGUI(Parent())                                  
        self.__dice.append(frame)
      
      self.dice_frame.pack()   
    # Otherwise, handle invalid entry
    else:    
      messagebox.showwarning('Warning', 'Please input digits')

      # Clear entry box
      self.entry.delete(0, END)
      

  # Reset roll counter, sum, all dice
  def clear_rolls(self):

    # Reset roll counter and sum
    self.__roll_counter = counter.Counter()
    self.sum.set(0)

    # Loop to reset each die in collection
    for die in range(self.__number_dice):
      # Disable reset button
      self.reset.config(state = 'disabled')
      
DiceGUI()
