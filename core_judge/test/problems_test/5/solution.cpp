#include <bits/stdc++.h>

using namespace std;

int main(){
	
	int n; cin >> n;
	int cnt = 0;
	int tt;
	while(1){
		char c;
		cin>>c;
		cin>>tt;
		if(c=='!')break;
		if(tt > n){
			cout<<">"<<endl;
			fflush(stdout);
		}
		else
		{
			if(tt < n){
				cout<<"<"<<endl;fflush(stdout);
			}
			else
			{
				cout<<"="<<endl;fflush(stdout);
			}
			
		}
		cnt+=1;
		if(cnt > 60){
			cout<<"You ask more than 60 question!!!"<<endl;
			fflush(stdout);
			return 0;
		}
	}
	if(tt==n){
		cout<<"AC"<<endl;
		fflush(stdout);
		
	}
	else {
		cout<<"WA"<<endl;
		fflush(stdout);
	}
	
	return 0;
}

