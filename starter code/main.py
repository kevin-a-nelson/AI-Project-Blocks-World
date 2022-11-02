# =================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
# =================================================

import random
from state import State
import copy

AIR = ''


class KevinPlan:

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

    # ***=========================================
    # First implement all the operators
    # I implemented two operators to give you guys an example
    # Please implement the remainder of the operators
    # ***=========================================

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
            block1.clear = True

    def stack(self, block1, block2):

        # block1 cannot be move if it has a block on top
        if not block1.isclear:
            return

        # if block2 is table, stack block1 on table
        if block2.id == "table":
            block1.on.isclear = True
            block1.on = block2
            block1.isclear = True
            return

        # block2 cannot have a block stacked on top of it if it already has a block ontop
        if not block2.isclear:
            return

        # stack block1 on block2
        block1.on.isclear = True
        block1.on = block2
        block1.isclear = True
        block2.isclear = False

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

    def getClearBlocks(self, state):
        # return blocks that are clear
        clearBlocks = []
        for block in state:
            if block.isclear and block.on:
                clearBlocks.append(block)
            if block.id == "table":
                clearBlocks.append(block)
        return clearBlocks

    # return block with given id
    def getBlockWithId(self, blocks, id):
        for block in blocks:
            if block.id == id:
                return block

    def stackBlockOneOnBlockTwo(self, clearBlock1, clearBlock2, state):

        # if the original state is modified, we can't get all possible states from it so we have to copy
        possibleState = copy.deepcopy(state)

        # get block1
        copyClearBlock1 = self.getBlockWithId(
            possibleState, clearBlock1.id)

        # get block2
        copyClearBlock2 = self.getBlockWithId(
            possibleState, clearBlock2.id)

        # stack block1 on block2
        self.stack(copyClearBlock1, copyClearBlock2)

        return possibleState

    def getNextPossibleStates(self, state):

        # To go to a next possible state
        # You move a clear block onto another clear block
        clearBlocks = self.getClearBlocks(state)

        possibleNextStates = []

        # stack clear blocks ontop of each other
        for clearBlock1 in clearBlocks:
            for clearBlock2 in clearBlocks:
                # Don't stack a table on another block
                if clearBlock1.id == "table":
                    continue

                # Don't stack a block on itself
                if clearBlock1.id == clearBlock2.id:
                    continue

                # get a possible state where block1 is stacked on block2
                possibleNextState = self.stackBlockOneOnBlockTwo(
                    clearBlock1, clearBlock2, state)

                # add possible state to all possible states
                possibleNextStates.append(possibleNextState)

        return possibleNextStates

    def createEmptyMatrix(self, state):
        numberOfBlocks = len(state) - 1

        matrix = [[AIR for x in range(numberOfBlocks)]
                  for y in range(numberOfBlocks)]

        tableRow = ["table"] * len(matrix)

        matrix.append(tableRow)

        return matrix

    def prettyPrintMatrix(self, matrix):

        for idx, row in enumerate(matrix):
            if idx == len(matrix) - 1:
                break
            print("\n")
            for col in row:
                print(col, end="\t")

    def removeBlock(self, state, blockToRemove):
        for idx, block in enumerate(state):
            if block.id != blockToRemove:
                continue
            del state[idx]

    def stateToMatrix(self, state):

        matrix = self.createEmptyMatrix(state)
        copyState = copy.deepcopy(state)
        self.removeBlock(copyState, "table")

        startCol = 0
        endCol = len(matrix[0])
        currentRow = len(matrix)
        while copyState:
            currentRow -= 1
            for i in range(startCol, endCol):
                for block in copyState:
                    # current block is not on the block below
                    if block.on.id != matrix[currentRow][i]:
                        continue

                    if matrix[currentRow - 1][i] != AIR:
                        continue

                    matrix[currentRow - 1][i] = block.id
                    self.removeBlock(copyState, block.id)

        return matrix

    def blocksAreEqual(self, block1, block2):
        if block1.type != block2.type:
            return False

    def getHueristicValuesMatrix(self, state):

        # goal state as 2D array
        goal = self.stateToMatrix(self.goal_state)

        # initilize H matrix
        hueristicMatrix = self.createEmptyMatrix(self.goal_state)

        maxRow = len(goal) - 1
        minRow = 0

        maxCol = len(goal[0])
        minCol = 0

        for col in range(minCol, maxCol):
            minValueForBlocksInThisColumn = 0
            for row in range(maxRow, minRow - 1, -1):
                # Tables have a value of 0
                if state[row][col] == "table":
                    hueristicMatrix[row][col] = 0
                    continue
                # Air has a value of 0
                elif state[row][col] == AIR:
                    hueristicMatrix[row][col] = 0
                    continue

                # Condition
                # 1. Block is in the right place
                # 2. Block below it isn't
                #
                # Cost
                # This block and all blocks above it get a H value of 4
                elif state[row][col] == goal[row][col] and state[row + 1][col] != goal[row + 1][col]:
                    minValueForBlocksInThisColumn = 4

                # Condition
                # 1. Block is not in the right place
                #
                # Cost
                # This block and all blocks above it get a H value of atleast 2
                elif state[row][col] != goal[row][col]:
                    minValueForBlocksInThisColumn = max(
                        minValueForBlocksInThisColumn, 2)

                hueristicMatrix[row][col] = minValueForBlocksInThisColumn

        return hueristicMatrix

    def matrixSum(self, matrix):
        sum = 0
        for row in matrix:
            for col in row:
                sum += col
        return sum

    def prettyPrintState(self, state):
        self.prettyPrintMatrix(self.stateToMatrix(state))

    def getHueristicValue(self, state):
        # creates blocks world as 2D array
        stateMatrix = self.stateToMatrix(state)

        # 2D array representing the H value of each block
        hueristicValuesMatrix = self.getHueristicValuesMatrix(stateMatrix)

        # Sum of the H values of all blocks
        hueristicValue = self.matrixSum(hueristicValuesMatrix)

        return hueristicValue

    def printStateInfo(self, state, steps):
        hueristicValues = self.getHueristicValuesMatrix(
            self.stateToMatrix(state))
        hueristicValue = self.matrixSum(hueristicValues)
        print("\n\n==== NEXT BEST STATE ====\n")
        State.display(state, f"Step: {steps}\tH Value:{hueristicValue}")
        print("\n\n-------- H Values ---------")
        self.prettyPrintMatrix(hueristicValues)

    def printAnswer(self, state, steps, hueristicValue):
        print("\n\n===== GOAL STATE REACHED ====")
        State.display(state, f"Step: {steps}\tH Value:{hueristicValue}")
        print("\n\n-------- H Values ---------")
        hueristicValues = self.getHueristicValuesMatrix(
            self.stateToMatrix(state))
        self.prettyPrintMatrix(hueristicValues)
        print("\n")

    def sample_plan(self):

        minHueristicValue = float('inf')

        initialStateCopy = copy.deepcopy(self.initial_state)
        nextEquallyBestStates = [initialStateCopy]

        steps = 0

        while True:

            # select random state amongst states with equal hueristic values
            randomIdx = random.randint(0, len(nextEquallyBestStates) - 1)
            nextBestState = nextEquallyBestStates[randomIdx]

            self.printStateInfo(nextBestState, steps)

            # all possible states which are one move away
            nextPossibleStates = self.getNextPossibleStates(nextBestState)

            for nextPossibleState in nextPossibleStates:
                # hueristic value of possible state
                hueristicValue = self.getHueristicValue(nextPossibleState)

                # state is goal state
                if hueristicValue == 0:
                    self.printAnswer(nextPossibleState, steps, hueristicValue)
                    return

                # state is closer to goal state
                if hueristicValue < minHueristicValue:
                    minHueristicValue = hueristicValue
                    nextEquallyBestStates = [nextPossibleState]

                # state is equal to current best state
                elif hueristicValue == minHueristicValue:
                    nextEquallyBestStates.append(nextPossibleState)

            # A block is moved
            steps += 1


if __name__ == "__main__":

    # init the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")

    # init the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    """
    Sample Plan
    """
    p = KevinPlan(initial_state_blocks, goal_state_blocks)
    p.sample_plan()
