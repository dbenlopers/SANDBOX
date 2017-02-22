
function sumBelow(x)
    sum = 0
    for i = 1:x-1
        if i % 3 == 0
            sum += i
        elseif i % 5 == 0
            sum += i
        end
    end
    return sum
end


println(sumBelow(1000))
