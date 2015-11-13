float accumulate(const std::vector<float>& v)
{
    // copy the length of v and a pointer to the data onto the local stack
    const size_t N = v.size();
    const float* p = (N > 0) ? &v.front() : NULL;

    __m128 mmSum = _mm_setzero_ps();
    size_t i = 0;

    // unrolled loop that adds up 4 elements at a time
    for(; i < ROUND_DOWN(N, 4); i+=4)
    {
        mmSum = _mm_add_ps(mmSum, _mm_loadu_ps(p + i));
    }

    // add up single values until all elements are covered
    for(; i < N; i++)
    {
        mmSum = _mm_add_ss(mmSum, _mm_load_ss(p + i));
    }

    // add up the four float values from mmSum into a single value and return
    mmSum = _mm_hadd_ps(mmSum, mmSum);
    mmSum = _mm_hadd_ps(mmSum, mmSum);
    return _mm_cvtss_f32(mmSum);
}

To increase performance even further, we can add more _mm_add_ps calls to the body of the unrolled loop. In order
to add up 16 floats in a single iteration, insert the snippet below after the size_t i = 0; To increase performance
even further, we can add more _mm_add_ps calls to the body of the unrolled loop. In order to add up 16 floats in a
single iteration, insert the snippet below after the size_t i = 0;

for(; i < ROUND_DOWN(N, 16); i+=16)
{
    mmSum = _mm_add_ps(mmSum, _mm_loadu_ps(p + i + 0));
    mmSum = _mm_add_ps(mmSum, _mm_loadu_ps(p + i + 4));
    mmSum = _mm_add_ps(mmSum, _mm_loadu_ps(p + i + 8));
    mmSum = _mm_add_ps(mmSum, _mm_loadu_ps(p + i + 12));
}

While this code reduces the loop-overhead, it does not maximize performance. Modern CPUs are capable of executing two
operations at the same time using multiple execution units. It is therefore possible to execute multiple SSE commands
simultaneously by obeying a simple rule: do not read from the register you have just written. In other words, if you use
two mutually data-independent instructions, both instructions can be either executed at the same time using instruction
 paring or at least allow to hide latencies.

In our unrolled accumulation code we can for example break the dependency chain on the mmSum register by introducing
intermediate registers that contain partial sums:

for(; i < ROUND_DOWN(N, 16); i+=16)
{
    __m128 v0 = _mm_loadu_ps(p + i + 0);
    __m128 v1 = _mm_loadu_ps(p + i + 4);
    __m128 s01 = _mm_add_ps(v0, v1);

    __m128 v2 = _mm_loadu_ps(p + i + 8);
    __m128 v3 = _mm_loadu_ps(p + i + 12);
    __m128 s23 = _mm_add_ps(v2, v3);

    mmSum = _mm_add_ps(mmSum, s01);
    mmSum = _mm_add_ps(mmSum, s23);
}
