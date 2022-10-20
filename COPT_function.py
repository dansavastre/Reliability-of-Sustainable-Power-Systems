
def COPT_function(Cgens,Ugens,P_round):
    # Eduardo Jerez, based on Bart Tuinema's Matlab code
    # COPT calculation
    # COPT = COPT_function(Cgens,Ugens,P_round)
    # Cgens = unit capacities
    # Ugens = Generator unavailabilities (FOR's)
    # P_round = capacities are rounded to this value

    import numpy as np

    Cgens = np.multiply(P_round,np.round(np.divide(Cgens,P_round)))  # round capacities
    P_total = sum(Cgens)  # total capacity
    n_units = len(Cgens)  # number of units

    COPT = np.zeros([np.int_(P_total/P_round), 2])
    COPT[:,0] = range(0,np.int_(P_total),P_round)
    COPT[0,1] = 1
    for i in range(n_units):
        COPT2 = np.multiply(COPT[:,1],Ugens[i])  # COPT when unit i is off
        COPT[:,1] = np.multiply(COPT[:,1],(1-Ugens[i]))  # COPT when unit i is on
        COPT[:,1] = np.add(COPT[:,1], np.hstack([np.zeros([np.int_(Cgens[i]/P_round)]), COPT2[0:-np.int_((Cgens[i]/P_round))]]))    #COPT2 is shifted down by the capacity of the generator

    #COPT = [COPT zeros(size(COPT[0]),1)]    # adding 3rd column
    #COPT(1,3) = 1
    COPT = np.transpose(np.vstack([np.transpose(COPT), np.subtract(1,np.hstack([[0],np.cumsum(COPT[0:-1,1])]))]))

    return COPT
