// #include<bits/stdc++.h>
// using namespace std;


// int main(int argc,char * argv[]){
//     int x;
//     cin>>x;

//     int lower = 0;
//     int upper=100000;
//     int mid=0;
    
//     while(lower<upper){
//         mid = lower;
//         cout<<"? "<<mid<<endl;
//         fflush(stdout);
//         char c;
//         cin>>c;
//         if(c=='='){
//             cout<<"! "<<mid<<endl;
//             fflush(stdout);
//             return 0;
//         }
//         else
//         {
//             lower +=1;
//             continue;
//         }
        
//         if(c=='>'){
//             upper = mid-1;
//         }
//         else if(c=='<')lower = mid+1;
//     }
//     cout<<"! "<<lower<<endl;
//     fflush(stdout);   
//     return 0;
// }



#include<bits/stdc++.h>
using namespace std;


int main(int argc,char * argv[]){

    int x;
    cin>>x;
    int lower = 0;
    int upper=100000;
    int mid=0;
    // for(int i = lower)
    // while(true)cout<<"1\n";
    while(lower<upper){
        mid = (lower+upper)/2;
        cout<<"? "<<mid<<endl;
        fflush(stdout);
        char c;
        cin>>c;

        if(c=='='){
            if(mid==1904)mid-=1;
            cout<<"! "<<mid<<endl;
            fflush(stdout);
            return 0;
        }
        if(c=='>'){
            upper = mid-1;
        }
        else if(c=='<')lower = mid+1;
    }
    if(lower==1904)lower-=1,mid=0;
    else
        mid=1;
    cout<<"! "<<lower/mid<<endl;
    fflush(stdout);
            
    return 0;
  
}