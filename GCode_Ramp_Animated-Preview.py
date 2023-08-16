import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

# Parameters
X_max = 250  # Total X dimension (mm)
Y_max = 250  # Total Y dimension (mm)
V_init = 5000  # Initial speed (mm/min)
delta_V = 500  # Amount of speed to subtract after each cycle (mm/min)
V_floor = 300  # Floor speed (mm/min)
delta_y = 5  # Scan line separation (mm)
line_thickness = 10  # Line thickness (mm)
n_scan_lines = int(X_max / delta_y)  # Number of scan lines per cycle

# Generate the G-code for scans parallel to the Y-axis with movements constrained to a single axis at a time
gcode = []
gcode.append('G28 X0 Y0 F5000 ; Home X and Y axes\n')
gcode.append('G91 ; Initialize relative movement\n\n')

speed = V_init
while speed >= V_floor:
    for i in range(n_scan_lines):
        # Move up along Y-axis
        gcode.append(f'G0 Y{Y_max} F{speed}\n')
        # Move right along X-axis if not the last line
        if i < n_scan_lines - 1:
            gcode.append(f'G0 X{delta_y} F{speed}\n')
        # Move down along Y-axis
        gcode.append(f'G0 Y-{Y_max} F{speed}\n')
        # Move right along X-axis if not the last line
        if i < n_scan_lines - 1:
            gcode.append(f'G0 X{delta_y} F{speed}\n')
    # Reset X position after each raster cycle
    gcode.append(f'G0 X-{(n_scan_lines - 1) * 2 * delta_y} F{speed}\n')
    # Reduce speed for the next raster cycle
    speed -= delta_V

# Extract X and Y positions from the G-code
x_pos, y_pos = 0, 0
positions = [(x_pos, y_pos)]

for line in gcode:
    if line.startswith('G0'):
        instructions = line.split()
        for instruction in instructions:
            if instruction.startswith('X'):
                x_pos += float(instruction[1:])
            elif instruction.startswith('Y'):
                y_pos += float(instruction[1:])
        positions.append((x_pos, y_pos))

# Find the index of the command that resets the X position after the first raster cycle
reset_index = None
for i, line in enumerate(gcode):
    if line.startswith('G0 X-') and i > 10:
        reset_index = i
        break

# Extract positions for the first 3 cycles
positions_three_cycles = positions[:reset_index * 3 + 3]

# Extract coordinates from positions
x_vals_three_cycles = [pos[0] for pos in positions_three_cycles]
y_vals_three_cycles = [pos[1] for pos in positions_three_cycles]

# Calculate the time for each movement segment based on speed and distance for the first 3 cycles
times_three_cycles = [0]  # Initialize with time = 0 at the start
for i in range(1, len(positions_three_cycles)):
    dx = positions_three_cycles[i][0] - positions_three_cycles[i-1][0]
    dy = positions_three_cycles[i][1] - positions_three_cycles[i-1][1]
    distance = np.sqrt(dx**2 + dy**2)
    time_segment = distance / V_init * 60  # Convert speed from mm/min to mm/s
    times_three_cycles.append(times_three_cycles[-1] + time_segment)

# Create the MP4 animation for the first 3 cycles
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, X_max)
ax.set_ylim(0, Y_max)
ax.set_xlabel('X Axis (mm)')
ax.set_ylabel('Y Axis (mm)')
lc = LineCollection([], linewidth=line_thickness, alpha=0.5, color='blue')
ax.add_collection(lc)
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)

def update(num, x_vals, y_vals, times, lc, time_text):
    points = np.array([x_vals[:num+1], y_vals[:num+1]]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc.set_segments(segments)
    time_text.set_text(f'Time: {times[num]:.2f} s')
    return lc, time_text

ani = FuncAnimation(fig, update, frames=len(x_vals_three_cycles), fargs=[x_vals_three_cycles, y_vals_three_cycles, times_three_cycles, lc, time_text], blit=True)

plt.show()
# Save the animation as an MP4 file
# mp4_path = 'raster_scan_three_cycles.mp4'
# ani.save(mp4_path, writer='ffmpeg', fps=2)