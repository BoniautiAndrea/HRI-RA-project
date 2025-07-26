# HRI-RA-project

Nowadays, the presence of informatics and even Artificial Intelligence is usual in a lot of environments,
from industry ones to study and research, even in homes for assistance goals.
In the last decades the attention to increase this presence and the aid that artificial intelligence can
give to us has led to the development of robotic systems, able to do physical labour instead of humans
or as just interactable interfaces that are able to reason and reduce the load of work and reasoning of
humans.
As shown in Figure 1, these robotic systems have spread in like every field of study/work/commerce

and are coming in different shapes and logics. As robotic arms [1] for industrial purposes, accelerat-
ing and automating assembly lines. As humanoid robots [23, 12] that could reach all human motion

capabilities and will find utility in like every kind of task, at least all task feasible for humans, from
military purposes to even some product used as waiter/waitress in restaurants.

And even four-legged and animaloid ones has been developed and research to study and learn locomo-
tion challenges and pros and cons of different locomotion structures.

Robotic and autonomous systems has found also successful application in space exploration of plane-
Figure 1: The growth of stock of industrial and service robotic systems in the latest years. Asia seems

to be the leading region on this sector. On the right side, it’s shown that logistic purpose is the most
common.
tary surfaces. Systems like orbiters, landers and rovers have been used to substitute human exploration
in those dangerous environments being able to retrieve important images, geographical and biological
information of the moon and mars [32], making possible the research of sign of ancient microbial life
[33].
Given that take off and flying are well studied task and can be planned and controlled by human
teams, the first task for an autonomous system is the landing on a surface.
The landing should be as smooth as possible to not harm the system architecture, should be precise
to land on a selected place, that should be selected for a safe landing (on a flat surface for example).
Autonomous landing has been developed mainly through deep learning approaches and reinforcement
learning techniques, using simulation environments to train these systems in order to make them able
to behave correctly in real life scenarios.
This report describes the structure, details and development process of the project for Human-Robot
Interaction and Reasoning Agents module of the Elective in Artifical Intelligence project.
It consists in a framework for interacting and planning through a simulated agent/robot in the Lunar
Lander environment offered by OpenAI’s Gymnasium, an API standard for reinforcement learning
with a diverse collection of reference environments.[8]

The user can interact with the agent, called LuLa, through voice or text in a terminal, asking infor-
mation about what it can do, find what pure planning can achieve in the lunar landing task, plan new

task defined by the user, learn the history of Apollo 11 while waiting for the plan to be finished and
also play a minigame to learn the challenges and difficulties that an autonomous robot faces during
landing.
At every interaction the robot state updates, but the user is able to come back and revert all of its
progresses at any time and restart with different options.
Lula essentially uses available plans built through different discretization logics, runs a simulation in

2

the Gymnasium environment and collects data from it. Simulation information can be watched and
retrieved by the user to know how well that plan performed.
The report continues with an overview of the code organization and its flow of information, then with

some implementation details, used libraries and models. At the end some discussion about the devel-
opment, with limitation and challenges faced and some solutions/workarounds.

This project could be an interesting basis to learn how planning can be used and how much it is able
to adapt in continuous environments, through a system that can iteratively run simulations guided by
policies made through planning.

Figure 2: Some example of different types of robotic systems, from humanoid ones (upper-left), drone
(bottom-left) to robotic arms used for surgery (second from bottom-right).
