import math
from scipy.optimize import fsolve

global roll_vel
global high,low
global a, b, shift, y0, yf, base, shift  # parameters for the velocity-to-frequency function


# Calculate the logarithmic function.
# f(x) = a * log(x + shifter) + b
# x represents velocity
def freqFunction(x):
   return a * math.log(x + shift, base) + b

# Calculate the logarithmic inverse function.
# Given the logarithmic function: f(x) = a * log(x + shifter) + b
# the matching inverse function is: f(x) = base^((x-b)/a) - shifter
# x represents velocity
def inverseFreqFunction(x):
   return base**((x-b)/a) - shift

def findIntersections(fun1, fun2, x0):
    xs = fsolve(lambda x: fun1(x) - fun2(x), x0)
    intersectionPoints = [[0, 0], [0, 0]]
    for i, x in enumerate(xs):
        x = round(x)
        xs[i] = x
        y=round(fun1(x))
        intersectionPoints[i][0] = x
        intersectionPoints[i][1] = y

    return intersectionPoints


def EucleadianDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)+(y2-y1))


def findMatchingEarFreq(freq):
    # 1) finding the distance between one intersection point and the calculated freq value by the log function.
    # 2) finding the point on the exponential function that matches the same distance from the other intersection point.

    epsilon = 1
    sum = 0
    intersections = findIntersections(freqFunction, inverseFreqFunction, [0, 1])

    # 1)
    xOne = intersections[0][0]  # x coordinate of the first intersection point - That's the lower bound
    yOnePrev = intersections[0][1]  # starts as the y coordinate of the first intersection point
    freqXval = roll_vel  # x coordinate of the current freq (=the given velocity) - That's the higher bound

    # 2)
    xTwoPrev = intersections[1][0]   # starts as the x coordinate of the second intersection point
    yTwoprev = intersections[1][1]  # starts as the y coordinate of the second intersection point
    xTwoCurr = xTwoPrev-epsilon

    for xi in range(xOne+epsilon,freqXval, epsilon):
        yi = freqFunction(xi)
        dist = EucleadianDistance(xi-epsilon, yOnePrev, xi, yi)
        sum = sum + dist

        # make the same step (distance) from the other intersection point on the exponential function
        inverseFreq = yTwoprev - math.sqrt(dist**2 - epsilon)

        yOnePrev = yi
        yTwoprev = inverseFreqFunction(xTwoCurr)
        xTwoCurr = xTwoCurr - epsilon

    return inverseFreq