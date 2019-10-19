# SLAM Qt

This is a simple repository to study "[SLAM for dummies](http://web.mit.edu/16.412j/www/html/Final%20Projects/Soren_project.ps)".

Check version 0.1 for:
      - Old obstacle avoidance version
      - Old Box2D simulation
      - With:
        - Bug
        - SUSNEA, MINZU, VASILU Proposal
        - Map generation with cellular automata method
        - And more basic stuff

## To do:
###### Simulation
- [x] Create a map generator with [cellular automata method](http://www.roguebasin.com/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels).
- [x] Create a vehicle than can run in the map and collide with it.
- [x] Create a 'sonar like' sensor to the vehicle.
- [ ] Add some obstacle avoidance from [Simple, Real-Time Obstacle Avoidance Algorithm for Mobile
Robots.](https://pdfs.semanticscholar.org/519e/790c8477cfb1d1a176e220f010d5ec5b1481.pdf)
  - [x] Bug
        ![](/doc/bug.gif)
  - [ ] Potential Field
  - [ ] Vector Field Histogram (VFH)
  - [ ] Bubble Band Technique
  - [x] SUSNEA, MINZU, VASILIU Proposal
        ![](/doc/proposal.gif)


### Run it
You'll need the last version of Qt to compile it.
```
$ git clone https://github.com/patrickelectric/SLAM_Qt && cd SLAM_Qt
$ git submodule update --init --recursive
$ mkdir build && cd build
$ qmake ..
$ make
$ ./Simulator
```

---
SLAM for dummies appears to be Free, but I'm not sure.
