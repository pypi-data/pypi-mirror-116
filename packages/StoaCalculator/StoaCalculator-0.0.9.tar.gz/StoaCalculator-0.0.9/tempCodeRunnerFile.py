def quadraticplot(x, quadraticformula):

    plt.style.use('dark_background')

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_color('#00FFFF')
    ax.spines['bottom'].set_color('#00FFFF')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, quadraticformula, 'w')

    # show the plot
    plt.show()