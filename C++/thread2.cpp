#include <cmath>
#include <thread>
#include <vector>

void parallelFor(const unsigned int size, std::function<void(const unsigned int)> func) {
    const unsigned int nbThread = std::thread::hardware_concurrency();
    std::vector<std::thread> threads;
    for (unsigned int idThread = 0; idThread < nbThread; idThread++) {
        auto threadFunc = [=, &threads]() {
	    for (unsigned int i = idThread; i< size; i+=nbThread) {
		func(i);
	    }
	};
	threads.push_back(std::thread(threadFunc));
    }
    for (auto & t : threads) t.join();
}

int main() {
   unsigned int size = 1e8;
   std::vector<double> vect(size);
   auto myFunc = [=, &vect](unsigned int i) {
	vect[i] = sin(2*M_PI*i/(double)size);
   };
   parallelFor(size, myFunc);
   return 0;
}
