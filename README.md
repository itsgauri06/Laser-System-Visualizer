# Laser-System-Visualizer
A visual physics simulation of a 3-level solid-state laser cavity built in Python using tkinter.

https://github.com/user-attachments/assets/d684b285-0257-43f4-b91e-8287adba60b0

# What is happening?
1. The Energy States
In this simulation, atoms transition between three specific energy levels:
 **E1 (Ground State):** The resting state of the atoms at the bottom of the cavity.
 **E2 (Metastable State):** The "waiting room." Atoms pause here for a short time, which is crucial for building up enough potential energy (population inversion).
 **E3 (Excited State):** The highest energy level.
   
 3. The Pumping Process
Clicking **"Pump Energy"** injects energy into the system. An atom at the Ground State (E1) absorbs this energy and shoots up to the Excited State (E3). Because it cannot hold that high energy for long, it quickly drops to the Metastable State (E2).

Once an atom is resting at the Metastable State (E2):
 
 **Spontaneous Emission:** If left alone for too long, the atom naturally drops back down to E1, releasing its stored energy as a single red photon.

 **Stimulated Emission (The Laser Effect):** If a traveling photon bumps into an atom waiting at E2, it forces the atom to drop to E1 immediately. The atom releases a new photon that is an exact "clone" of the one that hit it—traveling in the same direction. This is how the light multiplies.

 4. The Optical Cavity
The atoms are trapped between two mirrors:
 **The Left Mirror:** A 100% reflective mirror that bounces all photons back into the mix.
 **The Right Mirror (Output Coupler):** This acts as a smart valve. It forces photons to bounce back and forth until the cavity is highly energized (holding more than 10 photons). Once this "lasing threshold" is reached, a steady stream of photons can pass through, creating a continuous laser beam.

**State Machines:** Each atom is programmed with a specific state (`"ground"`, `"pumping"`, `"metastable"`, or `"dropping"`) to prevent animation glitches and ensure accurate physics sequencing.

**Coordinate Tracking:** The code continuously monitors the `(x, y)` coordinates of every photon and atom on the Tkinter canvas to detect collisions for stimulated emission and mirror bounces.

**Smooth Animation:** Utilizes `window.after()` for non-blocking animation loops, allowing multiple atoms and photons to move independently at the same time while still being able to pause cleanly via the "Stop" button.
