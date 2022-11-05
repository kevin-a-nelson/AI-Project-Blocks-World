###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State
import copy
import random

AIR = '#'


class Plan:

  def __init__(self, initial_state, goal_state):
    """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
    self.initial_state = initial_state
    self.goal_state = goal_state
    self.visitedStates = []
    self.unvisitedStates = []

  #***=========================================
  # First implement all the operators
  # I implemented two operators to give you guys an example
  # Please implement the remainder of the operators
  #***=========================================

  def putdown(self, block1):
    """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

    # get table object from initial state
    table = State.find(self.initial_state, "table")

    if block1.air:
      block1.on = table
      block1.isclear = True

  def unstack(self, block1, block2):
    """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

    # if block1 is clear safe to unstack
    if block1.isclear:

      # block1 should be in air
      # block1 should not be on block2
      # set block2 to clear (because block1 is in air)
      block1.isclear = False
      block1.air = True
      block1.on = None

      block2.isclear = True

  # ***=========================================
  # After you implement all the operators
  # The next step is to implement the actual plan.
  # Please fill in the sample plan to output the appropriate steps to reach the goal
  # ***=========================================

  def binarySearch(self, arr, val, start, end):
    #print(f"Arr = {arr}")
    #print(f"val = {val}")
    #arr in this case will be a que of (state, H, blockinAir, cmdlist)
    if len(arr) == 0:  #If array has no length.
      return 0

    if start == end:  #If wagreement reached
      if arr[start][1] > val[1]:
        return start
      else:
        return start + 1
    if start > end:
      return start

    mid = int(round((start + end) / 2, 0))
    #print(
    #f"Checking for floats: compare {mid}, in other words the halfway point in the unvisited array's heuristic > {val[1]}, or the herusitc at hand"
    #)
    #Reach agreement
    if arr[mid][1] < val[1]:
      return self.binarySearch(arr, val, mid + 1, end)
    elif arr[mid][1] > val[1]:
      return self.binarySearch(arr, val, start, mid - 1)
    else:
      return mid

  def sample_plan(self):

    # get the specific block objects
    # Then, write code to understand the block i.e., if it is clear (or) on table, etc.
    # Then, write code to perform actions using the operators (pick-up, stack, unstack).

    # Below I manually hardcoded the plan for the current initial and goal state
    # You must automate this code such that it would produce a plan for any initial and goal states.

    SeenStates = []
    steps = 0

    initial_state_copy = copy.deepcopy(self.initial_state)

    SeenStates.append(self.createUniqueStateId(initial_state_copy))
    hueristic_value = self.getHueristicValue(initial_state_copy)
    #(State, Heuristic, BlockInAirID, CommandList(function id id : function id id...))
    cost = 0  #Every action will increase the previous cost
    self.unvisitedStates.append(
      (initial_state_copy, hueristic_value + cost, cost, None,
       ""))  #String tracks the function calls, and ids

    while True:
      tempTup = self.unvisitedStates.pop(0)
      self.visitedStates.append((self.createUniqueStateId(tempTup[0]),
                                 tempTup[4]))  #remove first in unvisited
      #break only when goal state is found (Heur=0)

      alterState = tempTup
      #print("Check state and Tupple")
      #print(investState)
      #self.ShowState(investState[0])

      if (alterState[1] -
          alterState[2] == 0):  #State's heuristic is the goal state!
        print("Success")
        return alterState[4], alterState, steps, self.getHueristicValue(
          alterState
        )  #Return the command list. "" if none were needed, " : delimnator" if some where.

      steps = steps + 1
      #print(
       # f"step {steps}, State H ={alterState[1]-alterState[2]}, Cost G={alterState[3]}, state = {alterState[0]}"
      #)
      #self.ShowState(alterState[0])

      tempCost = alterState[2] + 1
      #Table id table, on none, isclear false, air false.
      moveAmt = 1
      if (alterState[3] != None):
        #In air! alterState[2] holds the ID of the block to investigate
        for block in alterState[0]:
          if (block.isclear or block.id == 'table'):
            for i in range(moveAmt):
              self.move2(
                alterState[3] #Note be sure to skip blocks that make no sense
              )  #basically it'll print to the extent we have stacks, so 1 for one stack (because table exists), two for 2 stacks (again table exists).
            moveAmt += 1

          if block.isclear and block.on!=None:
            if block.type == 1:
              #print("into state stack2")
              #self.ShowState(alterState[0])

              temp = self.stack2(alterState[3], block.id,
                                 copy.deepcopy(alterState[0]))
              #deepcopy state, with command stack, id, id,

              tempTup = (temp, self.getHueristicValue(temp) + tempCost,
                         tempCost, None,
                         alterState[4] + f":stack {alterState[3]} {block.id}")
              if ((self.createUniqueStateId(
                  tempTup[0]), tempTup[4]) not in self.visitedStates
                  and tempTup not in self.unvisitedStates):
                self.unvisitedStates.insert(
                  self.binarySearch(self.unvisitedStates, tempTup, 0,
                                    len(self.unvisitedStates) - 1), tempTup)
              #insert (deep state, H(deep state), None, alterstate[3]+":stack id id")

            elif block.type == 3 and block.on!=None:
              temp = self.putdown2(alterState[3], copy.deepcopy(alterState[0]))
              #deepcopy state, with command stack, id, id,
              tempTup = (temp, self.getHueristicValue(temp) + tempCost,
                         tempCost, None,
                         alterState[4] + f":putdown {alterState[3]}")
              if ((self.createUniqueStateId(
                  tempTup[0]), tempTup[4]) not in self.visitedStates
                  and tempTup not in self.unvisitedStates):
                self.unvisitedStates.insert(
                  self.binarySearch(self.unvisitedStates, tempTup, 0,
                                    len(self.unvisitedStates) - 1), tempTup)
              #insert ... ... ... alterstate[3]+":putdown id"
              continue
        moveAmt = 1

      else:  #Note optimize by making temp at the start instead of four locations. Also note optimize by changing binary back to just array vs value, isntead of self.unvisited vs tupple.
        #No block in the air.
        for block in alterState[0]:
          if block.id != "table"  and block.on!=None and block.on.id == "table" and block.isclear:
            #pickup
            temp = self.pickup2(block.id, copy.deepcopy(alterState[0]))
            tempTup = (temp, self.getHueristicValue(temp) + tempCost, tempCost,
                       block.id, alterState[4] + f":pickup {block.id}")
            if ((self.createUniqueStateId(
                tempTup[0]), tempTup[4]) not in self.visitedStates
                and tempTup not in self.unvisitedStates):
              self.unvisitedStates.insert(
                self.binarySearch(self.unvisitedStates, tempTup, 0,
                                  len(self.unvisitedStates) - 1), tempTup)

          else:
            #unstack
            if (block.id != 'table' and block.isclear and  
                block.on!=None and block.on.id != 'table'):
              temp = self.unstack2(block, block.on,
                                   copy.deepcopy(alterState[0]))
              tempTup = (temp, self.getHueristicValue(temp) + tempCost,
                         tempCost, block.id,
                         alterState[4] + f":unstack {block.id} {block.on}")
              if ((self.createUniqueStateId(
                  tempTup[0]), tempTup[4]) not in self.visitedStates
                  and tempTup not in self.unvisitedStates):
                self.unvisitedStates.insert(
                  self.binarySearch(self.unvisitedStates, tempTup, 0,
                                    len(self.unvisitedStates) - 1), tempTup)

        #For block in state, if block.on != 'table', unstack
        #Else pickup

        continue

      #Check blocks in init mathc blocks in goal so we don't have oddness
      #Check goal is a legal solution (So if we end up not finding the tree, but having no more states to visit)
      #Check that iniial is not alreayd the goal

      #BestState=unvisited.pop(0)
      #Insert states to unvisited by binary search in the que, using second tupple value
      #Display state (for bug testing)
      #ConsiderAll
      #For every true return of function, generate unique state ID
      #IF unique state ID NOT in SeenStates (List that includes visited and unvisited)
      #append to unvisited states tupple
      #Otherwise ignore. If it's in SeenStates, that means theres a cheaper state that has the oreintation because we append for each true attempt from the start - can check herusitic and replace it if it's lower I guess

  #Unique Identifier for Cylcing

  def createUniqueBlockId(self, block):
    return f"{block.type}{block.id}{block.on}{block.isclear}{block.air}"

  def createUniqueStateId(self, state):
    formationId = ""
    for block in state:
      formationId += self.createUniqueBlockId(block)

    return formationId

  #End of Unique Identifiers for Cycling

  #Begin Matrix Heuristic Functions

  def getHueristicValue(self, state):
    # creates blocks world as 2D array
    #Seems the state matrix might be 7 by 8 instead of expected 7 by 7.... Bottom row is 'table''s, is this intentional from Kevins oriinal code?
    stateMatrix = self.stateToMatrix(state)

    #Besides the table row in the resulting matrix, the values and amountof values we get is as expected.
    # 2D array representing the H value of each block
    hueristicValuesMatrix = self.getHueristicValuesMatrix(stateMatrix, state)

    # Sum of the H values of all blocks/ Is MatrixSum to blame?
    hueristicValue = self.matrixSum(hueristicValuesMatrix)
    return hueristicValue

  def stateToMatrix(self, state):

    matrix = self.createEmptyMatrix(state)
    #print("OK")
    copyState = copy.deepcopy(state)
    copyState = self.removeBlock(
      copyState, "table")  #does not properly remove the block from copyState.
    #print(f"Check if saved {copyState}")
    #print("OK")
    startCol = 0
    endCol = len(matrix[0])
    currentRow = len(matrix)
    while copyState and currentRow > 0:
      currentRow -= 1
      for i in range(startCol, endCol):
        for block in copyState:
          # current block is not on the block below
          if block.on == None:  #weird error happening.
            continue
          if block.on.id != matrix[currentRow][i]:
            continue

          if matrix[currentRow - 1][i] != AIR:
            continue

          matrix[currentRow - 1][i] = block.id
          self.removeBlock(copyState, block.id)

    return matrix

  def removeBlock(self, state, blockToRemove):
    for idx, block in enumerate(state):
      if block.id == blockToRemove:
        del state[idx]
    return state

  def getHueristicValuesMatrix(self, stateMatrix, state):

    # goal state as 2D array
    goalMatrix = self.stateToMatrix(self.goal_state)

    # initilize H matrix
    hueristicMatrix = self.createEmptyMatrix(self.goal_state)

    maxRow = len(goalMatrix) - 1
    minRow = 0

    maxCol = len(goalMatrix[0])
    minCol = 0

    for col in range(minCol, maxCol):
      for row in range(maxRow, minRow - 1, -1):

        # Tables have a value of 0
        if stateMatrix[row][col] == "table":
          hueristicMatrix[row][col] = 0
          continue

        # Air has a value of 0
        elif stateMatrix[row][col] == AIR:
          hueristicMatrix[row][col] = 0
          continue

        if stateMatrix[row][col] != goalMatrix[row][col]:
          if (State.find(state, stateMatrix[row][col]).air == True):  #inserted
            hueristicMatrix[row][col] = 1
          else:  #Original
            hueristicMatrix[row][
              col] = 2  #additionally we could add another cost if it's not clear.
            #Note, increasing penaltiies will likely give us better runtimes.
        else:
          hueristicMatrix[row][col] = 0

    return hueristicMatrix

  def createEmptyMatrix(self, state):
    numberOfBlocks = len(state) - 1

    matrix = [[AIR for x in range(numberOfBlocks)]
              for y in range(numberOfBlocks)]

    tableRow = ["table"] * len(matrix)

    matrix.append(tableRow)

    return matrix

  def matrixSum(self, matrix):
    sum = 0
    for row in matrix:
      for col in row:
        sum += col
    return sum

  #End of Matrix Heuristic Functions

  #Movement types
  def putdown2(self, block1, state="default"):
    """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """
    if state == "default":
      table = State.find(self.initial_state, "table")
    # get table object from initial state
    else:
      #print(state)
      #self.ShowState(state)
      table = State.find(state, "table")
      blockObj1 = State.find(state, block1)

    if blockObj1.air:
      blockObj1.on = table
      blockObj1.isclear = True
      blockObj1.air = False  #added.
    return state

  def stack2(self, block1, block2, state):
    """
      Operator to stack block 1 onto block 2
      
        :param block1: block1 to stack onto block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: True if operation successful, False otherwise
    """
    #print("Inside stack state")
    #self.ShowState(state)
    BlockObj1 = State.find(state, block1)
    BlockObj2 = State.find(state, block2)
    if BlockObj1.air and BlockObj2.isclear and BlockObj2.type == 1:
      BlockObj1.isclear = True
      BlockObj2.isclear = False
      BlockObj1.on = BlockObj2
      BlockObj1.air = False
      #print("return stack state")
      #self.ShowState(state)
      return state
    print(
      f"Error 2 : block1{block1}{BlockObj1.air}, block2{block2}{BlockObj2.isclear}{BlockObj2.type}"
    )
    n = 1
    return False

  def move2(self, block1):
    #once per putdown, once per stack, up to the number of stacks iterations. (So we need a counter)
    return

  def unstack2(self, block1, block2, state):
    """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """
    BlockObj1 = State.find(state, block1.id)
    BlockObj2 = State.find(state, block2.id)

    # if block1 is clear safe to unstack
    if BlockObj1.isclear:
      # block1 should be in air
      # block1 should not be on block2
      # set block2 to clear (because block1 is in air)
      BlockObj1.isclear = False
      BlockObj1.air = True
      BlockObj1.on = None
      BlockObj2.isclear = True
      return state

  def pickup2(self, block1, state):
    """
      Operator to pickup block1 from table
      
      :param block1: block1 pickup from table
      :type block1: Object of block.Block
      :return: True if operation successful, False otherwise
    """
    BlockObj1 = State.find(state, block1)

    if BlockObj1.on.id == "table" and BlockObj1.isclear and not BlockObj1.air:
      BlockObj1.air = True
      BlockObj1.isclear = False
      BlockObj1.on = None
      return state  #Was all deepcopies, but pasisng in deepcopies already.
    print("Error")
    return False

  def ShowState(self, state):
    for item in state:
      print(
        f"{item} {item.id} On:{item.on} Clear:{item.isclear} Air:{item.air}")


if __name__ == "__main__":

  # get the initial state
  initial_state = State()
  initial_state_blocks = initial_state.create_state_from_file("C:/Users/thebl/OneDrive/Desktop/project 1/starter code/input.txt")

  #display initial state
  State.display(initial_state_blocks, message="Initial State")

  # get the goal state
  goal_state = State()
  goal_state_blocks = goal_state.create_state_from_file("C:/Users/thebl/OneDrive/Desktop/project 1/starter code/goal.txt")

  #display goal state
  State.display(goal_state_blocks, message="Goal State")
  """
    Sample Plan
    """

  p = Plan(initial_state_blocks, goal_state_blocks)
  instructions, stateTup, steps, heuristic = p.sample_plan()
  print(
    f"We recommend plan - {instructions}\n State Tup is {stateTup}\n Number of steps = {steps}\n Heuristic = {heuristic}"
  )
