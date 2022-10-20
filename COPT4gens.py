# Eduardo Jerez, based on Bart Tuinema's Matlab version
# 4-Generator example generation adequacy
import numpy as np
import math

def COPT():
    # initial values
    Cgens = [200, 100, 200, 500]
    Ugens = [0.05, 0.03, 0.04, 0.06]

    COPT = np.zeros([np.int_(sum(Cgens)/100+1),3])
    COPT[:,0] = range(0,np.int_(sum(Cgens)+100),100)
    Agens = np.subtract([1,1,1,1],Ugens)
    A_allgens = math.prod(Agens)


    ## 0th-order
    COPT[0,1] = A_allgens


    ## 1st-order
    for i in range(4):
        Pstate = Ugens[i]*A_allgens/Agens[i]
        COPT[np.int_(Cgens[i]/100),1] = COPT[np.int_(Cgens[i]/100),2] + Pstate


    ## 2nd-order
    for i in range(3):
        for j in range(i,4):
            Pstate = Ugens[i]*Ugens[j]*A_allgens/(Agens[i]*Agens[j])
            COPT[np.int_((Cgens[i] + Cgens[j])/100),1] = COPT[np.int_((Cgens[i] + Cgens[j])/100),2] + Pstate


    ## 3rd-order
    for i in range(2):
        for j in range(i,3):
            for k in range(i,4):
                Pstate = Ugens[i]*Ugens[j]*Ugens[k]*A_allgens/(Agens[i]*Agens[j]*Agens[k])
                COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k])/100),1] = COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k])/100),1] + Pstate


    ## 4th-order
    Pstate = np.prod(Ugens)
    COPT[np.int_(sum(Cgens)/100),1] = COPT[np.int_(sum(Cgens)/100),1] + Pstate


    ## results

    COPT[0,2] = 1

    for i in range(np.int_(sum(Cgens)/100+1)):
        COPT[i,2] = 1-sum(COPT[0:i,1])

    return COPT


def COPT2():
    # initial values
    Cgens = [200, 100, 200, 500, 400]
    Ugens = [0.05, 0.03, 0.04, 0.06, 0.05]

    COPT = np.zeros([np.int_(sum(Cgens)/100+1),3])
    COPT[:, 0] = range(0,np.int_(sum(Cgens)+100),100)
    Agens = np.subtract([1, 1, 1, 1, 1], Ugens)
    A_allgens = math.prod(Agens)


    ## 0th-order
    COPT[0,1] = A_allgens


    ## 1st-order
    for i in range(5):
        Pstate = Ugens[i]*A_allgens/Agens[i]
        COPT[np.int_(Cgens[i]/100),1] = COPT[np.int_(Cgens[i]/100),2] + Pstate


    ## 2nd-order
    for i in range(4):
        for j in range(i,5):
            Pstate = Ugens[i]*Ugens[j]*A_allgens/(Agens[i]*Agens[j])
            COPT[np.int_((Cgens[i] + Cgens[j])/100),1] = COPT[np.int_((Cgens[i] + Cgens[j])/100),2] + Pstate


    ## 3rd-order
    for i in range(3):
        for j in range(i,4):
            for k in range(i,5):
                Pstate = Ugens[i]*Ugens[j]*Ugens[k]*A_allgens/(Agens[i]*Agens[j]*Agens[k])
                COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k])/100),1] = COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k])/100),1] + Pstate


    ## 4th-order
    for i in range(2):
        for j in range(i,3):
            for k in range(i,4):
                for l in range(i,5):
                    Pstate = Ugens[i]*Ugens[j]*Ugens[k]*Ugens[l]*A_allgens/(Agens[i]*Agens[j]*Agens[k]*Agens[l])
                    COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k] + Cgens[l])/100),1] = COPT[np.int_((Cgens[i] + Cgens[j] + Cgens[k] + Cgens[l])/100),1] + Pstate

    ## 5th-order
    Pstate = np.prod(Ugens)
    COPT[np.int_(sum(Cgens)/100),1] = COPT[np.int_(sum(Cgens)/100),1] + Pstate


    ## results

    COPT[0,2] = 1

    for i in range(np.int_(sum(Cgens)/100+1)):
        COPT[i,2] = 1-sum(COPT[0:i,1])

    return COPT
