# Tutorial@BuildSys24 (Hangzhou!)

## More details on the plan and schedule will be online shortly. Stay tuned!!!

Smart building applications have shown potential to reduce building energy consumption while also maintaining occupant comfort and increasing productivity. Prior research on building operating systems and standardized building representations lays the foundation of developing portable and adaptable building applications. Despite technological and standardization victories, the pace of innovation and the adoption rate of these smart building applications in the real world remains low due to safety reasons. Building managers are naturally reluctant to deploy third party building applications which are unvetted and possibly buggy. The inability of modern buildings to properly restrict an application's permissions also makes the application's execution generally opaque to the manager, unless intensive manual effort is invested to monitor them.

Playground is an open-source ``safe'' operating system (OS) abstraction for buildings that enables the execution of untrusted, multi-tenant applications in modern buildings. Playground is integrated with the Brick representation of the underlying buildings and features flexible and extensible access control and resource isolation mechanisms. These novel mechanisms of Playground avoid the intensive manual effort required to deploy building apps safely.

In this tutorial, we will cover the design of Playground, and introduce how to develop and deploy building apps with Playground as well as how to ensure the safe executions of them with the mechanisms we provide. Ideally, attendants will be able to write their first own building application, deploy it on a real building, and write customized access control and resource isolation policies to regulate it. The goal is to encourage innovation and exploration of how modern building applications can provide value to occupants, managers, and other stakeholders in the real world with Playground.

## What is Playground and why does it matter?
Adoption of building apps in practice is slow for two safety reasons:
1. Building managers DO NOT trust any third-party software
    * Third-party, unvetted, possibly buggy
    * May affect safety- and comfort-critical elements of building

2. The inability of modern buildings to properly restrict an application’s permissions
    * Execution opaquely to the manager with unclear impact on the building state
    * Require extensive manual effort to oversee all potential effects

To bridge the gap, we introduce Playground, an open-source ``safe'' operating system (OS) abstraction for buildings that enables the execution of untrusted, multi-tenant applications in modern buildings. Playground is integrated with the Brick representation of the underlying buildings and features flexible and extensible access control and resource isolation mechanisms. These novel mechanisms of Playground avoid the intensive manual effort required to deploy building apps safely.

## What to Expect in this Tutorial?
1. A quick walkthrough of the system design of Playground and relevant background
2. Write your own toy building applications and deploy on real buildings
3. Regulate your building application with fully customizable access control and isolation mechanism provided by Playground on real buildings 


## Tentative Schedule (A half day ~3hr event)

| Topic                                                                                                                                                                                                                                                                                                                                                                                                      | Presenter                      | Time  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ----- |
| Introduction to Playground                                                                                                                                                                                                                                                                                                                                                                                 | Xiaohan Fu                     | 25min |
| Recap on Brick programming and NREL’s BuildingMOTIF [2]                                                                                                                                                                                                                                                                                                                                                    | Gabe Fierro                    | 20min |
| Lab session 1 — Write your own building app with Playground<br>Checkpoints:<br><ul><li>Write a simple building application with Brick and Playground interfaces<br>E.g. energy metering/zone control app</li><li>Write permission profile for the app and upload these apps to Playground.</li><li>(optional) Write semantic sufficiency requirement of the app and check its compatibility with the Brick graph</li></ul> | Xiaohan Fu and/or<br>Yihao Liu | 50min |
| BREAK                                                                                                                                                                                                                                                                                                                                                                                                      |                                | 20min |
| Lab session 2 — Regulate building apps with various policies<br>Checkpoints:<br><ul><li>Design permission profiles of users in the system</li><li>Define resource constraints and regulating policies</li><li>Install previously written and uploaded apps to playground and play with it</li></ul>                                                                                                                            | Xiaohan Fu and/or<br>Yihao Liu | 60min |
| (optional) discussions and feedback                                                                                                                                                                                                                                                                                                                                                                        |                                | ~     |
