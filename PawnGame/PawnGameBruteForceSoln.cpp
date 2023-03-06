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
//typedef long long ll;


char f(vector<char> &s,int t,int i,int r,vector<int>& v,int n)
{
	if(t==2*r-1&&i-v[i]>=0&&i-v[i]<(n/2))
	return 'B';
	else if(t==2*r-1&&i+v[i]<n&&i+v[i]<(n/2))
	return 'B';
	else if(t==2*r-1)
	return 'A';
	
	if(t%2==0)
	{
		char a,b;
		if(i+v[i]<n)
		{
		  a=f(s,t+1,i+v[i],r,v,n);
		if(a=='A')
		{
		return 'A';
	    }
	    }
		if(i-v[i]>=0)
		{
		b=f(s,t+1,i-v[i],r,v,n);	
		if(b=='A')
		return 'A';
	    }
		else
		{
		return 'B';
	    }
	}
	else
	{
    	if(i+v[i]<n)
		{
		
		if(f(s,t+1,i+v[i],r,v,n)=='B')
		return 'B';
	    }
		if(i-v[i]>=0)
		{
		
		if(f(s,t+1,i-v[i],r,v,n)=='B')
		return 'B';
	    }
		else
		return 'A';
	}
	
}

int main()
{
	int T;
	cin>>T;
	while(T--)
	{	
	int n,r,i,t,q;
	cin>>n>>r>>q;
	vector<int> v(n);
    vector<char> s(n),s1(n);
	for(i=0;i<n;i++)
	cin>>v[i];
	
	for(i=0;i<n;i++)
	{
		if(i-v[i]>=0&&i-v[i]<(n/2))
		s[i]='B';
		else if(i+v[i]<n&&i+v[i]<(n/2))
		s[i]='B';
		else
		s[i]='A';
		s1[i]=s[i];
	}
	
	for(i=0;i<n;i++)
	{
		for(t=2*r-2;t>=0;t--)
		{
			s1[i]=f(s,t,i,r,v,n);
		}
	}
	

    
	
	while(q--)
	{
		int pos;
		cin>>pos;
		if(s1[pos]=='A')
		cout<<"ALICE";
		else
		cout<<"BOB";
		cout<<"\n";
	}
}
	
	
}
