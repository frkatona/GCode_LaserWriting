newfile = 'gcodeoutput/apk_casserolescan.gcode' # puts written file into the gcodeoutput folder.  Change filename here
overwrite = 'w' # x = not allowed (raises error); w = allowed
speed = 3000 # speed in mm/min
stepsize = 3 # distance between rows
rowsize = 210 # length of rows
time = 3 # approximate desired hours for entire script to run (user should err high)
n_inloop = round(rowsize/(stepsize*2))
dist_inloop = (stepsize + rowsize) * 2 * n_inloop # approximate distance travelled in mm through entire execution (fudged a bit to make time more accurate)
n_outloop = round(time/speed * dist_inloop) # number of times to execute script given time and distance inputs

# g-code single-use (outer-looped) commands
home_xy = 'G28 X0 Y0 F4200\n\n' # code start, home X and Y at same time
init_abs = 'G90\n' # initialize absolute movement for start position
pos_start = 'G0 X0 Y0 Z 50 F4200\n' # move to origin position between external loop iterations at max speed
init_rel = 'G91\n\n\n' # initialize relative movement for scans

# g-code inside-looped commands
loop1 = 'G0 Y{} F{}\nG0 X{}\nG0 Y-{}\n'.format(rowsize, speed, stepsize, rowsize)
loop1_tail = 'G0 X{}\n'.format(stepsize)
loop2 = 'G0 X-{} F{}\nG0 Y{}\nG0 X{}\n'.format(rowsize, speed, stepsize, rowsize)
loop2_tail = 'G0 Y{}\n'.format(stepsize)

with open(newfile, overwrite) as f:
    f.writelines([home_xy])
    for x in range(n_outloop):
    
        f.writelines([init_abs, pos_start, init_rel])    

        for i in range(n_inloop):
            f.writelines(loop1)
            if i < (n_inloop - 1): # skips 'step' on final iteration to smoothly loop back
                f.writelines(loop1_tail)

        f.writelines('\n')

        for i in range(n_inloop):
            f.writelines(loop2)
            if i < (n_inloop - 1):
                f.writelines(loop2_tail)
        
        f.writelines('\n\n\n')