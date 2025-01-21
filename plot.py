import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


def animated_pendulum(values, length):
    # Set figure size: 680px x 760px translates to ~6.8in x ~7.6in (1 inch = 100px)
    fig, axis = plt.subplots(figsize=(6.8, 7.6))

    #   fig.subplots_adjust(left=0, right=1, top=2, bottom=0)
    fig.subplots_adjust(left=0, right=1, top=1.02, bottom=0.03) 

    # Set aspect ratio and grid for 1.5cm cells
    axis.set_aspect('equal')

    #Set limits for x. y axes
    axis.set_xlim(-8.2, 8.2)
    axis.set_ylim(-8.2, 8.2)

    #Set background color to black
    fig.patch.set_facecolor("black")

    #Remove the axes
    axis.axis('off')

    # Initialize plot elements
    line, = axis.plot([], [], "o-", color="green", linewidth=2)
    path, = axis.plot([], [], color="yellow", linewidth=0.5)
    fps_text = axis.text(0.05, 0.95, "", transform=axis.transAxes, fontsize=10, va="top", color="white")

    

    start_time = time.time()
    x = time.time()
    avg = 0

    def update_frame(frame):
        nonlocal start_time, x, avg

        # Update the path and line data
        path.set_data(values["x2_val"][:frame], values["y2_val"][:frame])
        line.set_data([0, values["x1_val"][frame], values["x2_val"][frame]], [0, values["y1_val"][frame], values["y2_val"][frame]])

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - start_time + 1e-5)  # Avoid division by zero
        start_time = current_time
        avg = (avg * frame + fps) / (frame + 1)
        fps_text.set_text(f"FPS: {fps:.2f} | Time: {(time.time() - x):.2f}s | Average FPS: {avg:.2f}")

        return path, line, fps_text

    # Create the animation
    animation = FuncAnimation(fig=fig, func=update_frame, frames=length, interval=3.5, repeat=False, blit=True)

    return fig, animation
