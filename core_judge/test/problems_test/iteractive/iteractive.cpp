// #include<bits/stdc++.h>
// #include "testlib.h"
// using namespace std;

// void send(char x){
//     printf("%c\n",x);
//     fflush(stdout);
//     fclose(stdout);
    
// }

// int main(int argc, char * argv[]){
//     registerInteraction (argc,argv);

//     // quitf(_wa,"wrong answer");
//     int n = inf.readInt();
//     // int n;
//     int queries = 0;
//     tout<<n<<endl;
//     cout<<n<<endl;
//     fflush(stdout);
//     fclose(stdout);
//     registerInteraction(argc,argv);
//     // FILE *xxx;
//     // xxx= fopen("./in.txt","w");
//     // fprintf(xxx,"%d\n",n);
//     // return 0;
//     // ouf.readEof();
//     // while(ouf.seekEof())continue;
//     int c=60;
//     while(c--){
//         // char cmd ;
//         // ouf.readEof();
//         // if(ouf.seekEof())continue;
//         // string cmd = ouf.readToken("[!?]{1,1}");
//         // ouf
//         // fflush(stdin);
//         // ouf.init(stdin, _output);
//         char cmdx ;
//         cmdx=ouf.readChar(cmdx);
//         tout<<int(cmdx)<<endl;
//         int par_ans =ouf.readInt();
//         // cin>>par_ans;
//         tout<<par_ans<<endl;
//         // n = inf.readInt();
//         if(cmdx=='!'){
//             // int par_ans ;cin>>par_ans;
//             tout<<par_ans<<endl;
//             // ouf.readEof();
//             if(par_ans == n){
//                 // tout<<par_ans<<endl;
//                 // ouf.readEof();
                
//                 quitf(_ok,"passed");
//             }
//             else
//             {
//                 // tout<<par_ans<<endl;
//                 quitf(_wa,"NOT PASSSED");
//             }
            
//         }
//         else
//         {
//             queries+=1;
//             if(queries > 60){
//                 tout <<"-1\n";
//                 quitf(_wa,"Queries limited");
//                 return 0;
//                 break;
//             }
//             else
//             {
//                 // int que_par = ouf.readInt();
//                 int que_par = par_ans;
//                 if(que_par > n)send('>');
//                 else if (que_par==n) send('=');
//                 else if(que_par < n)send('<');
//                 registerInteraction(argc,argv);
//             }
            
//         }
        
//     }
//     quitf(_wa,"Queries limited");
//     return 0;
// }

#include<bits/stdc++.h>
#include "testlib.h"
using namespace std;

int main(int argc,char* argv[]){
    signal(SIGPIPE, SIG_IGN);
    ouf.init(stderr,_output);
    // registerTestlibCmd
    // for(int i = 0;i<argc;i++)cout<<argv[i]<<endl;
    FILE* fcommout = fopen(argv[2], "w");
    // cout<<"here"<<endl<<fcommout<<endl;
	FILE* fcommin = fopen(argv[1], "r");
    
    setvbuf(fcommout, NULL, _IONBF, 0);
    // cout<<"here"<<endl<<fcommin<<endl;
    // setvbuf(fcommout, NULL, _IONBF, 0);
    int n=34;
    cin>>n;
    fprintf(fcommout,"%d\n",n);
    fflush(fcommout);
    // cout<<n<<endl;
    int offset = 60;
    
    while(offset--){
        char c;
        while(fscanf(fcommin,"%c",&c)==1){
            if (c==' ' || c == '\n' || c=='\r')continue;
            else break;
        }
        if(c!='!' && c!='?'){
            
            cout<<"WA errors handle IO c or fail fomat "<<c<<" "<<int(c);
            quitf(_wa,"errors handle IO");
        }
        
        // cout<<c<<" here";
        int m;
        if(fscanf(fcommin,"%d",&m)!=1){
            cout<<"WA errors handle IO d";
            quitf(_wa,"errors handle IO x");
        }
        // cout<<c<<' ';
        // cout<<m<<" here"<<endl;
        if(c=='!'){
            if(m!=n){
                // cout<<"WA jury has answer = "<<n<<"\nparticipant has answer = "<<m<<endl;
                cout<<m<<endl<<60-offset<<endl;
                quitf(_wa,"WA answer");
            }
            else
            {
                // cout<<"AC";
                cout<<m<<endl;
                cout<<60-offset<<endl;
                quitf(_ok,"AC rui");
            }
            
        }
        else
        {
            if(m>n){
                fprintf(fcommout,">\n");
                fflush(fcommout);
            }
            else if(m<n)
            {
                
                fprintf(fcommout,"<\n");
                fflush(fcommout);
            }
            else
            {
                fprintf(fcommout,"=\n");
                fflush(fcommout);
            }
            
            
        }
        
    }
    cout<<n-1<<endl;
    cout<<61<<endl;
    quitf(_wa,"you asked more than 60 queries");
    return 0;
}