
function sum_divisor(n)
    sum = 0
    i = 1
    while i < n
        if n % i == 0
            sum += i
        end
        i += 1
    end
    return sum
end


function sum_amicable_pairs(low, high)
    a = low
    b = 0
    sum = 0
    while a <= high
        b = sum_divisor(a)
        if b > a && sum_divisor(b) == a
            sum += (a + b)
        end
        a += 1
    end
    return sum
end

println(sum_amicable_pairs(1, 10000))
