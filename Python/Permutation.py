# Python function to print permutations of a given list
def permutation(lst):

    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []

    # If there is only one element in lst then, only
    # one permuatation is possible
    elif len(lst) == 1:
        return [lst]

    # Find the permutations for lst if there are
    # more than 1 characters
    else:
        l = [] # initiate an empty list

        # Iterate the input(lst) and calculate the permutation
        for i in range(len(lst)):
            m = lst[i]

            # Extract lst[i] or m from the list.  remLst is
            # remaining list
            remLst = lst[:i] + lst[i+1:]

            # Generating all permutations where m is first
            # element
            for p in permutation(remLst):
                l.append([m] + p)
        return l


# Driver program to test above function
data = list('123')
for p in permutation(data):
    print p

from itertools import permutations
l = list(permutations(range(1, 4)))
print l

# Python program to print all permutations with
# duplicates allowed

# Function to swap values
def swap(a,l,r):
    t = a[l]
    a[l] = a[r]
    a[r] = t
    return a

def toString(List):
    return ''.join(List)

# Function to print permutations of string
# This function takes three parameters:
# 1. String
# 2. Starting index of the string
# 3. Ending index of the string.
def permute(a, l, r):
    if l==r:
        print toString(a)
    else:
        for i in xrange(l,r+1):
            a = swap(a,l,i)
            permute(a, l+1, r)
            a = swap(a,l,i) # backtrack

# Driver program to test the above function
string = "ABC"
n = len(string)
a = list(string)
permute(a, 0, n-1)
