
def printHueristicValuesOfBlocks(state):
    # get all possible next states
    nextPossibleStates = self.getNextPossibleStates(state)

    # creates blocks world as 2D array
    stateMatrix = self.stateToMatrix(state)

    # 2D array representing the H value of each block
    hueristicValuesMatrix = self.getHueristicValuesMatrix(stateMatrix)
    print("---")
    print("Hueristic Value of each block")
    print("---")
    self.prettyPrintMatrix(hueristicValuesMatrix)
    print("\n")
