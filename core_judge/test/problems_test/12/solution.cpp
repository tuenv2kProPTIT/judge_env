#include<stdio.h>
#include<math.h>

int main()
{
    int a,b,c,d;
    scanf("%d%d%d%d",&a,&b,&c,&d);
    c-= d;
    float delta = b*b - 4*a*c;
    if(a == 0)
    {
        
       if(b!=0)
       {
           printf("%.5f\n",(float)(-c)/b);
       }
       else
       {
           if(c == 0) printf("Infinity\n");
           else printf("NO\n");
       }
    }
    else
    if(delta < 0) printf("NO\n");
    else if(delta == 0)
    {
        printf("%.5f\n",(float)(-b)/(2*a) );
    }
    else{
        float sdelta = sqrt(delta);
        float x1 = (float)(-b-sdelta)/(2*a);
        float x2 = (float)(-b+sdelta)/(2*a);
        printf("%.5f %.5f\n", x1,x2);
    }
    return 0;



}
