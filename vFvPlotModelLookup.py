import numpy as np
from numpy import exp, power, float64, array, inf, logical_and, zeros, log10, log, logical_or, asarray
from pygsl.sf import synchrotron_1 
import pygsl.errors
from scipy.integrate import quad, quadrature


#J. Michael burgess October 2011
#
# This file contains models defined in the way of RMFIT for the SCATReader
# and other files to calculate errors and fluxes
# for each new model the modelLookup dict needs to be updated
#


def Band( x, A, Ep, alpha, beta):

	if x < (alpha-beta)*Ep/(2+alpha):
		band = A*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) )
	elif x >= (alpha-beta)*Ep/(2+alpha):
		band = A* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))
        return band

def BlackBody(x,A,kT):

	val = A*power(x,2)*power(exp(x/float64(kT))-1,-1)

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
#		print err
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

def PowerLaw2Breaks(x, A, pivot, index1, breakE1, index1to2, breakE2, index2):
	
	cond1 = x <= breakE1
	cond2 = logical_and(x > breakE1, x <= breakE2)
	cond3 = x > breakE2
	
	pl2b = np.piecewise(x, [cond1,cond2,cond3],\
				    [lambda x: power(x/pivot,index1),lambda x:power(breakE1/pivot,index1)*power(x/breakE1,index1to2),lambda x: power(breakE1/pivot,index1)*power(breakE2/breakE1,index1to2)*power(x/breakE2,index2)])

	return A*pl2b


def sbpl(ene, logN, pivot, indx1, breakE, breakScale, indx2):




    B = (indx1 + indx2)/2.0
    M = (indx2 - indx1)/2.0

    arg_piv = log10(pivot/breakE)/breakScale

    if arg_piv < -6.0:

        pcosh_piv = M * breakScale * (-arg_piv-log(2.0))

    elif arg_piv > 4.0:

        pcosh_piv = M * breakScale * (arg_piv - log(2.0))

    else:

        pcosh_piv = M * breakScale * (log( (exp(arg_piv) + exp(-arg_piv))/2.0 ))



    arg = log10(ene/breakE)/breakScale


    if  arg < -6.0:
        pcosh = M * breakScale * (-arg-log(2.0))

    elif arg >  4.0:
        pcosh = M * breakScale * (arg - log(2.0))

    else:
        pcosh = M * breakScale * (log( (exp(arg) + exp(-arg))/2.0 ))


   

    val = logN * power(ene/pivot,B)*power(10.,pcosh-pcosh_piv)

    return val







modelLookup = {"Power Law w. 2 Breaks":PowerLaw2Breaks, "Band's GRB, Epeak": Band, "Total Test Synchrotron": TotalSynchrotron, "Black Body": BlackBody,\
		"Comptonized, Epeak": Compt, "Power Law": PowerLaw, "BlackBody2":BlackBody ,"Smoothly Broken Power Law":sbpl}
