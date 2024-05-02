import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# All coordinates will have the following structure:
# Tuple of two elements (x, y) for positions on the cartesian plane
# All coordinates will be within 0 and 1 (floating point)

# enable dynamic mode for dynamically displaying changes
# Dynamic mode runs slower, but updates the graphs dynamically, which is useful to see the process
dynamic_mode = False

weights = []
i = 0
while i < 400:
    w = (random.random(), random.random())
    if (w[0]-(0.5))**2+(w[1]-(0.5))**2 > 0.5**2 or (w[0]-(0.5))**2+(w[1]-(0.5))**2 < 0.3**2:
        continue
    else:
        weights.append(w)
        i += 1

circle_out = plt.Circle((0.5, 0.5), 0.5, color='r', fill=False)
circle_inn = plt.Circle((0.5, 0.5), 0.3, color='r', fill=False)

fig, ax = plt.subplots()

ax.add_patch(circle_out)
ax.add_patch(circle_inn)

plt.scatter(*zip(*weights), color='b')

if dynamic_mode:
    plt.ion()
    plt.draw()
    plt.pause(0.1)
else:
    ax.set_title("i = 0")
    plt.show()

i = 0 # t
lambda_i = 10
lambda_f = 0.01
epsilon_i = 0.5
epsilon_f = 0.05

i_max = 40000 # t_max

while i < i_max:
    signal = (random.random(), random.random())
    if (signal[0]-(0.5))**2+(signal[1]-(0.5))**2 > 0.5**2 or (signal[0]-(0.5))**2+(signal[1]-(0.5))**2 < 0.3**2:
        continue
    else:
        distances = []
        for j in range(len(weights)):
            distance = math.sqrt((weights[j][0] - signal[0])**2 + (weights[j][1] - signal[1])**2)
            # The index of the weight (j) needs to be inserted into the distances list
            # This is to retain the weight after sorting the distances, so as to know which weight
            # belongs to that particular distance
            distances.append((distance, j))
        
        distances.sort()
        for k in range(len(distances)):
            # Formulas for calculating the weight delta
            # After calculating the formula, the points will slightly converge on the signal
            epsilon_for_t = (epsilon_i*(epsilon_f/epsilon_i)**((i+1)/i_max))
            lambda_for_t = (lambda_i*(lambda_f/lambda_i)**((i+1)/i_max))
            w_delta = epsilon_for_t*(math.exp((-k)/lambda_for_t))
            w_delta_x = w_delta*(signal[0]-weights[distances[k][1]][0])
            w_delta_y = w_delta*(signal[1]-weights[distances[k][1]][1])

            # Updating the weights based on the weight delta
            weights[distances[k][1]] = (weights[distances[k][1]][0]+w_delta_x, weights[distances[k][1]][1]+w_delta_y)
        
        # clear past weight and signal points
        if dynamic_mode:
            plt.cla()

            ax.add_patch(circle_out)
            ax.add_patch(circle_inn)

            plt.scatter(*zip(*weights), color='b')
            plt.scatter(signal[0], signal[1], color='g')
            plt.draw()
            plt.pause(0.1)
        else:
            if i == 299 or i == 2499 or i == 39999:
                plt.close()

                circle_out = plt.Circle((0.5, 0.5), 0.5, color='r', fill=False)
                circle_inn = plt.Circle((0.5, 0.5), 0.3, color='r', fill=False)

                fig, ax = plt.subplots()

                ax.set_title(f"i = {i+1}")

                ax.add_patch(circle_out)
                ax.add_patch(circle_inn)

                plt.scatter(*zip(*weights), color='b')
                plt.scatter(signal[0], signal[1], color='g')
                plt.draw()
                plt.show()
        
    i += 1

# After all the iterations are complete, the weights should be equally distributed
# in the ring enclosed by the circles

# Final pause. The final pause can be anything, and the final graph will display
# for the amount set in that pause. This can be changed to anything from 60 seconds
if dynamic_mode:
    plt.pause(60)