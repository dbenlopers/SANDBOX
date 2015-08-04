
function sumFibo(x)
    sum = 0
    term_1 = 1
    term_2 = 2
    term_3 = 0
    
    while term_1 <= x
        if term_1 % 2 == 0
            sum += term_1
        end
        term_3 = term_1 + term_2
        term_1 = term_2
        term_2 = term_3
    end
    return sum
    
    end
