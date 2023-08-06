import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Uniform(Distribution):
    """ Uniform distribution class for calculating and visualizing a Uniform distribution.
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        a (float) representing the upper limit
        b (float) representing the lower limit
    """
    def __init__(self, lowlim=0, highlim=1):
        self.a = lowlim
        self.b = highlim
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def calculate_mean(self):
        """Function to calculate the mean from a and b
        Args: None
        Returns: float: mean of the data set
        """
        self.mean = 1.0 * (self.b - self.a) / 2
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from a and b.
        Args: None
        Returns: float: standard deviation of the data set
        """
        self.stdev = (1.0 / 12) * (self.b - self.a) ** 2
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate a and b from the data set
        Args: None
        Returns:
            float: the a value
            float: the b value
        """
        self.a = min(self.data)
        self.b = max(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.a, self.b

    def pdf(self, k):
        """Probability density function calculator for the uniform distribution.
        Args: k (float): point for calculating the probability density function
        Returns: float: probability density function output
        """
        if k < self.a or k > self.b:
            pdfval = 0
        else:
            pdfval = 1.0 / (self.b - self.a)
        return pdfval

    def plot_bar_pdf(self):
        """Function to plot the pdf of the uniform distribution
        Args: None
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """
        x = []
        y = []
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')
        plt.show()
        return x, y

    def __add__(self, other):
        """Function to add together two Uniform distributions with equal a and b
        Args: other (Uniform): Uniform instance
        Returns: Uniform: Uniform distribution
        """
        try:
            assert self.a == other.a, 'a values are not equal'
        except AssertionError as error:
            raise
        try:
            assert self.b == other.b, 'b values are not equal'
        except AssertionError as error:
            raise
        result = Uniform()
        result.a = self.a
        result.b = self.b
        result.calculate_mean()
        result.calculate_stdev()
        return result

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        Args: None
        Returns: string: characteristics of the Gaussian
        """
        return "mean {}, standard deviation {}, a {}, b {}".\
        format(self.mean, self.stdev, self.a, self.b)
