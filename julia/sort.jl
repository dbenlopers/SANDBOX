## InsertionSort swap value into array
function SwapArray!(arr::AbstractArray, i1::Int, i2::Int)
    temp = getindex(arr, i1)
    setindex!(arr, getindex(arr, i2), i1)
    setindex!(arr, temp, i2)
end

# return sorted array
function InsertionSort(arr::AbstractArray)
    for i in 2:length(arr)
        k = i
        while k > 1 && (getindex(arr, k) < getindex(arr, k-1))
            SwapArray!(arr, k-1, k)
            k -= 1
        end
    end
    return arr
end

# return sorted array and movement count
function InsertionSortMovCnt(arr::AbstractArray)
    mvcnt = 0
    for i in 2:length(arr)
        k = i
        while k > 1 && (getindex(arr, k) < getindex(arr, k-1))
            SwapArray!(arr, k-1, k)
            k -= 1
            mvcnt += 1
        end
    end
    return arr, mvcnt
end


## merge sort
function mergesort!(A::AbstractVector)
    n = length(A)
    if n <= 1
        return A
    end
    Arr = Array(typeof(A[1]), length(A))
    width = 1
    while width < n
        i = 1
        while i < n
            i += i+2*width
            merge(A, i, min(i+width, n),min(i+2*width, n) ,Arr)
        end
        copyarray(Arr, A, n)
        width *= 2
    end
end

function merge(a::AbstractVector, left, right, final, b::AbstractVector)
    i = left
    j = right
    for k = left:final
        if (i < right) && (j >= final || a[i] <= a[j])
            b[k] = a[i]
            i += 1
        else
            b[k] = a[j]
            j += 1
        end
    end
end

# copy array b into array a
function copyarray(b::AbstractVector, a::AbstractVector, n)
    @inbounds for i = 1:n
        a[i] = b[i]
    end
end

####################### TEST


println("Swap inside array")
@time SwapArray!([6, 10, 4, 5, 1, 2], 4, 5)
@time SwapArray!([6, 10, 4, 5, 1, 2], 4, 5)

println("Insertion Sort")
A = randcycle(10000)
@time InsertionSort(A)
A = randcycle(10000)
@time InsertionSort(A)

f = open("/home/akopp/Documents/RosalindInput/rosalind_ins.txt")
x = readstring(f)
x = split(x, "\n")
array = readdlm(IOBuffer(x[2]), Int)
close(f)
@time InsertionSort(array)

A = randcycle(10000)
println("Merge Sort")
A = randcycle(10000)
@time mergesort!(A)
A = randcycle(10000)
@time mergesort!(A)


println("Julia sort")
A = randcycle(10000)
@time sort!(A)
A = randcycle(10000)
@time sort!(A)
