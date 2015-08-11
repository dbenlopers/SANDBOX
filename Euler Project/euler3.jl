N = 600851475143

function is_prime(number)
	for i in 2:ifloor(sqrt(number))
		if number % i == 0
			return false
		end
	end
	return true
end

function largest_factor(N)
	factor = 2
	L_factor = factor
	while factor <= N
		if N % factor == 0 && is_prime(factor)
			# println(factor)
			if factor > L_factor
				L_factor = factor
			end

			N = div(N, factor)
			factor = 2
		else
			factor += 1
		end
	end
	return L_factor
end

lar_factor = 0
iteration = 10000
i = 1
while i <= iteration
	lar_factor = largest_factor(N)
	i += 1
end
println(lar_factor)
