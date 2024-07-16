# About

## What is Playground?

PlayGround is a safe building operating system (SBOS), that incorporates a structured semantic representation of the building (based on [Brick](brickschema.org)) to inform the safe, multi-tenant execution of untrusted applications. We use the semantic representation to implement (a) a novel graph-based capability mechanism for fine-grained and expressive access control management, and (b) a resource isolation mechanism with preemptive interventions and passive telemetry-based live resource monitoring.

## Why does this matter?

Despite technological and standardization victories, the pace of innovation and the adoption rate of smart building applications in the real world remains low due to safety reasons. 

> I bet very few have used a real building application in the wild.

Building managers are naturally reluctant to deploy third party building applications which are unvetted and possibly buggy. The inability of modern buildings to properly restrict an application's permissions also makes the application's execution generally opaque to the manager, unless intensive manual effort is invested to monitor them.

Playground, is designed to tackle these issues. The goal of Playground is to encourage innovation and exploration of how modern building applications can provide value to occupants, managers, and other stakeholders while avoiding the intensive manual effort required to deploy them *safely*.


## Citation

A [paper](https://ieeexplore.ieee.org/abstract/document/10571633) describing the design philosophies and techinical contributions of Playground was published in 2024 ACM/IEEE 15th International Conference on Cyber-Physical Systems (ICCPS) and was awarded as one of the 🏆best paper finalists🏆. If you find Playground to be helpful, please consider cite
```latex
@INPROCEEDINGS{10571633,
  author={Fu, Xiaohan and Liu, Yihao and Koh, Jason and Hong, Dezhi and Gupta, Rajesh and Fierro, Gabe},
  booktitle={2024 ACM/IEEE 15th International Conference on Cyber-Physical Systems (ICCPS)}, 
  title={Playground: A Safe Building Operating System}, 
  year={2024},
  volume={},
  number={},
  pages={111-122},
  keywords={Smart buildings;Costs;Operating systems;Buildings;Semantics;Programming;Maintenance;Brick;building;isolation;capability},
  doi={10.1109/ICCPS61052.2024.00017}}
```