#include<bits/stdc++.h>

using namespace std;

int main(){
    int t;
    int res = 0;
    cin >> t;
    if (t > 30){
        t-=30;
        res = t*2000;
    }
    cout << res;
    return 0;
}