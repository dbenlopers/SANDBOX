#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>
#include <future>
static void transmit_item(int i) 
{
    std::cout << i << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    // ...
}
static size_t transmit_log(const std::vector<int> & log)
{
    std::for_each(std::begin(log), std::end(log), transmit_item);
    return log.size();
}
int main()
{
    std::vector<int> log{20,24,37,42,23,45,37};
    auto res = std::async(std::launch::async, transmit_log, log);
    size_t items = res.get();
    std::cout << "# " << items << std::endl;
}
