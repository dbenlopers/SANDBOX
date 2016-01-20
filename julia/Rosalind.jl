## Rosaling problem count dna letters

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

f = open("/home/akopp/Documents/RosalindInput/rosalind_dna.txt")
dna = readall(f)
dna = replace(dna, "\n", "")
close(f)
println("Apply on Data")
@time x = Count_DNA(dna)
println(x)


## Rosalind problem Counting point mutation between two sequences

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

f = open("/home/akopp/Documents/RosalindInput/rosalind_hamm.txt")
seq = readall(f)
x = split(seq, '\n')
close(f)
println("Apply on Data")
@time y = CountPointMutation(x[1], x[2])
println(y)


## Rosalind RNA to protein

function ReadTable(FilePath::AbstractString)
    table = Dict{ASCIIString, ASCIIString}()
    f = open(FilePath)
    for line in readlines(f)
        x = split(replace(line, "\n", ""), " ")
        table[x[1]] = x[2]
    end
    close(f)
    return table
end

rnatable = ReadTable("/home/akopp/Documents/RosalindInput/RNAcodontable.txt")

function RnaToProtein(table::Dict, rnaseq::AbstractString)
    protseq = Array{ASCIIString,1}()
    for i in range(1, 3, Int(round(length(rnaseq)/3)))
        push!(protseq, table[rnaseq[i:i+2]])
    end
    return join(protseq)
end

f = open("/home/akopp/Documents/RosalindInput/rosalind_prot.txt")
seq = readall(f)
seq = replace(seq, "\n", "")
close(f)

x = RnaToProtein(rnatable, seq)
println(x)

## Rosalind Find a motif in DNA

function SearchMotif(seq::AbstractString, motif::AbstractString)
    position = Array{Int, 1}()
    motle = length(motif)
    for i = 1:length(seq)-motle
        if seq[i:i+motle-1] == motif
            push!(position, i)
        end
    end
    return join(position, " ")
end

f = open("/home/akopp/Documents/RosalindInput/rosalind_subs.txt")
all = readall(f)
x = split(all, "\n")
close(f)
@show SearchMotif(x[1],x[2])

## Rosalind gc content

function gc(seq::AbstractString)
    total = length(seq)
    gc = length(matchall(r"G", seq)) + length(matchall(r"C", seq))
    return (gc/total) * 100
end

# @printf "%0.6f\n" gc("CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGACTGGGAACCTGCGGGCAGTAGGTGGAAT")

f = open("/home/akopp/Documents/RosalindInput/rosalind_gc.txt")
CurID = ""
CurSeq = Array{ASCIIString,1}()
for line in readlines(f)
    if line[1] == '>'
        if length(CurSeq) > 1
            @printf "%s %0.6f\n" CurID gc(join(CurSeq, ""))
        end
        CurSeq = Array{ASCIIString,1}()
        CurID = replace(line[2:end], "\n", "")
    else
        push!(CurSeq, replace(line, "\n", ""))
    end
end
@printf "%s %0.6f\n" CurID gc(join(CurSeq, ""))
close(f)

## Rosalind Protein mass

function AAMassTable(FilePath::AbstractString)
        table = Dict{ASCIIString, Float64}()
        f = open(FilePath)
        for line in readlines(f)
            x = split(replace(line, "\n", ""), "   ")
            table[x[1]] = parse(Float64, x[2])
        end
        close(f)
        return table
end

x = AAMassTable("/home/akopp/Documents/RosalindInput/AAMassTable.txt")

function ProteinMass(ProtSeq::AbstractString, AAMassTable::Dict)
    Mass = 0
    for AA in ProtSeq
        Mass += AAMassTable[string(AA)]
    end
    return Mass
end

f = open("/home/akopp/Documents/RosalindInput/rosalind_prtm.txt")
seq = readall(f)
seq = replace(seq, "\n", "")
close(f)

mass = ProteinMass(seq, x)
@printf "%0.8f\n" mass


## Rosalind calculating expected offsprings

function eo()
    dominance = [1.0, 1.0,1.0,0.75,0.5,0]
    arr = [17102, 18069, 19708, 17266, 16780, 18940]
    exp = 0
    for i = 1:6
        exp += 2*arr[i]*dominance[i]
    end
    return exp
end
println(eo())
