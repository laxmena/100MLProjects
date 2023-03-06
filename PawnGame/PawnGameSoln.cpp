/*
Problem:
Alice and Bob play a game. They are given an array A of N numbers and a pawn.
If the pawn is at the ith position, the player can either move the pawn by
Ai units to the right or Ai units to the left, i.e. the new position of the
pawn is i+Ai or i-Ai, but the new position must lie between [0,n-1].
The game goes on for R rounds, in each round Alice and Bob get one move each.

If at the end of R rounds, the pawn lies in the right half of the array [n/2,n-1],
Alice wins.

If at the end of R rounds, the pawn lies in the left half of the array [0,n/2-1],
Bob wins.

You are given Q queries where each query is a single integer p, which denotes the
position of the pawn before the game starts.

Alice starts the game.
N is even.
0 <= Ai <= (N/2).

For each query of each test case, print the winner of the game after R rounds.
If Alice wins, print "AlICE".
If Bob wins, print "BOB".


INPUT FORMAT:

The first line of input data contains single integer t - number of test cases.

The first line of each test case contains three integers N,R,Q.
N- Number of elements in the array. [N is even]
R- Number of Rounds.
Q- Number of Queries.

The second line of each test case contains N integers A0,A1....A(N-1) [0 <= Ai <= (N/2)].

The next Q lines of each test case contain an integer p. [0 <= p <= N-1]
p- position of the pawn before starting the game.


OUTPUT FORMAT:

For each test case, print on Q lines, the winner for each query.


*/




#include<iostream>
#include<math.h>
#include<string.h>
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;


int main()
{
	int T;
	cin>>T;
	while(T--)
	{	
	ll n,r,i,t,q;
	cin>>n>>r>>q;
	vector<ll> v(n);
	char dp[n][2];
	for(i=0;i<n;i++)
	cin>>v[i];
	
	for(i=0;i<n;i++)
	{
		if(i-v[i]>=0&&i-v[i]<(n/2))
		dp[i][0]='B';
		else if(i+v[i]<n&&i+v[i]<(n/2))
		dp[i][0]='B';
		else
		dp[i][0]='A';
	}
	
	for(t=0;t<=2*r-2;t++)
	{
		if(t%2==0)
		{   for(i=0;i<n;i++)
			    {
				if(i-v[i]>=0&&dp[i-v[i]][0]=='A')
			    dp[i][1]='A';
				else if(i+v[i]<n&&dp[i+v[i]][0]=='A')
				dp[i][1]='A';
				else
				dp[i][1]='B';
			    }
		}
		else
		{
			for(i=0;i<n;i++)
				{
				if(i-v[i]>=0&&dp[i-v[i]][1]=='B')
			    dp[i][0]='B';
				else if(i+v[i]<n&&dp[i+v[i]][1]=='B')
				dp[i][0]='B';
				else
				dp[i][0]='A';
			    }
		}
		
	}

	
	while(q--)
	{
		ll pos;
		cin>>pos;
		if(dp[pos][1]=='A')
		cout<<"ALICE";
		else
		cout<<"BOB";
		cout<<"\n";
	}
}
	
	
}
/*
1
10 1 10
3 2 4 1 1 3 5 1 2 4
0
1
2
3
4
5
6
7
8
9
*/
