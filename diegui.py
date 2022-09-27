'''
Jolin Lin, Amy Havill
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

# 1. define imports
from tkinter import *
from tkinter import messagebox
from diemultisided import *

# 2. define class
class DieGUI:
  
#-- Constructor ---------------------------------------------------------------
  
  # 3. define constructor, parent parameter
  # param parent GUI (DiceGUI) - owner of this instance
  def __init__(self, parent):

    # 4. Create null model for now (so we have a reference for later)
    self.__die = None  # Will be created from dieStr.DieMultiSided(sides) 

    # 5. Retrieve parent GUI object and get parent frame from it
    # This object's widgets will live in parent frame or window
    self.__parent = parent
    self.__parent_frame = self.__parent.get_dice_frame() # in DiceGUI class

    # 6. Create frame for this die's widgets
    #self.win = Tk()
    self.die_frame = Frame(self.__parent_frame)
    #self.mid_frame = Frame(self.win)
    
    # 7. Create static label and entry box for creating die (inside frame from #6)
    # Bind entry box to create_die event handler (#14-18)
    # User must specify number of sides before creation
    self.sides_label = Label(self.die_frame, text = 'Sides')
    self.entry_sides = Entry(self.die_frame, width = 2)
    self.entry_sides.bind('<Return>', self.create_die)
    

    # 8. Create button controller (inside frame from #6) for rolling die
    # set event handler to roll_die (#19-21)
    # make sure that button is 'disabled' to start
    self.roll_button = Button(self.die_frame, text = 'ROLL', command = self.roll_die)
    self.roll_button.config(state = 'disable')
    #self.roll_button.pack(sides = 'right')

    # 9. Create and set up StringVar and dynamic label viewer (inside frame from #6)
    #    to display the value that was rolled
    # Initialize StringVar to '  ' to start
    #self.sum = Label(self.die_frame, text = 'Sum')
    self.roll_value = StringVar()
    self.roll_value.set('')
    self.display_value = Label(self.die_frame, textvariable = self.roll_value)
    self.value_num = Label(self.die_frame, textvariable = self.roll_value)

    # 10. Pack the widgets from side to side into the die_frame (#6)
    #self.die_frame.pack()
    self.sides_label.pack(side = 'left')
    self.entry_sides.pack(side = 'left')
    self.roll_button.pack(side = 'left')
    #self.sum.pack(sides = 'top')
    #self.display_value.pack(sides = 'up')
    self.value_num.pack(side = 'right')
    
    # 11. Pack the die_frame (#6) into the parent frame
    self.die_frame.pack()
    

#-- Accessors -----------------------------------------------------------------

  #  12. Create Accessors
  
  # retrieve die_frame (Frame) (#6)
  def get_frame(self):
    return self.die_frame


  # invoke get() (StringVar)  
  # retrieve roll_value (StringVar)
  def get_roll_value(self):
    return self.roll_value.get()


#-- Mutators ------------------------------------------------------------------

  # 13. Create Mutators
    
  # Reset before next turn
  # invoke:
  #  reset() (DieMultiSided)
  #  set() (StringVar)
  #  __str__() (DieMultiSided)
  #  enable_roll() (self)
  def reset_die(self):
    self.__die.reset()
    self.roll_value.set('')
    self.enable_roll()


  # Enable roll_button after all dice have been created and after each turn
  # invokes:
  #  config (Button)
  def enable_roll(self):
    self.roll_button.config(state = 'normal')


  #-- EVENT HANDLERs ----------------------------------------------------------

  # Create die with given number of sides
  # invoke:
  #   get() (Entry)
  #   config() (Entry)
  #   __is_valid()  (DieGUI)
  #   __str__() (DieMultiSided)
  #   increment_number_created() (DiceGUI)
  #   all_dice_have_been_created() (DiceGUI)
  #   enable_roll_buttons() (DiceGUI)
  def create_die(self, event):
    # 14. Get number of sides on die string from entry box
    num_sides = self.entry_sides.get()
    try:
      # 15. Check for invalid entry (e.g.,number of sides str isn't all digits, etc.)
      if not(num_sides.isdigit() and int(num_sides) > 0):
        # and if so, Raise BadArgument exception
        raise BadArgument()
      # Otherwise:
      # 16. Create model and disable entry box
      else:
        self.__die = DieMultiSided(int(num_sides))
        self.entry_sides.config(state = 'disable')

      # 17. Let parent know that another die has been created
      self.__parent.all_dice_have_been_created()
      
      # 18. Have parent enable all roll buttons if all dice have been created
      if self.__parent.all_dice_have_been_created():
        self.__parent.enable_roll_buttons()
      
    # 19. handle invalid entry
    except BadArgument as e:  
      # 18. Warn user, clear entry box
      messagebox.showwarning('Warning', 'Input not valid')
      self.entry_sides.delete(0, END)
        
    
  # Roll die, set value, increment parent's roll counter, disable button
  # Sum rolls if all other dice have been rolled
  # invoke:
  #   roll() (DieMultiSided)
  #   set() (StringVar)
  #   __str__() (DieMultiSided)
  #   config() (Button)
  #   increment_roll_counter() (DiceGUI)
  #   all_dice_have_been_rolled() (DiceGUI)
  #   sum_rolls() (DiceGUI)
  def roll_die(self):
    # 19. Roll the die and set the StringVar with the die value
    self.__die.roll()
    self.roll_value.set(self.__die)

    # 20. Let parent know that die has been rolled and disable roll button
    self.__parent.all_dice_have_been_rolled()
    self.__parent.increment_roll_counter()
    self.roll_button.config(state = 'disabled')

    # 21. Have parent sum the rolls if all dice have been rolled
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
  # For testing purposes there will only be one die GUI at a time, so as
  #   little code as possible has been written

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


# Write main() tester class to create parent GUIS to exercise one at a time
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

  


  
