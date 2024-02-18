import scipy.linalg as sla #nla
import scipy.interpolate as spi #nla2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def spline (input_path):

    # BUILDING X AND Y
    X = np.array([], float)
    Y = np.array([], float)
    with open(input_path, 'r', newline='') as input_file:
        reader = csv.reader(input_file, delimiter=',')
        next(reader)
        for row in reader :
            X = np.append(X, float(row[2]))
            Y = np.append(Y, float(row[4]))

    # BUILDING FROM PANDAS WITH GENERIC X AND Y COLUMNS

    size = np.size(X) - 1  # Size of X - 1

    # Sorting X and Y :
    X = X[X.argsort()]
    Y = Y[X.argsort()]

    # Check for non-zero H :
    # Increase consecutive X[i] if they are equals.
    for i in range(0, size):
        if X[i] == X[i + 1]:
            j = 1
            while X[i] == X[i + j] :
                j += 1
            for k in range(1, j + 1):
                X[i + k] = X[i] + k * 0.1 / (j + 1)

    # Default
    p = 29.0

    # BUILDING SIGMA
    Sigma = np.eye(size + 1)
    Sigma2 = np.dot(Sigma, Sigma) # ??????? Equal to Sigma

    # BUILDING H AND G
    H = np.zeros(size)
    G = np.zeros(size)
    for i in range(0, size):
        H[i] = X[i + 1] - X[i]
        G[i] = 1 / H[i]

    # BUILDING T
    T = np.zeros((size - 1, size - 1))

    T[0, 0] = 1 / 3 * (2 * (H[0] + H[1]))
    T[1, 0] = 1 / 3 * H[1]
    T[size - 2, size - 2] = (1 / 3) * (2 * (H[size - 2] + H[size - 1]))
    T[size - 3, size - 2] = 1 / 3 * H[size - 2]
    for i in range(1, size - 2):
        T[i - 1, i] = 1 / 3 * H[i]
        T[i, i] = 1 / 3 * (2 * (H[i] + H[i + 1]))
        T[i + 1, i] = 1 / 3 * H[i + 1]

    # BUILDING Q
    Q = np.zeros((size + 1, size - 1))
    for i in range(0, size - 1):
        Q[i, i] = G[i]
        Q[i + 1, i] = -G[i] - G[i + 1]
        Q[i + 2, i] = G[i + 1]

    # CALCULATING PARAMETERS:

    # CALCULATING c
    A = np.dot(np.dot(Q.T, Sigma2), Q) + p * T
    b = p * np.dot(Q.T, Y)

    # Cholesky solution:
    L = np.linalg.cholesky(np.dot(np.dot(Q.T, Sigma), Q) + p * T)

    yy = sla.solve_triangular(L, b, trans=0, lower=True)
    c = sla.solve_triangular(L, yy, trans=1, lower=True)

    # Determining c_force
    c_force = np.concatenate(([0], c, [0]), axis=0)

    # CALCULATING d
    d = np.zeros(size, float)

    for i in range(0, size):
        d[i] = (c_force[i + 1] - c_force[i]) / (3 * H[i])

    # CALCULATING a
    a = Y - (1.0 / p) * np.dot(np.dot(np.dot(Sigma, Sigma), Q), c)

    # CALCULATING b
    b = np.zeros(size, float)

    for i in range(0, size):
        b[i] = ((a[i + 1] - a[i]) / H[i]) - (c_force[i] * H[i]) - (d[i] * (H[i] * H[i]))


    # CALCULATING DEGREE OF FREEDOM
    Sp = np.zeros((size + 1, size + 1))
    I = np.eye(size + 1)
    Sp = I - np.dot(Sigma2, np.dot(Q, np.dot(np.linalg.inv(A), Q.T)))
    df = np.trace(Sp)

    # PLOTTING GRAPH

    # Plotting points X and Y
    plt.plot(X, Y, 'r.')

    # Plotting spline segments + CALCULATING OPTIMAL PARAMETER
    sum_squared_error = 0
    for i in range(0, size):
        xnew = np.linspace(X[i], X[i] + H[i], 50)
        ynew = a[i] + b[i] * (xnew - X[i]) + c_force[i] * (xnew - X[i]) ** 2 + d[i] * (xnew - X[i]) ** 3
        sum_squared_error += ((Y[i] - ynew[0]) / (1 - Sp[i, i])) ** 2
        plt.plot(xnew, ynew, "-b")

    sum_squared_error += ((Y[size] - ynew[49]) / (1 - Sp[size, size])) ** 2

    # DISPLAYING CALCULATED PARAMETERS
    print("Optimal degree of freedom: ", df)
    print("Optimal parameter value: ", sum_squared_error)

    # DISPLAYING THE GRAPH
    plt.xlabel("age")
    plt.ylabel("spnbmd")
    plt.title("Smoothing Spline")
    plt.savefig('Output/smoothing_spline.png')
    plt.show()

if __name__ == "__main__" :
    input_path = 'Dataset/spnbmd.csv'
    X_column = 'age'
    Y_column = 'spnbmd'
    spline_parameters = dict()
    spline(input_path)
