import numpy as np
from numpy import exp, power, float64, array, inf
from instant import header_and_libs_from_pkgconfig, inline_with_numpy
from pygsl.sf import synchrotron_1 
import pygsl.errors
from scipy.integrate import quad, quadrature

def Band( x, A, Ep, alpha, beta):


	cond1 = x < (alpha-beta)*Ep/(2+alpha)
	cond2 = x >= (alpha-beta)*Ep/(2+alpha)



        band = np.piecewise(x, [cond1, cond2],\
				    [lambda x: A*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) ), \
					     lambda x:A* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100,beta))])

        return band

def BlackBody(x,A,kT):

	
#	print A
#	print kT
#	print x
	val = A*power(x,2)*power(exp(x/float64(kT))-1,-1)
#	print val
	#print val
	return val

def PowerLaw(x, A, Epiv, index):

    return A*(x/Epiv)**index

def Compt(x,A,Ep,index,Epiv):

	return A*exp(-x*(2+index)/Ep )*power(x/Epiv,index)


#### Synchrotron with pygsl

def TotalSynchrotron(x, A, eCrit, eta, index, gammaTh):

	A=float(A)
	eCrit = float(eCrit)
	eta = float(eta)
	index = float(index)
	gammaTh = float(gammaTh)

	val,err, = quad(Integrand, 1,inf, args=(x,A,eCrit,eta,index,gammaTh),epsabs=0., epsrel= 1.e-5 )
	val= val/(x)

	return val


def Integrand( gamma, x ,A, eCrit, eta, index, gammaTh):
	
	try:
		val = EDist(A,gamma,eta,gammaTh,index) * synchrotron_1(x/(eCrit*gamma*gamma))[0]
	except pygsl.errors.gsl_Error, err:
		print err
		val = 0.
	return val


def EDist(A,gamma,eta, gammaTh, index):
	
	epsilon = (eta/gammaTh)**(2+index)*exp(-(eta/gammaTh))
	cond1 = gamma <= eta
	cond2 = gamma > eta

	gamma=float(gamma)

	if gamma<=eta:

		val = A * (gamma/gammaTh)**2 * exp(-(gamma/gammaTh))

	else:
		val = A * epsilon * (gamma/gammaTh)**(-index)

#	val = np.piecewise(x,[cond1,cond2],\
#				   [lambda x: A * (gamma/gammaTh)**2 * exp(-(gamma/gammaTh)),\
#					    lambda x:  A * epsilon * (gamma/gammaTh)**(-index))



	return val
