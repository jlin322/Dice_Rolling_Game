'''
Team Members: Jolin Lin, Amy Havill
'''

'''
Notes:  This GUI lives inside its parent's window, so it doesn't have its own       
        all names start with self.
        model name starts with self.__

Provides control and view GUI for DieMultiSided model class
Models single multi-sided die that can be rolled

Model:
  __die (DieMultiSided)
Views:
  roll_value_label (Label)
  roll_value (StringVar)
Controllers:
  die_label (Label)
  num_sides_entry_box (Entry)
  roll_button (Button)
Organizational widgets:    
  parent_frame (Frame)
  die_frame (Frame)
Other instance objects:    
  parent (DiceGUI) - owner of this instance
  roll_value (StringVar)
Classes Used:
  BadArgument
  DieMultiSided
'''


#### Since this is a CHILD GUI, the invocation of mainloop() 
#### will take place in the parentGUI except for testing

from tkinter import *
from tkinter import messagebox
from diemultisided import *

class DieGUI:
  
#-- Constructor ---------------------------------------------------------------
  
  # Constructor defined with parent parameter
  # param parent GUI (DiceGUI) - owner of this instance
  def __init__(self, parent):

    # null model created
    self.__die = None 

    # Retrieve parent GUI object and get parent frame from it
    self.__parent = parent
    self.__parent_frame = self.__parent.get_dice_frame() 

    #self.win = Tk()
    self.die_frame = Frame(self.__parent_frame)
    #self.mid_frame = Frame(self.win)
    
    # static label and entry box for creating die
    self.sides_label = Label(self.die_frame, text = 'Sides')
    self.entry_sides = Entry(self.die_frame, width = 2)
    self.entry_sides.bind('<Return>', self.create_die)
    
    self.roll_button = Button(self.die_frame, text = 'ROLL', command = self.roll_die)
    self.roll_button.config(state = 'disable')
    #self.roll_button.pack(sides = 'right')

    # Initialize StringVar to '  ' to start
    #self.sum = Label(self.die_frame, text = 'Sum')
    self.roll_value = StringVar()
    self.roll_value.set('')
    self.display_value = Label(self.die_frame, textvariable = self.roll_value)
    self.value_num = Label(self.die_frame, textvariable = self.roll_value)

    # Pack widgets from side to side into die_frame
    #self.die_frame.pack()
    self.sides_label.pack(side = 'left')
    self.entry_sides.pack(side = 'left')
    self.roll_button.pack(side = 'left')
    #self.sum.pack(sides = 'top')
    #self.display_value.pack(sides = 'up')
    self.value_num.pack(side = 'right')
    
    # Pack the die_frame into parent frame
    self.die_frame.pack()
    

#-- Accessors -----------------------------------------------------------------
  def get_frame(self):
    return self.die_frame

  def get_roll_value(self):
    return self.roll_value.get()


#-- Mutators ------------------------------------------------------------------
  def reset_die(self):
    self.__die.reset()
    self.roll_value.set('')
    self.enable_roll()
    
  def enable_roll(self):
    self.roll_button.config(state = 'normal')


  #-- EVENT HANDLERs ----------------------------------------------------------
  def create_die(self, event):
    # Get number of sides on die string from entry box
    num_sides = self.entry_sides.get()
    try:
      # Check for invalid entry (e.g.,number of sides str isn't all digits, etc.)
      if not(num_sides.isdigit() and int(num_sides) > 0):
        raise BadArgument()
      else:
        self.__die = DieMultiSided(int(num_sides))
        self.entry_sides.config(state = 'disable')

      # Let parent know that another die has been created
      self.__parent.all_dice_have_been_created()
      
      # Have parent enable all roll buttons if all dice have been created
      if self.__parent.all_dice_have_been_created():
        self.__parent.enable_roll_buttons()
      
    # handle invalid entry
    except BadArgument as e:  
      # Warn user, clear entry box
      messagebox.showwarning('Warning', 'Input not valid')
      self.entry_sides.delete(0, END)
        
  def roll_die(self):
    # Roll the die and set the StringVar with the die value
    self.__die.roll()
    self.roll_value.set(self.__die)

    # Let parent know that die has been rolled and disable roll button
    self.__parent.all_dice_have_been_rolled()
    self.__parent.increment_roll_counter()
    self.roll_button.config(state = 'disabled')

    # Have parent sum the rolls if all dice have been rolled
    if self.__parent.all_dice_have_been_rolled():
      self.__parent.sum_rolls()

 
# -----------------------------------------------------------------------------
# Test Class
# Minimal parent GUI class for testing purposes ONLY!
class Parent:
  def __init__(self):
    # Create window and test widget frame
    self.__win = Tk()
    self.__parent_widgets = Frame(self.__win)

    # Create labels and IntVar for sum (of one die)
    self.__sum_label = Label(self.__parent_widgets, text = 'sum')
    self.__sum_var = IntVar()
    self.__sum_var.set(0)
    self.__sum_value = Label(self.__parent_widgets, textvariable = self.__sum_var)

    # Pack widgets, pack frame
    self.__sum_label.pack(side = 'left')
    self.__sum_value.pack(side = 'left')
    self.__parent_widgets.pack()

    # Create frame for die GUI, create die GUI   
    self.__dice_frame = Frame(self.__win)
    self.__die = DieGUI(self)

    # Pack frame for die GUI
    self.__dice_frame.pack()

    # Start listener
    mainloop()
    
  # ---------------------------------------------------------------------------
  # Stubbed versions of all necessary parent GUI methods

  # return the frame that will hold the die GUI
  def get_dice_frame(self):
    return self.__dice_frame

  # Only one will be created
  def increment_number_created(self):
    return 1

  # Only one will be rolled per turn
  def increment_roll_counter(self):
    return 1

  # return True since the only one has been rolled
  def all_dice_have_been_rolled(self):
    return True

  # return True since the only one has been created  
  def all_dice_have_been_created(self):
    return True

  # turn is over after one roll
  def enable_roll_buttons(self):
    self.__die.enable_roll()

  # only one has been rolled
  # get_roll_value() is second accessor found at #12
  def sum_rolls(self):
    self.__sum_var.set(int(self.__die.get_roll_value().strip()))
    self.enable_roll_buttons()

# -----------------------------------------------------------------------------

def main():
  reg1 = Parent() # create 4-sided die
  # Press <Enter> after entering 4 in the entry box
  # Keep on rolling until you are satisfied that it generates all values from
  #   1-4 inclusive and only those values
  # Click the x in the right-hand corner of the window when you are satisfied
  
  
  reg2 = Parent() # create 6-sided die
  # Press <Enter> after entering 6 in the entry box
  # Keep on rolling until you are satisfied that it generates all values from
  #   1-6 inclusive and only those values
  # Click the x in the right-hand corner of the window when you are satisfied
  
  reg3 = Parent() # create 12-sided die
  # Press <Enter> after entering 12 in the entry box
  # Keep on rolling until you are satisfied that it generates all values from
  #   1-12 inclusive and only those values
  # Click the x in the right-hand corner of the window when you are satisfied
  
  bad  = Parent() # create 3-sided die
  # Press <Enter> after entering 3 in the entry box
  # It should not be possible to create a die with less than 4 sides
  # Click the x in the right-hand corner of the window when you are satisfied  


if __name__ == '__main__':
  main()

  


  
