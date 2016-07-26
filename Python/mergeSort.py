#!/usr/bin/env python3
# encoding: utf-8

def merge(toBeSorted):

    if (len(toBeSorted) > 1):
        middle = len(toBeSorted) // 2
        left = toBeSorted[:middle]
        right = toBeSorted[middle:]

        merge(left)
        merge(right)

        leftIndex = 0
        rightIndex = 0
        totalIndex = 0

        while (leftIndex < len(left) and rightIndex < len(right)):
            if (left[leftIndex] <= right[rightIndex]):
                toBeSorted[totalIndex] = left[leftIndex]
                leftIndex += 1
                totalIndex += 1
            else:
                toBeSorted[totalIndex] = right[rightIndex]
                rightIndex += 1
                totalIndex += 1

        while (leftIndex < len(left)):
            toBeSorted[totalIndex] = left[leftIndex]
            leftIndex += 1
            totalIndex += 1

        while (rightIndex < len(right)):
            toBeSorted[totalIndex] = right[rightIndex]
            rightIndex += 1
            totalIndex += 1
        return toBeSorted


def ReadInputFile(InputFile):
    try:
        with open(InputFile) as data:
            '''
            Read Data
            '''
            size = map(int, data.readline().rstrip().split())
            
            lst = list(map(int, data.readline().rstrip().split()))

            sortedlst = merge(lst)
            for elem in sortedlst:
                print(elem)
                
    except IOError as e:
        print('Operation failed: %s' % e.strerror)
        
ReadInputFile("/home/akopp/Documents/RosalindInput/rosalind_ms.txt")