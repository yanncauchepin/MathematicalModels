import scipy.linalg as nla
import scipy.interpolate as nla2
import numpy as np
import matplotlib.pyplot as plt


#CONSTRUCTION DE X ET Y
import csv

X = np.array([], float)
Y = np.array([], float)
with open ('spnbmd.csv', 'r', newline='') as csvfile :
    myreader = csv.reader(csvfile, delimiter=',')
    next(myreader)
    for row in myreader :
        X = np.append(X,float(row[2]))
        Y = np.append(Y,float(row[4]))

n = np.size(X)-1 #Taille X-1

#Trier X et Y :
X = X[X.argsort()]
Y = Y[X.argsort()]

#Test de pour de pas avoir de H nul :
for i in range (0,n) :
    if X[i] == X[i+1] :
        #print(i)
        j=1
        while X[i+j] == X[i] :
            j = j+1
        for k in range (1,j+1) :
            X[i+k] = X[i] + k*0.1/(j+1)

        #X = np.delete(X,i+1)
        #Y = np.delete(Y,i+1)


#Par défaut
p=29.0

#CONSTRUCTION DE SIGMA

Sigma = np.eye(n+1)
Sigma2 = np.dot(Sigma, Sigma)

#CONSTRUCTION H ET G
H = np.zeros(n)
G = np.zeros(n)
for i in range(0,n):
  H[i] = X[i+1]-X[i]
  G[i] = 1/H[i]


#CONSTRUCTION T
T=np.zeros((n-1,n-1))

T[0,0]=1/3*(2*(H[0]+H[1]))
T[1,0]=1/3*H[1]
T[n-2,n-2]=(1/3)*(2*(H[n-2]+H[n-1]))
T[n-3,n-2]=1/3*H[n-2]
for i in range(1,n-2):
    #Attention, i ne prend pas n-2
    T[i-1, i]=1/3*H[i]
    T[i,i]=1/3*(2*(H[i]+H[i+1]))
    T[i+1, i]=1/3*H[i+1]

#CONSTRUCTION Q
Q=np.zeros((n+1,n-1))
    #Attention, i ne prend pas n
for i in range (0,n-1):
    Q[i, i]=G[i]
    Q[i+1, i] = -G[i]-G[i+1]
    Q[i+2,i] = G[i+1]




#CALCUL DES PARAMETRES :

#CALCUL DE c
A=np.dot(np.dot(Q.T,Sigma2), Q)+p*T #Partie gauche
b=p*np.dot(Q.T, Y) #Partie droite


#Résolution CHolesky :
#Ax=b
#On veut A = L*L.T (Factorisation)
#L*L.T*x=bimport matplotlib.pyplot as plt
#1) Ly=b (On cherche y)
#2) L.Tx=y (On cherche x)

#Bloc de Vérification par la méthode simple :
#np.linalg.solve(np.dot(np.dot(Q.T,Sigma), Q)+p*T, p*np.dot(Q.T, Y))

#On cherche L
L=np.linalg.cholesky(np.dot(np.dot(Q.T,Sigma), Q)+p*T)

#On retrouve bien L*L.T = A
yy=nla.solve_triangular(L, b, trans = 0, lower = True)
c=np.array([], float)
c=nla.solve_triangular(L, yy, trans = 1, lower = True)

#On détermine c_force
#Rajout de 0 au début et à la fin
c_force = np.concatenate(([0], c , [0]), axis=0)

#CALCUL DE d
d=np.zeros(n,float)

for i in range (0,n) :
    d[i]=(c_force[i+1]-c_force[i])/(3*H[i])

#CALCUL DE a
a = Y - (1.0/p) * np.dot(np.dot(np.dot(Sigma,Sigma), Q), c)

#CALCUL DE b
b=np.zeros(n,float)

for i in range (0,n) :
    b[i]=((a[i+1]-a[i])/H[i])-(c_force[i]*H[i])-(d[i]*(H[i]*H[i]))


#CALCUL DU DEGRE DE LIBERTE
Sp=np.zeros((n+1,n+1))
I=np.eye(n+1)
Sp = I - np.dot(Sigma2, np.dot(Q, np.dot(np.linalg.inv(A) , Q.T)))
df = np.trace(Sp)

#TRACER LE GRAPHE

#Tracer les points X et Y
#plt.plot(X,Y,'r.')

#Tracer les segments de la spline + CALCUL DU PARAMETRE OPTIMAL
somme = 0
for i in range(0,n):
	xnew = np.linspace(X[i], X[i]+H[i], 50)
	ynew = a[i] + b[i]*(xnew-X[i]) + c_force[i]*(xnew-X[i])**2 + d[i]*(xnew-X[i])**3
	somme = somme + ((Y[i]-ynew[0])/(1-Sp[i,i]))**2
	#plt.plot(xnew,ynew,"-r")
	plt.plot(xnew,ynew,"-b")

somme = somme + ((Y[n]-ynew[49])/(1-Sp[n,n]))**2

#AFFICHAGE DES PARAMETRES CALCULÉS
print("Le degré de liberté optimal vaut : ", df)
print("Le paramètre optimal vaut : ", somme)

#AFFICHAGE DU GRAPHE
plt.xlabel("age")
plt.ylabel("spnbmd")
plt.title("Spline lissante")
plt.show()
