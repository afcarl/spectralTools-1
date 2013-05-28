from numpy import power, exp, log, log10, sqrt, piecewise, cosh


def Linear(x,m,b):
    val = m*x+b 
    return val
    


def PowerLaw(x, norm, index, t0=0., pivot=1.):

    val = norm * power((x-t0)/pivot,index)
    return val

def BrokenPL(x, norm, indx1, breakPoint, indx2, t0=0., pivot=1):

    
    cond1 = x <  breakPoint
    cond2 = x >= breakPoint

    val = piecewise(x, [cond1, cond2],\
                                    [lambda x:norm * power((x-t0)/pivot ,indx1) , \
                                             lambda x: norm * power( (breakPoint-t0) / pivot ,indx1-indx2 ) * power((x-t0)/pivot, indx2)  ])
    return val


def Gaussian(x, norm, mu, sigma):

    val = norm * exp(-power(x-mu,2.)/(2*sigma**2))
    return val
    
    
def Exponential(x, norm, x0=0.,a=1., b=-1.):
    
    val = norm * exp(a*power(x-x0,b))
    return val
    
    
def RydeBPL(x, norm, indx1, indx2, breakTime ,delta, tn=1.,t0=0):

    eps=(indx2-indx1)/2
    phi=(indx2+indx1)/2
    
    val = norm*power((x-t0)/tn,phi)*power( cosh(log10((x-t0)/breakTime)/delta)/cosh(log10(tn/breakTime)/delta),eps*delta*log(10.)  )
    return val
 
def Band( x, A, Ep, alpha, beta):

	cond1 = x < (alpha-beta)*Ep/(2+alpha)
	cond2 = x >= (alpha-beta)*Ep/(2+alpha)



        band = piecewise(x, [cond1, cond2],\
				    [lambda x: A*( power(x/100., alpha) * exp(-x*(2+alpha)/Ep) ), \
					     lambda x:A* ( power( (alpha -beta)*Ep/(100.*(2+alpha)),alpha-beta)*exp(beta-alpha)*power(x/100.,beta))])

        return band  

def BlackBody(x,A,kT):

	val = A*power(x,2)*power(exp(x/float64(kT))-1,-1)

	return val
 

functionLookup = {"PowerLaw": PowerLaw, "BrokenPL": BrokenPL, "Gaussian": Gaussian, "Exponential" : Exponential, "Linear": Linear, "RydeBPL": RydeBPL, "Band" : Band, "BlackBody" : BlackBody }

