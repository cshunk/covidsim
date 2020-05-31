"""
This module is a grab-bag of data collections and utility methods returning values that are specific to
Covid-19.
"""

import random

# Canonical distribution for onset_to_death for Covid-19.
# Derived from: https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
onset_to_death_distribution = [
    [0, 0.001049317943],
    [0.001049317943, 0.00314795383],
    [0.00314795383, 0.00629590766],
    [0.00629590766, 0.01154249738],
    [0.01154249738, 0.02098635887],
    [0.02098635887, 0.03567681007],
    [0.03567681007, 0.05771248688],
    [0.05771248688, 0.08604407135],
    [0.08604407135, 0.1217208814],
    [0.1217208814, 0.1605456453],
    [0.1605456453, 0.2056663169],
    [0.2056663169, 0.2539349423],
    [0.2539349423, 0.3043022036],
    [0.3043022036, 0.3567681007],
    [0.3567681007, 0.4102833158],
    [0.4102833158, 0.463798531],
    [0.463798531, 0.5162644281],
    [0.5162644281, 0.5676810073],
    [0.5676810073, 0.6180482686],
    [0.6180482686, 0.666316894],
    [0.666316894, 0.7124868835],
    [0.7124868835, 0.7534102833],
    [0.7534102833, 0.7901364113],
    [0.7901364113, 0.8216159496],
    [0.8216159496, 0.8499475341],
    [0.8499475341, 0.8751311647],
    [0.8751311647, 0.8971668416],
    [0.8971668416, 0.9160545645],
    [0.9160545645, 0.9317943337],
    [0.9317943337, 0.944386149],
    [0.944386149, 0.9548793284],
    [0.9548793284, 0.963273872],
    [0.963273872, 0.9695697796],
    [0.9695697796, 0.9748163694],
    [0.9748163694, 0.9790136411],
    [0.9790136411, 0.982161595],
    [0.982161595, 0.9842602308],
    [0.9842602308, 0.9863588667],
    [0.9863588667, 0.9884575026],
    [0.9884575026, 0.9905561385],
    [0.9905561385, 0.9926547744],
    [0.9926547744, 0.9947534103],
    [0.9947534103, 0.9968520462],
    [0.9968520462, 0.9989506821],
    [0.9989506821, 1]
]

# Early epidemic distribution for onset_to_death for Covid-19.
# This is skewed to rapid deaths, which take a larger percentage of the total deaths early in
# the epidemic.
# Derived from: https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
onset_to_death_distribution_skewed_early = [
    [0.0, 0.01287553648],
    [0.01287553648, 0.03004291845],
    [0.03004291845, 0.05150214592],
    [0.05150214592, 0.08154506438],
    [0.08154506438, 0.1158798283],
    [0.1158798283, 0.1673819742],
    [0.1673819742, 0.2274678112],
    [0.2274678112, 0.3004291845],
    [0.3004291845, 0.3690987124],
    [0.3690987124, 0.4206008584],
    [0.4206008584, 0.4721030043],
    [0.4721030043, 0.5236051502],
    [0.5236051502, 0.5579399142],
    [0.5579399142, 0.5922746781],
    [0.5922746781, 0.6266094421],
    [0.6266094421, 0.6566523605],
    [0.6566523605, 0.686695279],
    [0.686695279, 0.7167381974],
    [0.7167381974, 0.7424892704],
    [0.7424892704, 0.7682403433],
    [0.7682403433, 0.7854077253],
    [0.7854077253, 0.8025751073],
    [0.8025751073, 0.8197424893],
    [0.8197424893, 0.8369098712],
    [0.8369098712, 0.8497854077],
    [0.8497854077, 0.8626609442],
    [0.8626609442, 0.8755364807],
    [0.8755364807, 0.8884120172],
    [0.8884120172, 0.9012875536],
    [0.9012875536, 0.9141630901],
    [0.9141630901, 0.9227467811],
    [0.9227467811, 0.9313304721],
    [0.9313304721, 0.9399141631],
    [0.9399141631, 0.9484978541],
    [0.9484978541, 0.9570815451],
    [0.9570815451, 0.9656652361],
    [0.9656652361, 0.974248927],
    [0.974248927, 0.982832618],
    [0.982832618, 0.991416309],
    [0.991416309, 0.9957081545],
    [0.9957081545, 1.0]
]

# A standard bell curve distribution for the incubation period of Covid-19, centered around 5 days.
incubation_distribution = [
    [0, 0.05263157895],
    [0.05263157895, 0.1052631579],
    [0.1052631579, 0.2105263158],
    [0.2105263158, 0.4210526316],
    [0.4210526316, 0.6842105263],
    [0.6842105263, 0.8947368421],
    [0.8947368421, 1]
]

minimum_onset_to_death = 1
minimum_incubation = 2

IFR = 0.1


def get_random_from_distribution(minimum_value, distribution, increment=1):
    """Returns an integer from minimum_value to len(distribution)*increment,
    where the probability of any specific integer is determined by the
    probability distribution.
    """
    x = random.random()
    result = minimum_value - increment
    for limits in distribution:
        if x > limits[1]:
            result = result + increment
        else:
            break

    return result


def get_random_days_till_death():
    """Returns a number of days from infection till death matching a canonical probability distribution for Covid-19."""
    x = random.random()
    if x > IFR:
        return 0  # Survivor!
    else:
        return get_random_from_distribution(
            minimum_incubation, incubation_distribution
        ) + get_random_from_distribution(
            minimum_onset_to_death, onset_to_death_distribution
        )
