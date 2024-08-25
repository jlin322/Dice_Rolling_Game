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

# 1. Define imports
from tkinter import *
from tkinter import messagebox
import counter 
from diemultisided import *
from diegui import *
import subprocess
import winsound

# 2. Define class, go to bottom for #3.
class DiceGUI(object):

  #-- Constructor --------------------------------------------------------

  # 4. Define constructor, then go to #5 (bottom of constructor)
  def __init__(self):   

    # 7. Create main window
    self.main_window = Tk()
    self.main_window.title('Dice GUI')
    self.main_window.configure(bg = 'light blue')

    #--------------------------------------------------------------------------

    # 8. Create model, count variables, and counter
    self.__dice = []  # model
    self.__number_dice = 0
    self.__number_created = 0
    self.__roll_counter = counter.Counter() # secondary model

    #--------------------------------------------------------------------------

    # 9. Create user input frame 
    self.input_frame = Frame(self.main_window)
    self.input_frame.configure(bg = 'light blue')

    # 10. Create static label and entry box for entering number of dice
    self.input_label = Label(self.input_frame, text = 'Number of Dice: ')
    self.input_label.configure(bg = 'light blue')
    self.input_label.configure(font=("Times", 14))
    self.entry = Entry(self.input_frame, width = 2)
    self.entry.bind('<Return>', self.create_dice)
    #self.entry.configure(bg = 'light blue')


    # 22. Pack widgets into input frame
    self.input_label.grid(row = 0, column = 0)
    self.entry.grid(row = 0, column = 1)


    # 23. Pack input frame in the main window (check that it displays)
    self.input_frame.pack()

    #--------------------------------------------------------------------------

    # 28. Create result frame
    self.result_frame = Frame(self.main_window)


    # 29. Create reset button, set its event handler to clear_rolls and its
    self.reset = Button(self.result_frame, text = 'Reset', command = self.clear_rolls)
    self.reset.configure(font=("Times", 14))
    self.reset.config(state = 'disabled')
    
    # 34. Create static result Label: ' You rolled: '
    self.result_label = Label(self.result_frame, text = ' You rolled: ')
    self.result_label.configure(font=("Times", 14))
    self.result_label.configure(bg = 'light blue')

    # 35. Create sum IntVar and initialize to 0
    self.sum = IntVar()
    self.sum.set(0)

    # 36. Create dynamic result value label and set to IntVar
    self.result_value = Label(self.result_frame, textvariable = self.sum)            #Dynamic Label
    self.result_value.configure(bg = 'light blue')
    self.result_value.configure(font=("Times", 14))
    
    # 37. Pack widgets into the result frame
    self.reset.grid(row = 1, column = 0)
    self.result_label.grid(row = 1, column = 1)
    self.result_value.grid(row = 1, column = 2)

    # 38. Pack result frame into the main window, run to check display, go to # 39.
    self.result_frame.pack()

    #--------------------------------------------------------------------------

    # 24. Create dice label frame
    self.__dice_label_frame = Frame(self.main_window)
    self.__dice_label_frame.configure(bg = 'light blue')

    # 25. Create static dice labels
    self.__dice_separator = Label(self.__dice_label_frame,
      text = '---------------------------')
    self.__dice_separator.configure(bg = 'light blue')
    self.__dice_label = Label(self.__dice_label_frame, \
                       text = 'DICE')
    self.__dice_label.configure(font=("Times", 14))
    self.__dice_label.configure(bg = 'light blue')

    # 26. Pack dice label into dice label frame
    self.__dice_separator.grid(row = 2, column = 0)
    self.__dice_label.grid(row = 3, column = 0)

    # 27. Pack dice label frame into main window, run to check display, go to #28
    self.__dice_label_frame.pack()

    #--------------------------------------------------------------------------

    # 6. Create the dice Frame -- but don't pack it yet 
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
  def all_dice_have_been_rolled(self):
    return (self.__number_dice == self.__roll_counter.get_count())

#-- Accessors ----------------------------------------------------------

  # 40. Create accessors (Called by child GUI)

  # return dice_frame (Frame) - contains all dice  
  def get_dice_frame(self):
    return self.dice_frame

  def get_roll_counter_value(self):
    count = self.__roll_counter.get_count()
    return count


#-- Mutators -----------------------------------------------------------

  # 41. Create Mutators (Called by child GUI)

  # 42.
  def increment_number_created(self):
    self.__number_created += Parent.increment_number_created(self)
    
  # 43.
  # invoke increment() (Counter)
  def increment_roll_counter(self):
    self.__roll_counter.increment()

  # 44.
  # invoke enable_roll() (DieGUI) on each die in collection
  def enable_roll_buttons(self):
    for die in self.__dice:
      die.enable_roll()

  # 45.
  def sum_rolls(self):
    # Sum all rolls by iterating over each die in collection
    sum = 0
    for index in range(self.__number_dice):
      roll_value_str = self.__dice[index].get_roll_value()

      roll_value = int(roll_value_str)
      sum += roll_value
    
    # Set IntVar to sum
    self.sum.set(sum)
    
    # Enable reset button (configure it to 'normal')
    self.reset.config(state = 'normal')
 
  ### Now, test completely!

  #-- EVENT HANDLERS ---------------------------------------------------
    
  # 11. Create collection of dice requested by user
  def create_dice(self, event):

    # 12. Get number of dice (as string) requested by user from entry box
    self.__number_dice_str = self.entry.get()

    # 13. Check that number of dice string is all digits
    if self.__number_dice_str.isdigit():
    
      # 14. Store as integer if it is
      self.__number_dice = int(self.__number_dice_str)
    
      # 15. Disable entry box
      self.entry.config(state = 'disabled')
      
      # 16. Loop for number of dice to be created
      for die in range(self.__number_dice):
      
        # 17. Create object of DieGUI class and append to list of dice 
        frame = DieGUI(self)                                  
        self.__dice.append(frame)
        
      # 18. Pack the completed dice frame into the main window
      self.dice_frame.pack()
      
    # 19. Otherwise, handle invalid entry
    else:    
      # 20. Warn user
      messagebox.showwarning('WARNING', 'Input not valid')

      # 21. Clear entry box
      self.entry.delete(0, END)
      

  # 30. Reset roll counter, sum, all dice
  def clear_rolls(self):
    '''------------------------------------------------------------
      IMPORTANT: PLEASE COMMENT LINE 252 AND UNCOMMENT LINE 251
        IF YOU ARE USING A MAC
    ------------------------------------------------------------'''
    #subprocess.call(["afplay", "C:/Users/Jolin/OneDrive/Desktop/Dice Gui PRJ/cartoon006.wav"])
    winsound.PlaySound("C:/Users/Jolin/OneDrive/Desktop/Dice Gui PRJ/cartoon006.wav", winsound.SND_FILENAME)

    # 31. Reset roll counter and sum
    self.sum.set(0)
    self.__roll_counter = counter.Counter()
        
    # 32. Loop to reset each die in collection
    for index in range(self.__number_dice):
      self.__dice[index].reset_die()

      # 33. Disable reset button, go back up to # 34.
    self.reset.config(state = 'disabled')

# 3. Create instance of class
DiceGUI()
