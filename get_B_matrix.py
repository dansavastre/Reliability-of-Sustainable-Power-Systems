def get_B_matrix_NL_func2020_MVL_without_SMH(lines):
    # Bart Tuinema
    # [B_matrix Y_lines C_lines] = get_B_matrix_NL_func2020_MVL(lines)
    # Gives the B_matrix, Y_lines and C_lines for the Dutch high voltage 380kV
    # power system to be used for the DC load flow for the 2020 scenario
    # MVL region only (without SMH)
    #
    # Input:
    # lines = indication which lines are in operation (vector 0/1)
    #
    # Output:
    # B_matrix = B_matrix for the DC load flow
    # Y_lines = line admittances
    #
    # buses:
    #  1 = MVL
    #  2 = WTL
    #  3 = WTR
    #  4 = BWK
    #  5 = CST
    #  6 = KIJ

    # lines:
    # 1-2 = MVL-WTL
    # 3-4 = WTL-WTR
    # 5-6 = WTR-BWK
    # 7-8 = BWK-KIJ
    # 9-10 = MVL-SMH-CST
    # 11-12 = CST-KIJ

    # Vbase = 380e3   # 380 kV
    # Sbase = 100e6   # 100 MVA
    # Zbase = Vbase^2/Sbase   # 1444 Ohm
    # lines = ones(14,1)


    ## Line Impedances
    import numpy as np

    Z_line1 = 0.008918j
    Z_line2 = Z_line1
    Z_line3 = 0.001151j
    Z_line4 = Z_line3
    Z_line5 = 0.002810j
    Z_line6 = Z_line5
    Z_line7 = 0.003131j
    Z_line8 = Z_line7
    Z_line9 = 0.004364j+0.006786j
    Z_line10 = Z_line9
    Z_line11 = 0.002490j
    Z_line12 = Z_line11


    ## Line Admittances

    Y_line1 = 1/Z_line1
    Y_line2 = 1/Z_line2
    Y_line3 = 1/Z_line3
    Y_line4 = 1/Z_line4
    Y_line5 = 1/Z_line5
    Y_line6 = 1/Z_line6
    Y_line7 = 1/Z_line7
    Y_line8 = 1/Z_line8
    Y_line9 = 1/Z_line9
    Y_line10 = 1/Z_line10
    Y_line11 = 1/Z_line11
    Y_line12 = 1/Z_line12
    Y_lines = np.array([Y_line1, Y_line2, Y_line3, Y_line4, Y_line5, Y_line6, Y_line7, Y_line8, Y_line9, Y_line10, Y_line11, Y_line12], dtype="complex_")

    Y_lines = np.multiply(lines,Y_lines)


    ## Y-bus calculation

    Y_bus = np.zeros([6,6], dtype='complex_')

    Y_bus[0,0] = Y_lines[0] + Y_lines[1] + Y_lines[8] + Y_lines[9]
    Y_bus[1,1] = Y_lines[0] + Y_lines[1] + Y_lines[2] + Y_lines[3]
    Y_bus[2,2] = Y_lines[2] + Y_lines[3] + Y_lines[4] + Y_lines[5]
    Y_bus[3,3] = Y_lines[4] + Y_lines[5] + Y_lines[6] + Y_lines[7]
    Y_bus[4,4] = Y_lines[8] + Y_lines[9] + Y_lines[10] + Y_lines[11]
    Y_bus[5,5] = Y_lines[6] + Y_lines[7] + Y_lines[10] + Y_lines[11]

    Y_bus[0,1] = -(Y_lines[0] + Y_lines[1])
    Y_bus[1,0] = Y_bus[0,1]
    Y_bus[1,2] = -(Y_lines[2] + Y_lines[3])
    Y_bus[2,1] = Y_bus[1,2]
    Y_bus[2,3] = -(Y_lines[4] + Y_lines[5])
    Y_bus[3,2] = Y_bus[2,3]
    Y_bus[3,5] = -(Y_lines[6] + Y_lines[7])
    Y_bus[5,3] = Y_bus[3,5]
    Y_bus[0,4] = -(Y_lines[8] + Y_lines[9])
    Y_bus[4,0] = Y_bus[0,4]
    Y_bus[4,5] = -(Y_lines[10] + Y_lines[11])
    Y_bus[5,4] = Y_bus[4,5]


    ## B'-matrix calculation

    B_matrix = np.multiply(-1,np.imag(Y_bus[1:6,1:6]))

    return B_matrix, Y_lines
