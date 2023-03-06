#include <bits/stdc++.h>

using namespace std;

void randomArr(vector<int> &a, int n) {
    int k=n/2;
    for (int i = 0; i < n; i++) {
        a[i] = rand() % k + 1;
    }
}

void printData(int n, int r, int q, vector<int> &a) {
    
    cout << n << ' ' << r << ' ' << q << '\n';
    for (auto x : a) cout << x << ' ';
    cout << '\n';
    int p;
    for (int i = 0; i < q; i++)
    {
        
        p = rand() % n;
        cout << p << '\n';
    }
}

void generate(int t) {
    cout<<t<<'\n';
    for(int i=0;i<t;i++)
    {
    int n = rand()%10 + 1;
    if(n%2!=0)
    n++;
    int r = rand() % n + 1;
    int q = rand() % n + 1;
    

    vector<int> a(n);

    randomArr(a, n);

    printData(n, r, q, a);
    }
}



int main() {
    string filename = "sample1.txt";
    srand(time(0));

    freopen(filename.c_str(), "w", stdout);
    
    generate(5);
    

    return 0;
}