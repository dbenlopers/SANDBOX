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


####################### TEST

println("Fibonacci")
@time x = Fibonacci(200)
@time x = Fibonacci(200)


println("Recursive binary search")
@time x = RecBinarySearch([6, 10, 12, 20, 65], 10, 1, 6)
println(x)
@time x = RecBinarySearch([6, 10, 12, 20, 65, 78, 79, 85, 90], 85, 1, 9)
println(x)


println("Iterative binary search")
@time x = ItBinarySearch([6, 10, 12, 20, 65], 10)
println(x)
@time x = ItBinarySearch([6, 10, 12, 20, 65, 78, 79, 85, 90], 85)
println(x)

f = open("/home/akopp/Documents/RosalindInput/rosalind_bins.txt")
x = readall(f)
x = split(x, "\n")
close(f)
array = readdlm(IOBuffer(x[3]), Int)
searching = readdlm(IOBuffer(x[4]), Int)
# for elem in searching
#     x = ItBinarySearch(array, elem)
#     print(x)
#     print(" ")
# end


println("Use of Binary search")
@time ItBinarySearch(array, 3008)
@time RecBinarySearch(array, 3008, 1, length(array))
