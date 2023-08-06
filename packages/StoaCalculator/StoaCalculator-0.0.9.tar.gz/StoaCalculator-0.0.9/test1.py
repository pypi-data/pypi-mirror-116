import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
x = np.linspace(-5, 5, 100)

# the function, which is y = x^2 here
formula1 = 2*x
formula2 = np.sin(x)


def biplot(x, formula1, formula2):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title('Stoas Calculator Graph')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, formula1, 'w', label='1st Equation')
    plt.plot(x, formula2, 'm', label='2nd Equation')

    plt.legend(loc='upper left')

    # show the plot
    plt.show()

biplot(x, formula1, formula2)
