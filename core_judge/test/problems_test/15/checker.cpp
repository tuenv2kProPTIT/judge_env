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
    
    int ouf_num_lines = ouf_data.size();
    int ans_num_lines = ans_data.size();
    if(ans_num_lines != ouf_num_lines){
        string l1, l2;
        if(ans_num_lines <= 1) l1 = "line";
        if(ans_num_lines > 1) l1 = "lines";
        if(ouf_num_lines <= 1) l2 = "line";
        if(ouf_num_lines > 1) l2 = "lines";
        quitf(_wa, "expected %d %s, got %d %s", ans_num_lines, l1.c_str(), ouf_num_lines, l2.c_str());
    }

    for(int i = 0; i < ans_num_lines; i++){
        vector<string> ans_row = tokenize(ans_data[i], " ");
        vector<string> ouf_row = tokenize(ouf_data[i], " ");
        int num_ans_row = ans_row.size();
        int num_ouf_row = ouf_row.size();
        if(num_ouf_row != ans_row.size()){
            quitf(_wa, "in line %d, expected %d elements, got %d elements", i, num_ans_row, num_ouf_row);
        }
        for(int j = 0; j < num_ans_row; j++){
            if(ans_row[j] != ouf_row[j]){
                quitf(_wa, "in line %d, at element %d", i, j);
            }
        }
    }
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