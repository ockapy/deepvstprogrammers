#include <iostream>
#include <vector>
#include <unordered_map>
#include <chrono>
#include <array>

class TestListVSDict {
public:
    TestListVSDict(int size = 155) 
        : list(size, 0), array(), npArray(size, 0) {
        this->size = size;
        for (int i = 0; i < size; ++i) {
            array[i] = 0;
        }
    }

    void setList(int i, int x) {
        list[i] = x;
    }

    void setDict(int i, int x) {
        dict[i] = x;
    }

    void setArray(int i, int x) {
        array[i] = x;
    }

    void setNpArray(int i, int x) {
        npArray[i] = x;
    }

private:
    std::vector<int> list;
    std::unordered_map<int, int> dict;
    std::array<int, 155> array;
    std::vector<int> npArray;
    int size;
};

int main() {
    int size = 155;
    int repeat = 100000;
    TestListVSDict testListVSDict(size);

    auto start = std::chrono::high_resolution_clock::now();
    for (int rep = 0; rep < repeat; ++rep) {
        for (int i = 0; i < size; ++i) {
            testListVSDict.setNpArray(i, i);
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "NP Array " << elapsed.count() << std::endl;

    start = std::chrono::high_resolution_clock::now();
    for (int rep = 0; rep < repeat; ++rep) {
        for (int i = 0; i < size; ++i) {
            testListVSDict.setList(i, i);
        }
    }
    end = std::chrono::high_resolution_clock::now();
    elapsed = end - start;
    std::cout << "List " << elapsed.count() << std::endl;

    start = std::chrono::high_resolution_clock::now();
    for (int rep = 0; rep < repeat; ++rep) {
        for (int i = 0; i < size; ++i) {
            testListVSDict.setDict(i, i);
        }
    }
    end = std::chrono::high_resolution_clock::now();
    elapsed = end - start;
    std::cout << "Dict " << elapsed.count() << std::endl;

    start = std::chrono::high_resolution_clock::now();
    for (int rep = 0; rep < repeat; ++rep) {
        for (int i = 0; i < size; ++i) {
            testListVSDict.setArray(i, i);
        }
    }
    end = std::chrono::high_resolution_clock::now();
    elapsed = end - start;
    std::cout << "Array " << elapsed.count() << std::endl;

    return 0;
}
