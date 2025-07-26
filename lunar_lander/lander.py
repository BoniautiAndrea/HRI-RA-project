import gymnasium as gym
from gymnasium import Wrapper
import Box2D
from Box2D.b2 import fixtureDef, polygonShape, revoluteJointDef#, edgeShape, contactListener

FPS = 50
SCALE = 30.0  # affects how fast-paced the game is, forces should be adjusted as well

MAIN_ENGINE_POWER = 13.0
SIDE_ENGINE_POWER = 0.6

INITIAL_RANDOM = 0.01#1000.0  # Set 1500 to make game harder

LANDER_POLY = [(-14, +17), (-17, 0), (-17, -10), (+17, -10), (+17, 0), (+14, +17)]
LEG_AWAY = 20
LEG_DOWN = 18
LEG_W, LEG_H = 2, 8
LEG_SPRING_TORQUE = 40

SIDE_ENGINE_HEIGHT = 14
SIDE_ENGINE_AWAY = 12
MAIN_ENGINE_Y_LOCATION = (
    4  # The Y location of the main engine on the body of the Lander.
)

VIEWPORT_W = 600
VIEWPORT_H = 400

class Lander(Wrapper):

    def __init__(self, env: gym.Env):
        super().__init__(env)

    # init_x and init_y can have values in [0,1]
    def reset(self, init_x = 'center', init_y = 'middle'):
        # Admissible values for position:
        # x value: [0,20]
        # y value: [7,13]
        if init_x == 'left':
            init_x = 2
        elif init_x == 'right':
            init_x = 18
        else:
            init_x = 10
        
        if init_y == 'high':
            init_y = 13
        elif init_y == 'low':
            init_y = 7
        else:
            init_y = 10

        initial_x = init_x#0.1 + 10*(2*init_x)
        initial_y = init_y#7 + 6*init_y

        self.env.reset()
        self.unwrapped.lander: Box2D.b2Body = self.unwrapped.world.CreateDynamicBody(
            position=(initial_x, initial_y),
            angle=0.0,
            fixtures=fixtureDef(
                shape=polygonShape(
                    vertices=[(x / SCALE, y / SCALE) for x, y in LANDER_POLY]
                ),
                density=5.0,
                friction=0.1,
                categoryBits=0x0010,
                maskBits=0x001,  # collide only with ground
                restitution=0.0,
            ),  # 0.99 bouncy
        )
        self.unwrapped.lander.color1 = (128, 102, 230)
        self.unwrapped.lander.color2 = (77, 77, 128)

        # Apply the initial random impulse to the lander
        self.unwrapped.lander.ApplyForceToCenter(
            (
                self.unwrapped.np_random.uniform(-INITIAL_RANDOM, INITIAL_RANDOM),
                self.unwrapped.np_random.uniform(-INITIAL_RANDOM, INITIAL_RANDOM),
            ),
            True,
        )

        self.unwrapped.legs = []
        for i in [-1, +1]:
            leg = self.unwrapped.world.CreateDynamicBody(
                position=(initial_x - i * LEG_AWAY / SCALE, initial_y),
                angle=(i * 0.05),
                fixtures=fixtureDef(
                    shape=polygonShape(box=(LEG_W / SCALE, LEG_H / SCALE)),
                    density=1.0,
                    restitution=0.0,
                    categoryBits=0x0020,
                    maskBits=0x001,
                ),
            )
            leg.ground_contact = False
            leg.color1 = (128, 102, 230)
            leg.color2 = (77, 77, 128)
            rjd = revoluteJointDef(
                bodyA=self.unwrapped.lander,
                bodyB=leg,
                localAnchorA=(0, 0),
                localAnchorB=(i * LEG_AWAY / SCALE, LEG_DOWN / SCALE),
                enableMotor=True,
                enableLimit=True,
                maxMotorTorque=LEG_SPRING_TORQUE,
                motorSpeed=+0.3 * i,  # low enough not to jump back into the sky
            )
            if i == -1:
                rjd.lowerAngle = (
                    +0.9 - 0.5
                )  # The most esoteric numbers here, angled legs have freedom to travel within
                rjd.upperAngle = +0.9
            else:
                rjd.lowerAngle = -0.9
                rjd.upperAngle = -0.9 + 0.5
            leg.joint = self.unwrapped.world.CreateJoint(rjd)
            self.unwrapped.legs.append(leg)

        self.unwrapped.drawlist = [self.unwrapped.lander] + self.unwrapped.legs

        return self.step(0)[0], {}


    def step(self, action):
        return self.unwrapped.step(action)

"""
lander = Lander(gym.make('LunarLander-v2', render_mode='human'))
observation, info = lander.reset(init_x='center', init_y='low')
obs = []
for i in range(20):
    if i%2 == 0:
        observation, reward, terminated, truncated, info = lander.step(0)
        lander.step(0)
    else:
        observation, reward, terminated, truncated, info = lander.step(2)
    o = []
    for i in range(6):
        print(observation[i].item())
        #o.append(float(("%.9f" % observation[i].item()).rstrip('0').rstrip('.')))
        #o.append(round(float(observation[i].item()), 10))
        o.append(float('{:.8f}'.format(observation[i])))
    obs.append(o)

print(obs)
"""
