#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <type_traits>
template <typename T>
static void transmit_item(T i)
{
    static_assert(std::is_integral<T>::value, "integral type expected");
    std::cout << i << std::endl;
    // ...
}
template <typename Log, typename Filt>
static void transmit_log(Log && log, Filt myfilter)
{
    log.erase(std::remove_if(std::begin(log), std::end(log), myfilter),
              std::end(log));
    std::sort(std::begin(log), std::end(log));
    std::for_each(std::begin(log), std::end(log),
                  transmit_item<typename Log::value_type>);
}
int main()
{
    using log_item_type = long;
    std::vector<log_item_type> log{20,24,37,42,23,45,37};
    transmit_log(std::move(log), [](log_item_type i) { return i <= 23; });
}
