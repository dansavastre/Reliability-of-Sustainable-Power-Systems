def get_P_lines_MVL_func(B_matrix, Y_lines, C_lines, bus_loads):
    # P_lines = get_P_lines(B_matrix, Y_lines, C_lines, generations, exports, loads)
    # gives the values of P_lines given the input values, MVL-network
    #
    # Input:
    # B_matrix = B_matrix for the DC load flow
    # Y_lines = line admittances
    # C_lines = line capacities
    # bus_loads = loadings of the system buses (load-generation)
    #
    # Output:
    # P_lines = the power flows through the lines (in # of the line capacities)

    import numpy as np

    angles = np.hstack([0, np.linalg.solve(B_matrix, (np.multiply(0.01, (bus_loads[1:len(bus_loads)]))))])

    P_lines = np.multiply(100, [np.sin(angles[1] - angles[0]) * np.imag(Y_lines[0]),
                                np.sin(angles[1] - angles[0]) * np.imag(Y_lines[1]),
                                np.sin(angles[2] - angles[1]) * np.imag(Y_lines[2]),
                                np.sin(angles[2] - angles[1]) * np.imag(Y_lines[3]),
                                np.sin(angles[3] - angles[2]) * np.imag(Y_lines[4]),
                                np.sin(angles[3] - angles[2]) * np.imag(Y_lines[5]),
                                np.sin(angles[5] - angles[3]) * np.imag(Y_lines[6]),
                                np.sin(angles[5] - angles[3]) * np.imag(Y_lines[7]),
                                np.sin(angles[4] - angles[0]) * np.imag(Y_lines[8]),
                                np.sin(angles[4] - angles[0]) * np.imag(Y_lines[9]),
                                np.sin(angles[5] - angles[4]) * np.imag(Y_lines[10]),
                                np.sin(angles[5] - angles[4]) * np.imag(Y_lines[11])])

    P_lines = np.multiply(100, np.abs(np.divide(P_lines, C_lines)))

    return P_lines
