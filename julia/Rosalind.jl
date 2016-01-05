# # Rosaling problem count dna letters

function Count_DNA(seq::AbstractString)
    Count = Dict{AbstractString,Int64}("A"=>0, "T" => 0, "G"=>0, "C" => 0)

    for i in seq
        Count["$i"] += 1
    end

    return Count
end

println("Warmup of function")
@time x = Count_DNA("AGCT")
println("Test")
@time x = Count_DNA("AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC")
println(x)

f = open("/home/akopp/Downloads/rosalind_dna.txt")
dna = readall(f)
dna = replace(dna, "\n", "")
close(f)
println("Apply on Data")
@time x = Count_DNA(dna)
println(x)


# Rosalind problem Counting point mutation between two sequences

function CountPointMutation(s::AbstractString, t::AbstractString)
    Count = 0
    for i = 1:length(s)
        if s[i] != t[i]
            Count += 1
        end
    end
    return Count
end

println("Warmup and test")
@time y = CountPointMutation("GAGCCTACTAACGGGAT", "CATCGTAATGACGGCCT")

f = open("/home/akopp/Downloads/rosalind_hamm.txt")
seq = readall(f)
x = split(seq, '\n')
close(f)
println("Apply on Data")
@time y = CountPointMutation(x[1], x[2])
println(y)
