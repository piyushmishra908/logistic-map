import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def logistic(r, x):
    return r * x * (1 - x)


def plot_system(r, x0, n, ax=None):
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
    t = np.linspace(0, 1)
    ax.plot(t, logistic(r, t), 'k', lw=2)
    ax.plot([0, 1], [0, 1], 'k', lw=2)

    # Recursively apply y=f(x) and plot two lines:
    # (x, x) -> (x, y)
    # (x, y) -> (y, y)
    x = x0
    for i in range(n):
        y = logistic(r, x)
        # Plot the two lines.
        ax.plot([x, x], [x, y], 'k', lw=1)
        ax.plot([x, y], [y, y], 'k', lw=1)
        # Plot the positions with increasing
        # opacity.
        ax.plot([x], [y], 'ok', ms=10,
                alpha=(i + 1) / n)
        x = y

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1*(r/2.5))
    ax.set_title(f"$r={r:.1f}, \, x_0={x0:.1f}$")

def comp_map(r1,n1):
	fig, ax1 = plt.subplots(1, 1, figsize=(9, 6),sharey=True)
	plot_system(r1, .1, n1, ax=ax1)
	#plot_system(r2, .1, n2, ax=ax2)
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
    st.sidebar.markdown("Tunable Parameter")
    st.write("Sample Logistic Plot")
    x = np.linspace(0, 1)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, logistic(2, x), 'k')
    st.pyplot()
    st.write("Compare two Logistic Plot")
    r1 = st.sidebar.number_input('Enter a r1 value',value=2.5)
    n1 = st.sidebar.number_input('Enter a n1 value ',value=10)
    comp_map(r1,n1)
    ## Selectbox for displaying Bifurcation plot
    method_option = st.sidebar.checkbox("Route to Chaotic",value=False)

    if method_option:
        st.write("Bifurcation Plot")
        n = st.sidebar.number_input('Number for zeros',value=1000)
        range1 = st.sidebar.number_input('Range from',value=2.5)
        range2 = st.sidebar.number_input('Range to',value=4.0)
        iterations = st.sidebar.number_input('Iteration',value=1000)
        last = st.sidebar.number_input('Last value ',value=100)

        bifurcation_map(n,range1,range2,iterations,last)


