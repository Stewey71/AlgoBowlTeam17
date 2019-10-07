# AlgoBowlTeam17
Repo for AlgoBowl Team 17

Note on Files:
+ inputCreator.py generates an input in the createdInput.txt file
+ Heuristic.py finds the best output given an input
+ verifier.py verifies inputs for correctness

CSCI 406: AlgoBOWL

Reminder: You are NOT allowed to consult the internet to solve this problem.

1 Problem Description

You are given
	
	1. A universal set U of n elements {1, 2, 3, . . . n}.
	
	2. A list S1, S2, . . . Sm of subsets of U such that the union of the m subsets gives U.
	
	3. The weight wi of each subset Si.

A cover is defined as a collection of subsets whose union is equal to U. The goal is to find a cover
whose total weight is minimized.

Input Format: Line 1 of the input contains n, the number of elements in U. Line 2 contains m, the
number of subsets of U. Each of the next m pairs of lines specifies a subset Si and its weight wi. 
In the example that follows, I’ve included comments for your understanding. Comments should not
be included in actual inputs:

5                                                          // U = {1, 2, 3, 4, 5}

3                                                          // Three subsets: S1, S2, S3.

1 2 3                                                      // S1 = {1, 2, 3}

15                                                         // w1

4 5                                                        // S2 = {4, 5}

6                                                          // w2

1 2 3 4 5                                                  // S3 = {1, 2, 3, 4, 5}

26                                                         // w3

We have: S1 = {1, 2, 3} with weight w1 = 15, S2 = {4, 5} with weight w2 = 6, S3 = {1, 2, 3, 4, 5}
with weight w3 = 26. (Notice that S3 = U, but this is okay because a set can be a subset of itself.)

Two possible covers are C1 = {S1, S2} and C2 = {S3}. Their weights are 15 + 6 = 21 and 26,
respectively, making C1 the better solution.

Input Restrictions: Assume n ≤ 1000 and m ≤ 500. Each weight must be an integer in [1,1000].

Output Format: Line 1 of your output will contain the best weight that your algorithm was able to
find. The next line will contain the IDs of the sets included in your cover. To illustrate, the output
for cover C1 in the example is

21

1 2

Note: This problem is NP-hard, which means that it is unrealistic to expect that your
algorithm will compute an optimal solution in a reasonable time frame. Please keep
this in mind as you work on this project.
