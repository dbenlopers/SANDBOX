# Playzone


function one_sample_ttest(arr::Array{}, testmean)
    sample_size = length(arr)
    if sample_size < 2
        quit("Array must be more populated")
    end
    sample_mean = mean(arr)
    sample_std = std(arr)
    t = (sample_mean - testmean)/(sample_std/sqrt(sample_size))
end

function two_sample_ttest(arr1::Array{}, arr2::Array{})
    t = (mean(arr1) - mean(arr2)) / ()
end
