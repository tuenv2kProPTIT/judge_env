//Author: nghiatd_16
//Type: Default Checker - Ignore all white space

#include "testlib.h"
#include <string>
#include <vector>
using namespace std;


vector<string> read_data_from_stream(InStream &inS){
    vector<string> data;
    while(!inS.seekEof()){
        if(!inS.seekEoln()){
            data.push_back(inS.readLine());
        }
    }
    inS.close();
    return data;
}
void check(){
    vector<string> ans_data = read_data_from_stream(ans);
    vector<string> ouf_data = read_data_from_stream(ouf);
    if(ouf_data.size()==0){
        quitf(_wa,"may be jury ans isn't correct!!");
    }
    if(ouf_data[ouf_data.size()-1] !="AC"){
        quitf(_wa, "wa");
    }
    else
        quitf(_ok, "%s", "");
}
int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    try {
        check();
    } catch (const char* msg) {
        quitf(_fail, "%s", msg);
    }
}