#include <iostream>
#include "testlib.h"
using namespace std;
#define ii pair<int,int> 
bool isNotok(ii a, ii b, ii c)
{
    if (a == b || b == c || c == a)
        return false;

    if (a.first == b.first)
    {

        return (c.first == a.first);
    }
    if (a.second == b.second)
        return (c.second == a.second); // y=const

    int t = (c.first - a.first) * (b.second - a.second);
    int tt = (c.second - a.second) * (b.first - a.first);

    return (t == tt);
}
int main(int argc, char* argv[]) {
    
    

    return 0;
}

// inf: luong file input
// ouf: luong file output cua thi sinh
// ans: luong file output chuan