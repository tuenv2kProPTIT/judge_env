#include<bits/stdc++.h>
using namespace std;
#define ii pair<int,int>
double area(ii a,ii b,ii c)
{
    double ans=0;
    ans=a.first*b.second-a.second*b.first;
    ans+=b.first*c.second-b.second*c.first;
    ans+=c.first*a.second-c.second*a.first;
    ans=fabs(ans)/2.0;
    return ans;
}
int main()
{
    ii F[3];
    for(int i=0;i<3;i++)cin>>F[i].first>>F[i].second;
    ii D;
    cin>>D.first>>D.second;

    double t1=area(D,F[0],F[1]),t2=area(D,F[0],F[2]),t3=area(D,F[1],F[2]);


    if(t1==0||t2==0||t3==0||t1+t2+t3!=area(F[0],F[1],F[2]))
    {
        cout<<"NO\n";
    }
    else cout<<"YES\n";
    return 0;

}
