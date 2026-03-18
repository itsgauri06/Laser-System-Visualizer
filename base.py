from tkinter import *
import random


window = Tk()
window.title("Laser System")
running = False
laser_cooldown = False

canvas = Canvas(window, height=500, width=900,
                bg="#040124", highlightthickness=0)
canvas.pack()


def create_atom(x, y):
    r = 4
    atom = canvas.create_oval(x-r, y-r, x+r, y+r,
                              fill="#ffff66", outline="")
    return {"id": atom, "state": "ground"}


atoms = [
    create_atom(150, 440),
    create_atom(190, 440),
    create_atom(230, 440),
    create_atom(270, 440),
    create_atom(310, 440),
    create_atom(350, 440)
]


canvas.create_line(700, 450, 130, 450, fill="white", width=4)
canvas.create_line(700, 300, 130, 300, fill="white", width=4)
canvas.create_line(700, 200, 130, 200, fill="white", width=4)
# mirror walls
left_mirror = canvas.create_line(130, 100, 130, 470, fill="#cccccc", width=6)
right_mirror = canvas.create_line(690, 100, 690, 470, fill="#cccccc", width=6)
photons = []


def pump_energy():
    global running
    if running:
        return
    running = True
    release_atoms()


def release_atoms():
    if not running:
        return
    ground_atoms = [a for a in atoms if a["state"] == "ground"]

    if ground_atoms:
        atom = random.choice(ground_atoms)
        atom["state"] = "pumping"
        move_ball(atom)

    # window.after(time, function) time=400-900ms
    window.after(random.randint(500, 900), release_atoms)


def move_ball(atom):

    if not running:  # If the simulation is stopped, exit the function immediately.
        return

    ball = atom["id"]
    x1, y1, x2, y2 = canvas.coords(ball)

    if y1 > 190:
        canvas.move(ball, random.randint(-1, 1), -2)
        window.after(30, lambda: move_ball(atom))
    else:
        # Reached E3 Now quickly fall down to E2 (Metastable)
        window.after(50, lambda: drop_to_metastable(atom))


def drop_to_metastable(atom):
    if not running:
        return

    ball = atom["id"]
    x1, y1, x2, y2 = canvas.coords(ball)

    # Step 2: Drop to E2 (Metastable)
    if y1 < 290:
        canvas.move(ball, 0, 2)
        window.after(30, lambda: drop_to_metastable(atom))
    else:
        # Reached E2, It pauses here for a few seconds.
        atom["state"] = "metastable"

        window.after(2500, lambda: spontaneous_drop(atom))


def spontaneous_drop(atom):
    if not running:
        return

    # Crucial check: If it was ALREADY hit by a photon, skip this drop so it doesn't glitch!
    if atom["state"] not in ["metastable", "dropping"]:
        return

    atom["state"] = "dropping"
    ball = atom["id"]
    x1, y1, x2, y2 = canvas.coords(ball)

    # Step 3: Drop back to E1 (Ground)
    if y1 < 440:
        canvas.move(ball, 0, 4)
        window.after(30, lambda: spontaneous_drop(atom))
    else:
        # Back at ground state! Release the photon and reset the atom.
        atom["state"] = "ground"
        release_photon(atom)


def drop_atom(atom):
    if not running:
        return

    ball = atom["id"]
    x1, y1, x2, y2 = canvas.coords(ball)

    if y1 < 300:
        canvas.move(ball, 0, 2)
        window.after(40, lambda: drop_atom(atom))
    else:
        release_photon(atom)


def release_photon(atom):

    ball = atom["id"]
    x1, y1, x2, y2 = canvas.coords(ball)

    photon = canvas.create_line(x2, 375, x2+10, 375,  # horizontal line
                                fill="red", width=3)

    photons.append({"id": photon, "dx": 6})  # dx- speed and dirn

    move_photon(photon)

    canvas.coords(ball, x1, 440, x2, 448)

    atom["ready"] = False


def move_photon(photon):

    if not running:
        # If stopped, don't move, just check again in 30ms (acts as a pause)
        window.after(30, lambda: move_photon(photon))
        return

    # next-> give me first matching item and if none return
    # it means look through all the photons and find the one whose id matches this photon,so basically, we are using id to find speed, which is stored in a dictionary
    photon_data = next((p for p in photons if p["id"] == photon), None)
    if photon_data is None:
        return

    # moves photons left or right ; it gets the speed then in canvas.move according to +ve or -ve speed it controls direction
    dx = photon_data["dx"]
    canvas.move(photon, dx, 0)

    x1, y1, x2, y2 = canvas.coords(photon)

    if x2 > 900 or x1 < 0:
        canvas.delete(photon)
        photons[:] = [p for p in photons if p["id"] != photon]
        return

    if x2 >= 690:
        photon_data["dx"] = -6
        check_laser_output()

    if x1 <= 130:
        photon_data["dx"] = 6

    check_stimulated_emission(photon)

    window.after(30, lambda: move_photon(photon))


def check_stimulated_emission(photon):

    px1, py1, px2, py2 = canvas.coords(photon)

    incoming_data = next((p for p in photons if p["id"] == photon), None)
    if not incoming_data:
        return
    incoming_dx = incoming_data["dx"]

    for atom in atoms:
        ball = atom["id"]
        x1, y1, x2, y2 = canvas.coords(ball)

        # to see if it hits a metastable atom
        if atom["state"] == "metastable" and 285 < y1 < 315 and abs(px1-x1) < 20:

            new_photon = canvas.create_line(
                px2, py1, px2+8, py1, fill="red", width=2)

            # Give the new photon the exact same direction as the incoming one!
            photons.append({"id": new_photon, "dx": incoming_dx})
            move_photon(new_photon)

            canvas.coords(ball, x1, 440, x2, 448)
            atom["state"] = "ground"


def check_laser_output():

    close_photons = []
    for p in photons:
        coords = canvas.coords(p["id"])
        if coords:
            x2 = coords[2]
            if 640 < x2 <= 690 and p["dx"] > 0:
                close_photons.append(p)

    if len(photons) > 15 and len(close_photons) > 0:

        p = close_photons[0]
        canvas.delete(p["id"])  # to small dotted line from inside
        photons.remove(p)

        emit_laser()


def emit_laser():

    beam = canvas.create_line(690, 375, 760, 375, fill="red", width=5)
    move_beam(beam)


def move_beam(beam):

    if not running:
        window.after(30, lambda: move_beam(beam))
        return

    canvas.move(beam, 8, 0)

    x1, y1, x2, y2 = canvas.coords(beam)

    if x2 < 900:
        window.after(30, lambda: move_beam(beam))
    else:
        reset_laser()


def reset_laser():
    global laser_cooldown
    laser_cooldown = False


def click():
    print("Button clicked")


window.config(background="#040124")
label = Label(window, text="", bg="#040124").pack()
label = Label(window, text="Laser System", font=(
    'Bodoni MT Black', 25, 'bold'), fg='#e3f29d', bg="#040124")
label.pack()


canvas.create_text(10, 430, text="E1(Ground)", fill="white",
                   anchor="w", font=("Cascadia Code SemiBold", 11))
canvas.create_text(10, 290, text="E2(Metastable)", fill="white",
                   anchor="w", font=("Cascadia Code SemiBold", 11))
canvas.create_text(10, 190, text="E3(Excited)", fill="white",
                   anchor="w", font=("Cascadia Code SemiBold", 11))


button = Button(window, text="Pump Energy", command=pump_energy,
                font=("Comic Sans", 15), fg="#75b06a", bg="#1d274d",
                activeforeground="black", activebackground="#1d274d")

button.place(x=400, y=600)


def stop_simulation():
    global running
    running = False


stop_button = Button(window, text="Stop",
                     command=stop_simulation,
                     font=("Comic Sans", 15),
                     fg="#75b06a", bg="#1d274d")

stop_button.place(x=600, y=600)


window.mainloop()
