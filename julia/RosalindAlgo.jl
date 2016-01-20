## Compute Fibonnaci numbers, give a number n and get the n fibo number
function Fibonacci(n::Int)
    if n == 0
        return 0
    else
        Arr = Array(Int64, (n+1))
        setindex!(Arr, 0, 1)
        setindex!(Arr, 1, 2)
        for i in 3:n+1
            setindex!(Arr, (getindex(Arr, i-1) + getindex(Arr, i-2)), i)
        end
        return getindex(Arr, n+1)
    end
end



## recursive binary search, return index of value to search
function RecBinarySearch(arr::AbstractArray, value, low, high)
    if high < low
        return -1
    end
    mid = round(Int, (low+high) / 2)
    if getindex(arr, mid) > value
        return RecBinarySearch(arr, value, low, mid-1)
    elseif getindex(arr, mid) < value
        return RecBinarySearch(arr, value, mid+1, high)
    else
        return mid
    end
end


## iterative binary search, return index of value
function ItBinarySearch(arr::AbstractArray, value)
    low = 1
    high = length(arr)
    while low <= high
        mid = round(Int, (low+high) / 2)
        if getindex(arr, mid) > value
            high = mid - 1
        elseif getindex(arr, mid) < value
            low = mid + 1
        else
            return mid
        end
    end
    return -1
end


## Merge two sorted array
function MergeSortedArray(A::AbstractArray, B::AbstractArray)
    a = length(A)
    b = length(B)
    res = Array(Float64, (a+b))
    i = 1
    j = 1
    k = 1
    while i <= a && j <= b
        if A[i] <= B[j]
            res[k] = A[i]
            i += 1
        else
            res[k] = B[j]
            j += 1
        end
        k += 1
    end
    if i < a
        for p = i:a
            res[k] = A[p]
            k += 1
        end
    else
        for p = j:b
            res[k] = B[p]
            k += 1
        end
    end
    return res
end

####################### TEST

println("Fibonacci")
@time x = Fibonacci(200)
@time x = Fibonacci(200)


println("Recursive binary search")
@time x = RecBinarySearch([6, 10, 12, 20, 65], 10, 1, 6)
@time x = RecBinarySearch([6, 10, 12, 20, 65, 78, 79, 85, 90], 85, 1, 9)


println("Iterative binary search")
@time x = ItBinarySearch([6, 10, 12, 20, 65], 10)
@time x = ItBinarySearch([6, 10, 12, 20, 65, 78, 79, 85, 90], 85)

# f = open("/home/akopp/Documents/RosalindInput/rosalind_bins.txt")
# x = readall(f)
# x = split(x, "\n")
# close(f)
# array = readdlm(IOBuffer(x[3]), Int)
# searching = readdlm(IOBuffer(x[4]), Int)
# for elem in searching
#     x = ItBinarySearch(array, elem)
#     print(x)
#     print(" ")
# end


println("Use of Binary search")
@time ItBinarySearch(array, 3008)
@time RecBinarySearch(array, 3008, 1, length(array))

println("Merging two sorted arrays")
@time MergeSortedArray([6, 10, 12, 54, 60], [5, 7, 15, 52])
@time MergeSortedArray([6, 10, 12, 54, 60], [5, 7, 15, 52])

f = open("/home/akopp/Documents/RosalindInput/rosalind_mer.txt")
x = readall(f)
x = split(x, "\n")
close(f)
A = readdlm(IOBuffer(x[2]), Int)
B = readdlm(IOBuffer(x[4]), Int)
@time x= MergeSortedArray(A, B)
