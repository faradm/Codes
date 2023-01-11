import numpy as np
import math
import sys
from matplotlib import pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

def algorithm1(M, Delta, eta, P, B, d):

    V = np.zeros(M)
    V[0] = 1
    delta = math.inf

    while delta >= Delta:
        V_prime =   np.copy(V)
        for i in range(P-B-1):
            V_T = np.zeros(M)
            V_T[0:d] = (1-eta)*V[0:d]
            V_T[d:] = (1-eta)*V[d:] + eta*V[0:M-d]
            V = V_T

        for i in range(P-B, P):
            V_T = np.zeros(M)
            V_T[0] = (1-eta)*(V[0] + V[1])
            # print(V_T.shape)
            # print(V.shape)
            V_T[1:d-1] = (1-eta)*V[2:d]
            V_T[d-1:] = (1-eta)*np.append(V[d:], np.zeros(1)) + eta*V[0:M-d+1]
            V = V_T

        V = V / sum(np.abs(V))
        delta = sum(abs(V-V_prime))
        # print(delta)
    return V


def algorithm2(M, V, eta, P, B, d):
    
    A = np.zeros((M, B, P))
    nz_list = []
    tset = []

    for l in range(M):
        A[l,B-1,0] = V[l]
        tset.append((l, B-1)) 

    nz_list.append(tset)
    
    for n in range(P-1):

        iterset = nz_list[n]
        tset = []
        for (l, g) in iterset:
            # print( (l, g, n) )
            if g > 0:

                if l > 0:

                    A[l-1,g-1,n+1] += (1-eta)*A[l, g, n]
                    tset.append((l-1, g-1))
                    if l+d-1 < M:
                        A[l+d-1, g-1, n+1] += eta*A[l,g,n]
                        tset.append((l+d-1, g-1))
                
                elif l == 0:

                    A[l, g, n+1] += (1-eta)*A[l, g, n]
                    tset.append((l, g))
                    if l+d-1 < M:
                        A[l+d-1, g-1, n+1] += eta*A[l, g, n]
                        tset.append((l+d-1, g-1))

            elif g == 0:

                A[l, g, n+1] += (1-eta)*A[l, g, n]
                tset.append((l, g))
                if l+d < M:
                    A[l+d,g,n+1] += eta*A[l, g, n]
                    tset.append((l+d, g))
        tset = list(set(tset))
        nz_list.append(tset)

    return A, nz_list


def fds(l, g, n, d, P, B):
    h = l + d
    gamma1 = min(P-n, g)
    gamma2 = P-n-gamma1
    if h <= gamma1:
        return h
    elif h > gamma1 and h <= gamma1 + B:
        return h + gamma2
    else:
        return h + gamma2 + math.ceil((h-(gamma1+B))/B)*(P-B)
    
    print("error")
    return -1

def get_distribution(lambda_, d_prime, B_prime, P_prime, N=20, M=200):

    eq_sense = 0.1

    d = N
    B = math.floor(N*B_prime/d_prime)
    P = math.floor(N*P_prime/d_prime)
    eta = lambda_*d_prime/N
    print(f"{M}*({B}+1)*{P}, eta={eta}, d={d}")
    Delta = 0.01
    
    q_l_b_0 = algorithm1(M, Delta, eta, P, B, d)
    A, nz_list = algorithm2(M, q_l_b_0, eta, P, B, d)
    # print(q_l_b_0)
    print("finish alg 2")
    # print(A)
    # print( sum(sum( A[:, :, 0]) ) )
    # print( sum(sum( A[:, :, 1] )) )
    # print( sum(sum( A[:, :, 2] )) )
    # print( sum(sum( A[:, :, 3] )) )
    # print( sum(sum( A[:, :, 4] )) )
    # print( sum(sum( A[:, :, 5] )) )
    # print( sum(sum( A[:, :, 6] )) )
    # print( sum(sum( A[:, :, 7] )) )
    F_DS = np.zeros(M)
    # print(np.sum(A))
    for i in range(M):
        for l in range(A.shape[0]):
            for g in range(B):
                for n in range(P):
                    if abs( fds(l, g, n, d, P, B) - i ) < eq_sense:
                        F_DS[i] += 1/P*(A[l, g, n])

    return F_DS


if __name__ == "__main__":
    lambda_ = [0.2, 0.3, 0.4, 0.5]
    d_ = [0.5, 0.75, 1, 1.25]
    P_ = [1, 4, 8]
    W_ = [0.6, 0.8, 1]
    dist = []
    N = 17
    M = 300
    sweep_type = "W"
    # for lamb_ in lambda_:
    #     x = get_distribution(lamb_, 1, 1.2, 2, N, M)
    #     dist.append(x)
    #     plt.plot(np.arange(M)/N ,np.cumsum(x))
    #     plt.xlim((0, math.ceil(M/N)))

    # for d in d_:
    #     x = get_distribution(0.4, d, 1.2, 2, N, M)
    #     dist.append(x)
    #     plt.plot(np.arange(M)/N ,np.cumsum(x))
    #     plt.xlim((0, math.ceil(M/N)))

    # for P in P_:
    #     x = get_distribution(0.4, 1, 1.2/2*P, P, N, M)
    #     dist.append(x)
    #     plt.plot(np.arange(M)/N ,np.cumsum(x))
    #     plt.xlim((0, math.ceil(M/N)))


    for W in W_:
        x = get_distribution(0.4, 1, 2*W, 2, N, M)
        dist.append(x)
        plt.plot(np.arange(M)/N ,np.cumsum(x))
        plt.xlim((0, math.ceil(M/N)))

    plt.legend(["60%", "80%", "100%"])
    plt.savefig(f"{sweep_type}-sweepp,N={N},M={M}.png")