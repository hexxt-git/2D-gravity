# introduction
hello, this is my 2D gravity and space simulator. written in python and pyray
![image](https://user-images.githubusercontent.com/88392191/193830128-23c6abd8-903e-4c2a-8dab-d50f99b4229f.png)


# controlls
[tab] switch modes settings, drawing, deleting, orbits and statistics <br>
[up][down] select a setting <br>
[left][right] change the selected setting <br>
[mouse left]+[drag] pan around <br>
[mouse scroll] zoom in and out

# settings
here you can change the basic simulation rules
<ul>
  <li> walls: turn on and off the worlds boundries </li>
  <li> walls x, walls y: change the width and height of the boundries </li>
  <li> merge: turn on and off the planets merging on collision to form a new one</li>
  <li> bounce: turn on and off wether planets bounce or stick on collision </li>
  <li> gravity: change the effect of gravity between bodies</li>
</ul>

# drawing
here you can make new planets and change their settings
- size: how big the body is
- density: how much mass the drawn body has, changes how much it attracts other bodies
- static: static planets do not move, but attract others
- random: randomizes the new planet

# deleting
in this section you can delete unwanted bodies
- delete: click to delete one by one
- delete all: delets all bodies upon click

# statistics:
general information about the simulation world
- planets: how many are there in the world
- velocity: sum velocity of all bodies
- mass: sum mass of all bodies

#orbiter
a tool to make planets orbit each other(still a work in progress)
- select orbited
- select orbiter
- make orbit

# camera
change the camera settings
- follow: allows you to select a planet and follow it
- release: releases the camera controlls
