# WPI RBE 595 Haptic and Robotic Interaction
#### Prof. Jing Xiao | Fall 2022

The goal of this project is to develop a simulated environment where a user-controlled haptic interface point (HIP) interacts with arbitrary objects.
We based this work based off Zilles and Salisbury's Constraint-based method:

https://ieeexplore.ieee.org/document/525876

We render the environment in PyGame using PyOpenGL to draw our object, god-object, and HIP. Numpy is required for a lot of the god-object calculations.

## TO RUN:

Open _main.py_ and choose the _model_ you would like to test against. Make sure the HIP vertex is initialized outside the object, failing to do so 
will cause stability issues and break the simulation.

To control the HIP, the keyboard arrow keys are used: up and down for Y-axis motion, left and right for X-axis motion, and the right shift and return key for Z-axis motion. 

To control the camera, the mouse can be used to rotate the view. Also, the _w_ and _s_ keys will zoom in and out, respectively.

## Notes:

The simulation is not perfect, at times a collision with the object is not detected. In this situation, the god-object will be allowed to cross to a position where it should not be. At this point, you have two options: restart the simulation OR attempt another collision until it returns to the correct state.

The _render_ module contains all the PyOpenGL and PyGame information and initializations. 
The _HapticInterfacePoint_ module contains all the god calculations and handles updating the position of the HIP and god-object, updating the constraints, and calculating the forces.
The _checker_ module just contains the line and point tests required to detect collision and update constraints.

Reach out for any questions.
