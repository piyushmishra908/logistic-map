import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def logistic(r, x):
    return r * x * (1 - x)


def plot_system(r, x0, n):
    """
    Method to generate the logistic plot with step 

    input arguments:
        r: int or float, the r-value of a logistic coefficient
        x0: int or float, the radius of the circle
        n: int, number of points (optional)

    output:
        plot
    """
    # Plot the function and the
    # y=x diagonal line.
    """
    imput parameter:
        r: Coefficient for logistic map
        x0: input x for logistic map
        n: Max iteration 
    output:
       1. Return Logistic map plot
       2. Return xt(log function) vs t(time) plot
    """
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(8, 4))
    t = np.linspace(0, 1)
    ax1.plot(t, logistic(r, t), 'k', lw=2)
    ax1.plot([0, 1], [0, 1], 'k', lw=2)
    x = x0
    time= []
    xt = []
    for i in range(n):
        y = logistic(r, x)
        # Plot the two lines.
        ax1.plot([x, x], [x, y], 'k', lw=1)
        ax1.plot([x, y], [y, y], 'k', lw=1)
        # Plot the positions with increasing
        # opacity.
        ax1.plot([x], [y], 'ok', ms=10,
                alpha=(i + 1) / n)
        x = y
        time.append(i)
        xt.append(x)

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title(f"$r={r:.1f}, \, x_0={x0:.1f}$")
    ax2.plot(time,xt,'ok',alpha=0.6)
    ax2.plot(time,xt,'k',lw=2)
    ax2.set_ylim(0, 1)
    ax2.set_xlim(0, n)
    ax2.set_title(f"$r={r:.1f}, \, x_0={x0:.1f}$")
    st.pyplot()

    return

def bifurcation_map(n,range1,range2,iterations,last):
    """
    Method to generate the bifuraction plot 
    """
    r = np.linspace(range1, range2, n)
    x = 1e-5 * np.ones(n)
    lyapunov = np.zeros(n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9),
                                   sharex=True)
    for i in range(iterations):
        x = logistic(r, x)
        # We compute the partial sum of the
        # Lyapunov exponent.
        lyapunov += np.log(abs(r - 2 * r * x))
        # We display the bifurcation diagram.
        if i >= (iterations - last):
            ax1.plot(r, x, ',k', alpha=.25)
    ax1.set_xlim(2.5, 4)
    ax1.set_title("Bifurcation diagram")

    # We display the Lyapunov exponent.
    # Horizontal line.
    ax2.axhline(0, color='k', lw=.5, alpha=.5)
    # Negative Lyapunov exponent.
    ax2.plot(r[lyapunov < 0],
             lyapunov[lyapunov < 0] / iterations,
             '.k', alpha=.5, ms=.5)
    # Positive Lyapunov exponent.
    ax2.plot(r[lyapunov >= 0],
             lyapunov[lyapunov >= 0] / iterations,
             '.r', alpha=.5, ms=.5)
    ax2.set_xlim(range1, range2)
    ax2.set_ylim(-2, 1)
    ax2.set_title("Lyapunov exponent")
    plt.tight_layout()
    st.pyplot()

    return 

if __name__ == "__main__":
    #method_option = st.sidebar.selectbox("Choose a method", ["Logistic", "Bifurcation"])
    st.title("Logistic Map App")
    st.markdown("Version 1.1 : Author: Piyush Mishra : Mentor: Rajarshi Das : Updated: Jul 19, 2020")
    st.markdown("** x(t+1) = r * x(t) * (1 - x(t)) **")
    st.markdown("Example: Population(t+1) = Growth Rate * Population(t) * (1 - Population(t)) where Population(i) is expressed as a fraction of the maximum possible population size.")
    st.sidebar.markdown("Tunable Parameter")

    st.header("Logistic Plot")
    r1 = st.sidebar.number_input('Enter value of Growth Rate r : 0 < r < 4',value=2.5)
    x0 = st.sidebar.number_input('Enter initial population size, x(0): 0 < x(0) < 1',value=0.5)
    n1 = st.sidebar.number_input('Enter max number of iterations',value=10)
    plot_system(r1, x0, n1)
    ## Selectbox for displaying Bifurcation plot
    method_option = st.sidebar.checkbox("Route to Chaotic",value=False)

    if method_option:
        st.header("Bifurcation Plot")
        n = st.sidebar.number_input('Number for zeros',value=1000)
        range1 = st.sidebar.number_input('Range from',value=2.5)
        range2 = st.sidebar.number_input('Range to',value=4.0)
        iterations = st.sidebar.number_input('Iteration',value=1000)
        last = st.sidebar.number_input('Last value ',value=100)

        bifurcation_map(n,range1,range2,iterations,last)


