# SDN-Based Access Control System

## Problem Statement
Allow only authorized hosts to communicate within the network.

## Objective
To implement an SDN-based access control mechanism using Mininet and a POX controller that:
- Allows only authorized communication
- Blocks unauthorized hosts
- Uses OpenFlow rules for control

---

## Project Description
This project uses Software Defined Networking (SDN) to control communication between hosts.

A POX controller is used to:
- Inspect incoming packets
- Apply whitelist-based filtering
- Install flow rules dynamically in the switch

---

## Topology
- 1 Switch (s1)
- 3 Hosts:
  - h1 → 10.0.0.1
  - h2 → 10.0.0.2
  - h3 → 10.0.0.3

---

## Access Control Policy
- h1 ↔ h2 → ALLOWED
- h3 → BLOCKED from all communication

---

## Tools Used
- Mininet
- POX Controller
- Open vSwitch
- Ubuntu Linux

---

## Setup and Execution

Step 1: Start Controller
cd ~/pox
python3 pox.py access_control openflow.of_01 --port=6633

Step 2: Run Mininet
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1,port=6633 --switch ovs,protocols=OpenFlow10

---

## Testing

Allowed Communication
h1 ping h2
h2 ping h1

Blocked Communication
h3 ping h1
h3 ping h2

---

## Flow Table Verification
sh ovs-ofctl dump-flows s1

---

## Expected Output
- Authorized hosts communicate successfully
- Unauthorized host is blocked
- Controller logs show ALLOWED and BLOCKED packets
- Flow rules are installed dynamically

---

## Conclusion
This project demonstrates SDN-based access control using a centralized controller and whitelist-based policy enforcement.

---

## Author
Sruthi Vejju
