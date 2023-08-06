# **ilap** : Python Tools for Numerical Inversion of the Laplace Transform

## Overview

The **ilap** package implements the Fixed Talbot method for numerical inversion of the Laplace transform outlined by Abate and Valko (2004). Implementation is from scratch, based on the mathematical derivation presented in the paper.

Two functions are exposed, both of which implement the same functionality, but each using a different backend.

- **invert(_lt_, _t_)** takes the name, _lt_, of some function of a single variable, **lt(_s_)**,  defining a Laplace transform with Laplace variable _s_, and a specified scalar (integer or float), _t_, representing the time at which the transform is to be inverted. It returns a float, representing the approximate value of the inverse transform at time _t_. The implementation uses Numpy or pure Python for all its numerics, and should accept essentially any function **lt**, regardless of the libraries used in its definition.

- **invert_mp(_lt_, _t_)** operates the same way as **invert(_lt_, _t_)**, but it uses the mpmath arbitrary-precision library for its numerics. Because the numerical inversion of the Laplace transform is an ill-conditioned inverse problem, it is often necessary to use more than double precision to obtain useful results, and I recommend using this version if possible. The disadvantage of this method is that the mpmath library cannot work gracefully with Numpy/Scipy/Python math module functions: the transform **lt** _must_ be defined using only math functions defined in the mpmath module (most functions you could want are available), and basic Python arithmetic operations. **invert_mp** uses the currently set decimal precision of the mpmath module, which can be adjusted as needed before making a call to **invert_mp**. See the [mpmath documentation](https://mpmath.org/doc/current/) for more details.

## Usage Example

This example demonstrates numerical inversion of a Laplace-domain analytical solution to the advection-dispersion equation using both inversion methods, and comparing the results with a time-domain analytical solution:

    from ilap import invert, invert_mp
    from matplotlib.pyplot import plot, legend, show, title, xlabel, ylabel
    import mpmath as mpm
    import numpy as np
    from numpy import fromiter, float64, linspace, vectorize

    #DEFINE LAPLACE TRANSFORMS FOR ADE AND TARGET SOLUTION
    def L(alpha, d, v):
        return d**2/(2*alpha*v)

    def M(d, v):
        return d/v 

    #Laplace transform using numpy functions
    def phi_trans(s, d, alpha, v): 
        def ig_trans(s, L, M):
            return np.exp(L/M - np.sqrt(L/M**2+ 2*s)/np.sqrt(1/L))
        return ig_trans(s, L(alpha, d, v), M(d, v))

    #Laplace transform using mpmath functions
    def phi_trans_mp(s, d, alpha, v): 
        def ig_trans(s, L, M):
            return mpm.exp(L/M - mpm.sqrt(L/M**2+ 2*s)/mpm.sqrt(1/L))
        return ig_trans(s, L(alpha, d, v), M(d, v))

    #Target analytic solution
    def phi_direct(t, d, alpha, v): 
        def ig_direct(t, L, M):
            return np.sqrt(L/(2*np.pi*t**3))*np.exp(-L*(t-M)**2/(2*M**2*t))
        return ig_direct(t, L(alpha, d, v), M(d, v))

    #PHYSICAL PARAMETERS
    d = 1.5         #distance [m]
    alpha = 3e-2    #dispersivity [m]
    v = 0.53e-3     #velocity [m/s]
    v_t = linspace(1, 7000, num=100) #times [s]
    
    #PLOTTING
    #Plot target solution
    df = vectorize(lambda t: phi_direct(t, d, alpha, v))
    v_PDF = df(v_t)
    plot(v_t, v_PDF, 'ks', markerfacecolor='none', ms=6, markeredgecolor='darkolivegreen', label="Exact solution")

    #Plot numerical inversion via invert()
    lt = lambda s: phi_trans(s, d, alpha, v)
    v_PDFt = fromiter(map(lambda t: invert(lt,t), v_t), dtype=float64)
    plot(v_t, v_PDFt, lw=2, color="navy", label="Solution via invert()")

    #Plot numerical inversion
    lt = lambda s: phi_trans_mp(s, d, alpha, v)
    v_PDFt = fromiter(map(lambda t: invert_mp(lt,t), v_t), dtype=float64)
    plot(v_t, v_PDFt, ls=(0, (3, 3)), lw=2, color="goldenrod", label="Solution via invert_mp()")

    #Format the plot area
    xlabel("Time")
    ylabel("Probability density")
    title("Test of ilap module inversion methods on ADE solution")
    legend()
    show()

## Reference

Abate, J. and P. P. Valko, 2004. Multi-precision Laplace transform inversion. _International Journal for Numerical
Methods in Engineering_, 60(5), 979. doi:10.1002/nme.995.
