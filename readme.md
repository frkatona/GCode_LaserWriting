# Writes g-code file with automated looping and simplified inputs in an xy grid with parallel scan lines
- "standard" for constant speed
- "ramp" for speed changes between scan cycles
- "animated-preview" is unfinished but should replace all existing functionality and also provide an animation preview of the scan path (see figure)

![animated-example](animated-example.png)

## CHANGELOG
- 8/16 - added cGPT-assisted ramp creator with animation (still in development, wastes time between loops)
- 6/23 1: more finely, faster, smaller
- 6/23 2: smaller-still, true origin start
- 6/23: 3: chopped off cycle from 7 to 6 each way
- 6/23: 4: cut step size 15->3 [repeat 6->30], upped speed so P could go 7->13 hopefully
- 6/24: developed python automation for writing loops and simplifying inputs
- 6/27: mostly surface after ~30-60min of 13A 808nm so trying back down in speed [3000->2000] and lower weight loading [5e-4 -> 5e-5]; also lowered length [210->180] for less fire and faster runtime

can check code changes with nraynaud's g-code simulator: https://nraynaud.github.io/webgcode/