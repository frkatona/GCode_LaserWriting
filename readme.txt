Writes g-code file with automated looping and simplified inputs

CHANGELOG
6/23 - 1: more finely, faster, smaller
6/23 - 2: smaller-still, true origin start
6/23 - 3: chopped off cycle from 7 to 6 each way
6/23 - 4: cut step size 15->3 [repeat 6->30], upped speed so P could go 7->13 hopefully
6/24: developed python automation for writing loops and simplifying inputs
6/27: mostly surface after ~30-60min of 13A 808nm so trying back down in speed [3000->2000] and lower weight loading [5e-4 -> 5e-5]; also lowered length [210->180] for less fire and faster runtime

I recommend checking code changes with nraynaud's g-code simulator: https://nraynaud.github.io/webgcode/