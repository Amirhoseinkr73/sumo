#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import os
import sys

SUMO_HOME = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", SUMO_HOME), "tools"))

import traci  # noqa
import sumolib  # noqa

traci.start([sumolib.checkBinary('sumo'),
             '-n', 'input_net.net.xml',
             '-a', 'input_additional.add.xml',
             '-r', 'input_routes.rou.xml',
             '--tripinfo-output', 'tripinfo.xml',
             '--no-step-log',
             ] + sys.argv[1:])

print("constraints before swap")
for tlsID in traci.trafficlight.getIDList():
    for c in traci.trafficlight.getConstraints(tlsID):
        print(" tls=%s %s" % (tlsID, c))

traci.simulationStep()
newC = traci.trafficlight.swapConstraints("D", "t2", "A", "t0")
print("constraints added to avoid deadlock")
for c in newC:
    print(" tls=%s %s" % (tlsID, c))

print("constraints after swap")
for tlsID in traci.trafficlight.getIDList():
    for c in traci.trafficlight.getConstraints(tlsID):
        print(" tls=%s %s" % (tlsID, c))

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

traci.close()
