    #include "testlib.h"

    #include<vector>

    int main(int argc, char * argv[]){
        registerTestlibCmd(argc,argv);
        int n=inf.readInt();
        int m=ouf.readInt();
        int anss = ans.readInt();
        int step =ouf.readInt();
        // int mm=ans.readInt();
        if(step>60){
            quitf(_wa,"you asked more than 60 queries");
        }
        else
        {
            if(m == n)
                quitf(_ok,"ok");
            else quitf(_wa,"jury has answer = %d\n participant has answer = %d\n",n,m);
        }
        return 0;
        
    }