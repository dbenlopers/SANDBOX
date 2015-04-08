#include <iostream>
#include <memory>
#include <vector>
#include <time.h>
#include <algorithm>

struct LargeData {
    LargeData(int id_) : id(id_)
    {}
    int id;
    int arr[100];
};

struct Foo {
    Foo() { std::cout << "Constructor : " << this << " Done" << std::endl; }
    virtual ~Foo() { std::cout << "Destructor : " << this << " Done" << std::endl;}
};

bool compare_by_value(const LargeData& a, const LargeData& b) {
    return a.id < b.id;
}

bool compare_by_ptr(const LargeData* a, const LargeData* b) {
    return a->id < b->id;
}


bool compare_by_uniqptr(const std::unique_ptr<LargeData>& a, const std::unique_ptr<LargeData>& b) {
    return a->id < b->id;
}


int main()
{
    std::cout << "Testing unique ptr" << std::endl;
    {
        std::cout << "Enter scope" << std::endl;
        std::unique_ptr<Foo> uptr(new Foo());
        std::cout << "Exit score" << std::endl;
    }
    
    std::vector<LargeData> vec_byval;
    std::vector<LargeData*> vec_byptr;
    
    int n = 100000 ;
     
    for (int i = 0; i < n; ++i) {
        int id = std::rand() % 500000;
        vec_byval.push_back(LargeData(id));
        vec_byptr.push_back(new LargeData(id));
    }
    
    int start_s = clock();
    std::sort(vec_byval.begin(), vec_byval.end(), compare_by_value);
    int stop_s = clock();
    std::cout << "By Val : time: " << (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000 << std::endl;

    start_s = clock();
    std::sort(vec_byval.begin(), vec_byval.end(), compare_by_value);
    stop_s = clock();
    std::cout << "By pointer : time: " << (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000 << std::endl;
    
    std::vector<std::unique_ptr<LargeData>> vec_byuniqptr;
    for (int i = 0; i < n; ++i) {
        int id = std::rand() % 500000;
        vec_byuniqptr.push_back(std::unique_ptr<LargeData>(new LargeData(id)));
    }

    start_s = clock();
    std::sort(vec_byuniqptr.begin(), vec_byuniqptr.end(), compare_by_uniqptr);
    stop_s = clock();    
    std::cout << "By unique pointer : time: " << (stop_s-start_s)/double(CLOCKS_PER_SEC)*1000 << std::endl;

    return 0;
}
