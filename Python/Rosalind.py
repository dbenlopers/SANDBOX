# Enumerating Gene Orders problem for rosalind

def factorial(x):
    if x > 0:
        return x*factorial(x-1)
    else:
        return 1

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p
            xs[low], xs[i] = xs[i], xs[low]

I = 5
# I = open("/home/akopp/Documents/RosalindInput/rosalind_perm.txt", "r").read()

print(factorial(I))

for p in permute([i for i in range(1, 1+I, 1)]):
    for item in p:
        print(item, end=" ")
    print("")



"""A solution to the Rosalind prolbem "Mendel's First Law."
http://r...content-available-to-author-only...d.info/problems/iprb/
"""

def probability(k, m, n):
    """Find the probability that two randomly selected mating organisms will
    produce an individual with a dominant allele."""

    pops = {'k': k, 'm': m, 'n': n}

    def _total_pop(populations):
        return sum(v for k, v in populations.items())

    def _event_probablity(subpop, populations):
        return populations[subpop] / _total_pop(populations)

    def _pick(p1, p2, populations):
        _pop = dict(populations)

        first_event_probability = _event_probablity(p1, _pop)
        _pop[p1] = _pop[p1] - 1
        second_event_probability = _event_probablity(p2, _pop)

        if 'k' in (p1, p2):
            multiplier = 1.0
        elif p1 == p2 and p1 == 'm':
            multiplier = 0.75
        elif 'm' in (p1, p2) and 'n' in (p1, p2):
            multiplier = 0.5
        elif 'n' == p1 and 'n' == p2:
            multiplier = 0.0

        return first_event_probability * second_event_probability * multiplier

    return sum(_pick(subpop1, subpop2, pops)
               for subpop2 in pops.keys()
               for subpop1 in pops.keys())


# print(probability(18, 20, 15))


def rabinacci(old, young, reproduction_rate, months):
    result = None
    if months == 1:
        result = young
    else:
        result = rabinacci(young, old * reproduction_rate + young, reproduction_rate, months - 1)

    return result


print(rabinacci(0, 1, 3, 36))
