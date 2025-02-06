# Tutorial@CPS-IoT Week 25 (Irvine!)

## What is Playground and why does it matter?
Adoption of building apps in practice is slow for two safety reasons:

1. Building managers DO NOT trust any third-party software

    * Third-party, unvetted, possibly buggy

    * May affect safety- and comfort-critical elements of building

2. The inability of modern buildings to properly restrict an application’s permissions

    * Execution opaquely to the manager with unclear impact on the building state

    * Require extensive manual effort to oversee all potential effects

To bridge the gap, we introduce Playground, an open-source "safe" operating system (OS) abstraction for buildings that enables the execution of untrusted, multi-tenant applications in modern buildings. Playground is integrated with the Brick representation of the underlying buildings and features flexible and extensible access control and resource isolation mechanisms. These novel mechanisms of Playground avoid the intensive manual effort required to deploy building apps safely.

The original paper on Playground was published in 2024 ACM/IEEE 15th International Conference on Cyber-Physical Systems (ICCPS) and was awarded as one of the best paper finalists🏆. Find the paper at <https://ieeexplore.ieee.org/abstract/document/10571633>

## What to Expect in this Tutorial?
1. Recap/Introduction of Brick and Brick programming
1. A quick walkthrough of the system design of Playground and relevant background
2. Write your own toy building applications
3. Use access control and isolation mechanism provided by Playground to deploy a building application safely on *real buildings*!


## Tentative Schedule (A half day ~3hr event)

| Topic                                                                                                                                                                                                                                                                                                                                                                                                      | Presenter                      | Time  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ----- |
| Introduction to Playground                                                                                                                                                                                                                                                                                                                                                                                 | Xiaohan Fu                     | 25min |
| Recap on Brick programming and NREL’s BuildingMOTIF [2]                                                                                                                                                                                                                                                                                                                                                    | Gabe Fierro                    | 25min |
| Lab session 1 — Write your own building app with Playground<br>Checkpoints:<br><ul><li>Write a simple building application with Brick and Playground interfaces<br>E.g. energy metering/zone control app</li><li>Write permission profile for the app and upload these apps to Playground.</li><li>(optional) Write semantic sufficiency requirement of the app and check its compatibility with the Brick graph</li></ul> | Xiaohan Fu and/or<br>Yihao Liu | 50min |
| BREAK                                                                                                                                                                                                                                                                                                                                                                                                      |                                | 20min |
| Lab session 2 — Regulate building apps with various policies<br>Checkpoints:<br><ul><li>Design permission profiles of users in the system</li><li>Define resource constraints and regulating policies</li><li>Install previously written and uploaded apps to playground and play with it</li></ul>                                                                                                                            | Xiaohan Fu and/or<br>Yihao Liu | 60min |
| (optional) discussions and feedback                                                                                                                                                                                                                                                                                                                                                                        |                                | ~     |
