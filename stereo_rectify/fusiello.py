"""
fusiello.py
	An implementation of the stereo rectification algorithm as described by Fusiello et al.
	in "A compact algorithm for rectification of stereo pairs", 1999.
	Implementation ported to python based on MATLAB code provided in paper.
"""

import numpy as np

def rectify(Po1, Po2):
	A1, R1, t1 = art(Po1)
	A2, R2, t2 = art(Po2)

	c1 = - np.linalg.inv(Po1[:,0:3]).dot((Po1[:,3].reshape(3, 1)))
	c2 = - np.linalg.inv(Po2[:,0:3]).dot((Po2[:,3].reshape(3, 1)))

	v1 = (c1-c2);
	v2 = np.cross((R1[2,:].reshape(3,1)), v1, axis=0)
	v3 = np.cross(v1,v2, axis=0)

	R = np.vstack((v1.T/np.linalg.norm(v1), v2.T/np.linalg.norm(v2), v3.T/np.linalg.norm(v3)))

	A = (A1 + A2)/2.0
	A[0,1]=0

	Pn1 = A.dot(np.hstack((R, -1.0 * R.dot(c1))))
	Pn2 = A.dot(np.hstack((R, -1.0 * R.dot(c2))))

	T1 = Pn1[0:3,0:3].dot(np.linalg.inv(Po1[0:3,0:3]))
	T2 = Pn2[0:3,0:3].dot(np.linalg.inv(Po2[0:3,0:3]))

	return T1, T2

def art(P):
	"""
	Factorize a PPM as P = A*[R;t]
	"""	
	Q = np.linalg.inv(P[0:3, 0:3])
	U,B = np.linalg.qr(Q)
	R = np.linalg.inv(U)
	t = B.dot(P[0:3,3])
	A = np.linalg.inv(B)
	A = np.divide(A, A[2, 2])
	return (A, R, t.reshape(3, 1))