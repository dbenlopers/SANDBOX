
def suffixArrays(s):
    """
    Given T return suffix array SA(T). We use Python's sorted function here for simplicity, but we
    can to better.
    """
    # Empty suffix '' play role of $.
    satups = sorted([(s[i:], i) for i in range(0, len(s)+1)])
    # Extract and return just the offset
    return map(lambda x: x[1], satups)

def bwt(t):
    """
    Given T, returns BWT(T), by way of the suffix array.
    """
    bw = []
    for si in suffixArrays(t):
        if si == 0:
            bw.append('$')
        else:
            bw.append(t[si-1])
    return ''.join(bw) # return string-ized version of list bw

def rankBwt(bw):
    """
    Given BWT string bw, returns a parallel list of B-ranks. Also returns tots, a mapping
    from characters to # times the characters appears in BWT.
    """
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots:
            tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots

def firstCol(tots):
    """
    Return a map from characters to the range of cells in the first column containing the character.
    """
    first = {}
    totc = 0
    for c, count in sorted(tots.items()):
        first[c] = (totc, totc+count)
        totc += count
    return first

def reverseBwt(bw):
    """
    Make T from BWT(T)
    """
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0
    t = "$"
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t
        rowi = first[c][0] + ranks[rowi]
    return t

bw = bwt('Tomorrow_and_tomorrow_banana')
print(bw)
rbw = reverseBwt(bw)
print(rbw)


def countMatches(bw, p):
    """
    Given BWT(T) and a pattern string p, return the number of times
    p occurs in T.
    """
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    l, r = first[p[-1]]
    i = len(p)-2
    while i >= 0 and r > l:
        c = p[i]
        # scan from left, looking for occurrences of c
        j = l
        while j < r:
            if bw[j] == c:
                l = first[c][0] + ranks[j]
                break
            j += 1
        if j == r:
            l = r
            break # no occurrences -> no match
        r -= 1
        while bw[r] != c:
            r -= 1
        r = first[c][0] + ranks[r] + 1
        i -= 1
    return r - l

print(countMatches(bw, 'mo'))


def rankAllBwt(bw):
    """
    Given BWT string bw, returns a map of lists.  Keys are
    characters and lists are cumulative # of occurrences up to and
    including the row.
    """
    tots = {}
    rankAll = {}
    for c in bw:
        if c not in tots:
            tots[c] = 0
            rankAll[c] = []
    for c in bw:
        tots[c] += 1
        for c in tots.keys():
            rankAll[c].append(tots[c])
    return rankAll, tots

def countMatches2(bw, p):
    """
    Given BWT(T) and a pattern string p, return the number of times
    p occurs in T.
    """
    rankAll, tots = rankAllBwt(bw)
    first = firstCol(tots)
    if p[-1] not in first:
        return 0 # character doesn't occur in T
    l, r = first[p[-1]]
    i = len(p)-2
    while i >= 0 and r > l:
        c = p[i]
        l = first[c][0] + rankAll[c][l-1]
        r = first[c][0] + rankAll[c][r-1]
        i -= 1
    return r - l # return size of final range

print(countMatches2(bw, 'mo'))
