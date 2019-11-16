import time

from payton.scene import Scene
from payton.scene.collision import CollisionTest
from payton.scene.geometry import Cylinder

myScene = Scene()
c1 = Cylinder()
c1.position = (3, 3, 0)

c2 = Cylinder()
c2.position = (-3, -3, 0)

c3 = Cylinder()
c3.position = (-3, -3, 3)

moving_part = c2

def makeItRed(collision, pairs):
    global moving_part
    for pair in pairs:
        pair[1].material.color = [1.0, 0, 0]
        collision.resolve(pair[0], pair[1])
    c3.position = [c3.position[0], c3.position[1], c3.position[2]+0.11]

    moving_part = c3
    myScene.clocks["c2_clocks"].pause()
    print("Collision triggered")

collision = CollisionTest(callback=makeItRed)
collision.add_object(c2)
collision.add_object(c3)
myScene.add_collision_test(collision)

myScene.add_object("cylinder_1", c1)
myScene.add_object("cylinder_2", c2)
myScene.add_object("cylinder_3", c3)

def c2Move(period, total):
    pos = moving_part.position
    moving_part.position=[pos[0], pos[1], pos[2] + period]

def c3Move(period, total):
    if moving_part == c3 and myScene.clocks["c2_clocks"]._pause:
        time.sleep(0.2)
        c3.material.color = [1.0, 1.0, 1.0]
        myScene.clocks["c2_clocks"].pause()
    
myScene.create_clock("c2_clocks", 0.03, c2Move)
myScene.create_clock("c3_clocks", 0.03, c3Move)
myScene.run()