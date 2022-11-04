# =================================================
# git clone https://github.com/kevin-a-nelson/AI-Project-Blocks-World.git
# cd starter\ code
# python3 main.py
# =================================================

import random
from state import State
import copy

AIR = '#'


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
        self.visitedStates = []

    # ***=========================================
    # First implement all the operators
    # I implemented two operators to give you guys an example
    # Please implement the remainder of the operators
    # ***=========================================

    def createUniqueBlockId(self, block):
        return f"{block.type}{block.id}{block.on}{block.clear}"

    def createUniqueStateId(self, state):
        formationId = ""
        for block in state:
            formationId += self.createUniqueBlockId(block)

        return formationId

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

    def putdown(self, block1, block2):
        block1.on.isclear = True
        block1.on = block2
        block1.isclear = True
        return f"putdown({block1.id}, {block2.id})"

    def stack(self, block1, block2):
        block1.on.isclear = True
        block1.on = block2
        block1.isclear = True
        block2.isclear = False
        return f"upstack({block1.id}, {block2.id})"

    def moveBlocks(self, block1, block2):

        # block1 cannot be move if it has a block on top
        if not block1.isclear:
            return

        # if block2 is table, stack block1 on table
        if block2.id == "table":
            self.putdown(block1, block2)
            return f"putdown({block1.id}, {block2.id})"

        # block2 cannot have a block stacked on top of it if it already has a block ontop
        if not block2.isclear:
            return

        # stack block1 on block2
        self.stack(block1, block2)
        return f"stack({block1.id}, {block2.id})"

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
            possibleState["state"], clearBlock1.id)

        # get block2
        copyClearBlock2 = self.getBlockWithId(
            possibleState["state"], clearBlock2.id)

        # stack block1 on block2
        move = self.moveBlocks(copyClearBlock1, copyClearBlock2)

        return possibleState, move

    def sortStatesByTheirHvalues(self, hi):
        pass

    def getNextPossibleStates(self, state):

        # To go to a next possible state
        # You move a clear block onto another clear block
        clearBlocks = self.getClearBlocks(state["state"])

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
                possibleNextState, move = self.stackBlockOneOnBlockTwo(
                    clearBlock1, clearBlock2, state)

                uniqueStateId = self.createUniqueStateId(
                    possibleNextState["state"])

                # Add state to possible states if it is not visited
                if uniqueStateId in self.visitedStates:
                    continue

                self.visitedStates.append(uniqueStateId)

                path = copy.deepcopy(state["path"])
                moves = copy.deepcopy(state["moves"])
                moves.append(move)

                path.append(possibleNextState["state"])

                possibleNextState["path"] = path
                possibleNextState["moves"] = moves

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
        while copyState and currentRow > 0:
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
            for row in range(maxRow, minRow - 1, -1):

                # Tables have a value of 0
                if state[row][col] == "table":
                    hueristicMatrix[row][col] = 0
                    continue

                # Air has a value of 0
                elif state[row][col] == AIR:
                    hueristicMatrix[row][col] = 0
                    continue

                if state[row][col] != goal[row][col]:
                    hueristicMatrix[row][col] = 1
                else:
                    hueristicMatrix[row][col] = 0

        return hueristicMatrix

    def matrixSum(self, matrix):
        sum = 0
        for row in matrix:
            for col in row:
                sum += col
        return sum

    def getHueristicValue(self, state):
        # creates blocks world as 2D array
        stateMatrix = self.stateToMatrix(state)

        # 2D array representing the H value of each block
        hueristicValuesMatrix = self.getHueristicValuesMatrix(stateMatrix)

        # Sum of the H values of all blocks
        hueristicValue = self.matrixSum(hueristicValuesMatrix)

        return hueristicValue

    # Function to sort the list by second item of tuple
    def sortTupleBySecondElement(self, tuple):

        # reverse = None (Sorts in Ascending order)
        # key is set to sort using second element of
        # sublist lambda has been used
        tuple.sort(key=lambda x: x[1])
        return tuple

    def sample_plan(self):

        # initialize
        initialStateCopy = copy.deepcopy(self.initial_state)
        hueristicValue = self.getHueristicValue(initialStateCopy)

        initialUnvisitedState = {
            "state": initialStateCopy,
            "hueristic": hueristicValue,
            "moves": ["Initial State"],
            "path": [initialStateCopy]
        }

        unvisitedStates = [initialUnvisitedState]
        self.visitedStates.append(initialStateCopy)

        while True:

            # sort states by their hueristic value
            newlist = sorted(
                unvisitedStates, key=lambda state: state['hueristic'])

            # get state with lowest hueristic value
            bestState = unvisitedStates.pop(0)

            # display state

            print(
                f"Hueristic Value: {bestState['hueristic']}\tExplored Unique States so far: {len(self.visitedStates)}")
            # State.display(
            #     bestState["state"], message=f"Hueristic Value: {bestState['hueristic']}\tExplored States: {len(self.visitedStates)}\tPath: {len(bestState['path'])}")

            # get all possible next states
            nextPossibleStates = self.getNextPossibleStates(bestState)

            # loop through all possible next states
            for nextPossibleState in nextPossibleStates:

                # hueristic value of possible state
                hueristicValue = self.getHueristicValue(
                    nextPossibleState["state"])

                # state is goal state
                if hueristicValue == 0:
                    # State.display(
                    #     nextPossibleState["state"], message=f"Goal State Reached!!! Hueristic Value: {hueristicValue}\tExplored States: {len(self.visitedStates)}")
                    # print(f"move: {' -> '.join(nextPossibleState['move'])}")

                    for i in range(len(nextPossibleState["path"])):
                        State.display(
                            nextPossibleState["path"][i], message=nextPossibleState["moves"][i])
                    # for state in nextPossibleState["path"]:
                    #     State.display(state)

                    return

                uniqueStateId = self.createUniqueStateId(
                    nextPossibleState["state"])

                unvisitedStates.append(nextPossibleState)

                # self.visitedStates.append(uniqueStateId)


if __name__ == "__main__":

    # init the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")

    # init the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    p = KevinPlan(initial_state_blocks, goal_state_blocks)

    """
    Sample Plan
    """
    p = KevinPlan(initial_state_blocks, goal_state_blocks)
    p.sample_plan()
