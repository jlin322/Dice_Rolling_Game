'''
Jolin Lin and Amy Havill
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

#### Develop this class incrementally, ordered by the comment #s

# 1. Define imports
from tkinter import *
from tkinter import messagebox
import counter 
from diemultisided import *
from diegui import *

# 2. Define class, go to bottom for #3.
class DiceGUI(object):

  #-- Constructor --------------------------------------------------------

  # 4. Define constructor, then go to #5 (bottom of constructor)
  # Model:
  #   __dice (list of DieGUI)
  # Views:
  #   input_label (Label)
  #   result_label (Label)
  #   result_value (Label)
  #   dice_label (Label)
  #   sum (IntVar)
  # Controls:
  #   entry (Entry)
  #   reset (Button)
  # Organizational widgets:    
  #   main_window (Tk)
  #   input_frame (Frame)
  #   result_frame (Frame)
  #   dice_label_frame (Frame)
  #   dice_frame (Frame)    
  # Other instance variables and objects:    
  #   __number_dice (int)
  #   __number_created (int)
  #   __roll_counter (Counter) 
  def __init__(self):   

    # 7. Create main window
    self.main_window = Tk()

    #--------------------------------------------------------------------------

    # 8. Create model, count variables, and counter
    self.__dice = []  # model
    self.__number_dice = 0
    self.__number_created = 0
    self.__roll_counter = counter.Counter() # secondary model

    #--------------------------------------------------------------------------

    # 9. Create user input frame 
    self.input_frame = Frame(self.main_window)

    # 10. Create static label and entry box for entering number of dice
    # Bind entry box to create_dice event handler
    # Then go down to #11
    self.input_label = Label(self.input_frame, text = 'Number of Dice: ')
    self.entry = Entry(self.input_frame, width = 2)
    self.entry.bind('<Return>', self.create_dice)


    # 22. Pack widgets into input frame
    self.input_label.pack(side = 'left')
    self.entry.pack(side = 'left')


    # 23. Pack input frame in the main window (check that it displays)
    self.input_frame.pack()

    #--------------------------------------------------------------------------

    # 28. Create result frame
    self.result_frame = Frame(self.main_window)


    # 29. Create reset button, set its event handler to clear_rolls and its
    #     current state to 'disabled', go to # 30.
    self.reset = Button(self.result_frame, text = 'Reset', command = self.clear_rolls)
    self.reset.config(state = 'disabled')
    
    # 34. Create static result Label: ' You rolled: '
    self.result_label = Label(self.result_frame, text = ' You rolled: ')

    # 35. Create sum IntVar and initialize to 0
    self.sum = IntVar()
    self.sum.set(0)

    # 36. Create dynamic result value label and set to IntVar
    self.result_value = Label(self.result_frame, textvariable = self.sum)
    
    # 37. Pack widgets into the result frame
    self.reset.pack(side = 'left')
    self.result_label.pack(side = 'left')
    self.result_value.pack(side = 'left')

    # 38. Pack result frame into the main window, run to check display, go to # 39.
    self.result_frame.pack()

    #--------------------------------------------------------------------------

    # 24. Create dice label frame
    self.__dice_label_frame = Frame(self.main_window)

    # 25. Create static dice labels
    self.__dice_separator = Label(self.__dice_label_frame,
      text = '---------------------------')
    self.__dice_label = Label(self.__dice_label_frame, \
                       text = 'DICE')

    # 26. Pack dice label into dice label frame
    self.__dice_separator.pack()
    self.__dice_label.pack()

    # 27. Pack dice label frame into main window, run to check display, go to #28
    self.__dice_label_frame.pack()

    #--------------------------------------------------------------------------

    # 6. Create the dice Frame -- but don't pack it yet 
    # Will be packed after number of DieGUI objects to be created is known
    # (See create_dice() event handler), go back up to #7
    self.dice_frame = Frame(self.main_window)  
  
    #--------------------------------------------------------------------------

    # 5. Start the main loop, go to #6
    mainloop()
    
#-- Predicates ---------------------------------------------------------

  # 39. Create Predicates (Called by child GUI)

  # Check number of dice and number created count variables 
  def all_dice_have_been_created(self):
    return (self.__number_dice == self.__number_created)

  # Compare roll count with number of dice
  # invoke get_value() (Counter)
  def all_dice_have_been_rolled(self):
    return (self.__number_dice == self.__roll_counter.get_count())

#-- Accessors ----------------------------------------------------------

  # 40. Create accessors (Called by child GUI)

  # return dice_frame (Frame) - contains all dice  
  def get_dice_frame(self):
    return Parent.get_dice_frame(self)

  # invoke get_value() (Counter)
  # return count (int) of rolls this turn
  def get_roll_counter_value(self):
    count = self.__roll_counter.get_count()
    return count


#-- Mutators -----------------------------------------------------------

  # 41. Create Mutators (Called by child GUI)

  # 42.
  def increment_number_created(self):
    self.__number_created += 1
    
  # 43.
  # invoke increment() (Counter)
  def increment_roll_counter(self):
    self.__roll_counter += 1

  # 44.
  # invoke enable_roll() (DieGUI) on each die in collection
  def enable_roll_buttons(self):
    for die in range(self.__number_dice):
      die.DieGUI.enable_roll()

  # 45.
  # invoke get_roll_value() (DieGUI)
  # invoke set() (IntVar)
  # invoke config() (Button)
  def sum_rolls(self):
    # Sum all rolls by iterating over each die in collection
    # (Watch out for str vs. int types)
    roll_value_str = DieGUI.get_roll_value()
    roll_value = int(roll_value_str)
    
    # Set IntVar to sum
    self.sum.set(roll_value)
    
    # Enable reset button (configure it to 'normal')
    self.reset.config(state = 'normal')
 
  ### Now, test completely!

  #-- EVENT HANDLERS ---------------------------------------------------
    
  # 11. Create collection of dice requested by user
  # invoke:
  #   get() (entry)
  #   config() (entry)
  #   delete() (entry)
  #   isdigit() (str)
  #   append() (list of DiceGUI)
  #   pack() (Frame)
  #   showerror() (messagebox)
  def create_dice(self, event):

    # 12. Get number of dice (as string) requested by user from entry box
    self.__number_dice_str = self.entry.get()

    # 13. Check that number of dice string is all digits
    if self.__number_dice_str.isdigit():
    
      # 14. Store as integer if it is
      self.__number_dice = int(self.__number_dice_str)
    
      # 15. Disable entry box
      self.entry.config(state = 'disable')
      
      # 16. Loop for number of dice to be created
      for die in range(self.__number_dice):
      
        # 17. Create object of DieGUI class and append to list of dice 
        frame = DieGUI(Parent())                              # What to put for argument parent in DieGUI?               
        self.__dice.append(frame)
        
      # 18. Pack the completed dice frame into the main window
      self.dice_frame.pack()
      
    # 19. Otherwise, handle invalid entry
    else:    
      # 20. Warn user
      messagebox.showwarning('Warning', 'Please input digits')

      # 21. Clear entry box
      self.entry.delete(0, END)
      

  # 30. Reset roll counter, sum, all dice
  # invoke:
  #   reset() (CounterWP)
  #   set() (IntVar)
  def clear_rolls(self):

    # 31. Reset roll counter and sum
    self.__roll_counter = counter.Counter()
    self.sum.set(0)

    # 32. Loop to reset each die in collection
    for die in range(self.__number_dice):

      # 33. Disable reset button, go back up to # 34.
      self.reset.config(state = 'disabled')

# 3. Create instance of class
DiceGUI()
