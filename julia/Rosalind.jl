# Rosaling problem 1

function Count_DNA(seq::AbstractString)
    Count = Dict{AbstractString,Int64}("A"=>0, "T" => 0, "G"=>0, "C" => 0)

    for i in seq
        Count["$i"] += 1
    end

    return Count
end

@time x = Count_DNA("AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC")
@time x = Count_DNA("AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC")

println(x)

f = open("/home/akopp/Downloads/rosalind_dna.txt")
dna = readall(f)
dna = replace(dna, "\n", "")
close(f)

@time x = Count_DNA(dna)

println(x)
