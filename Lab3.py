import numpy as np


def solveTransitionMatrix(transitionMatrix):
    tm = transitionMatrix
    print("Transition matrix = \n", transitionMatrix)
    # (T - I).transpose
    transitionMatrix = (transitionMatrix - np.identity(len(transitionMatrix[0]))).T
    # print("(T - I).tr = \n", transitionMatrix)
    transitionMatrix[len(transitionMatrix[0]) - 1] = np.ones(len(transitionMatrix[0]))
    # print("Transition matrix = \n", transitionMatrix)

    res = np.zeros(len(transitionMatrix[0]))
    res[len(transitionMatrix[0]) - 1] = 1
    probabilities = np.linalg.solve(transitionMatrix, res)
    for i in range(len(probabilities)):
        print("Probability of state {} = {}, which is {} hours/year".format(i, probabilities[i], probabilities[i] * 8760))

    # State Transition Frequencies:
    for i in range(len(tm)):
        for j in range(i, len(tm[0])):
            print("State transition frequency from state {} to state {} = {}".format(i, j, tm[i][j] * probabilities[i]))


def makeTransitionMatrix(lam, miu):
    return np.array([[1 - 2 * lam, 2 * lam, 0],
                     [miu, 1 - (miu + lam), lam],
                     [0, 2 * miu, 1 - 2 * miu]])


if __name__ == '__main__':
    # State 0: 2  available
    # State 1: 1 circuit available
    # State 2: 0 circuits available

    # Question 1
    # OHL
    print("\nQuestion 1:\n")
    lam = 0.0022 * 10
    miu = 8760 / 8
    transitionMatrix = makeTransitionMatrix(lam, miu)
    solveTransitionMatrix(transitionMatrix)

    # Question 2
    # UGC
    print("\nQuestion 2:\n")
    lam = 6.37656e-05
    miu = 8760 / 730
    transitionMatrix = makeTransitionMatrix(lam, miu)
    solveTransitionMatrix(transitionMatrix)

    # Question 4
    # Double circuit UGC + spare cable with switching time of 24 hours
    print("\nQuestion 4:\n")
    lam = 6.37656e-05
    miu = 8760 / 730
    miuPrime = 8760 / 24
    transitionMatrix = np.array([[1 - lam, lam, 0, 0, 0, 0],
                                 [miu, 1 - (lam + miu + miuPrime), miuPrime, lam, 0, 0],
                                 [miu, lam, 1 - (lam + miuPrime + lam), 0, lam, miu],
                                 [0, miu, 0, 1 - (miuPrime + miu), miuPrime, 0],
                                 [0, 0, miu, lam, 1 - (miu + lam), 0],
                                 [miuPrime, 0, 0, 0, 0, 1 - miuPrime]])

    solveTransitionMatrix(transitionMatrix)
