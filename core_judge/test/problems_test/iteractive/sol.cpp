#include<bits/stdc++.h>
using namespace std;


int main(int argc,char * argv[]){
    // signal(SIGPIPE, SIG_IGN);
    // FILE *in = fopen(argv[1], "r");
    // FILE *out = fopen(argv[2], "w");
    // setvbuf(out, NULL, _IONBF, 0);
    int x;
    cin>>x;
    // fprintf(stderr,"%d\n",x);
    int lower = 0;
    int upper=100000;
    int mid=0;
    // for(int i = lower)
    
    while(lower<upper){
        mid = (lower+upper)/2;
        cout<<"? "<<mid<<endl;
        fflush(stdout);
        char c;
        cin>>c;
        // fprintf(stderr,"%d %c\n",mid,c);
        if(c=='='){
            cout<<"! "<<mid<<endl;
            fflush(stdout);
            return 0;
        }
        if(c=='>'){
            upper = mid-1;
        }
        else if(c=='<')lower = mid+1;
    }
    cout<<"! "<<lower<<endl;
    fflush(stdout);
            
    return 0;
    // int lower = 0;
    // int upper = 100000;
    // // int mid = -1;cin>>mid;
    // int mid=2000;
    // fscanf(in,"%d",&mid);
    // // cout<<"! "<<mid<<endl;
    // // fflus
    // // fflush(stdout);
    // // cout.flush();
    // upper=mid;
    // lower=mid-1;
    // cout<<"! "<<mid<<endl;
    // fprintf(out,"! %d\n",mid);
    // fflush(out);
    // return 0;
    // // return 0;
    // while(lower < upper){
    //     mid= (lower+upper)/2;
    //     cout<<"? "<<mid<<endl;
    //     fflush(stdout);
    //     char x;cin>>x;
    //     if(x=='='){
    //         cout<<"! "<<mid<<endl;
    //         fflush(stdout);
    //         return 0;
    //     }
    //     if(x=='>'){
    //         upper = mid-1;
    //     }
    //     else if (x=='<')lower = mid+1;
    // }
    // cout<<"! "<<mid<<endl;
    // fflush(stdout);
    // return 0;
}