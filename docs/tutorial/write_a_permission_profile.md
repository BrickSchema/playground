# Write a Permission Profile

A permission profile is a function-like object that takes in a few Brick-typed arguments and returns two lists of building resources for read and (read plus) write capability respectively.
The derivation of the two capability lists is defined by two SPARQL queries which use the provided arguments as parameters.
Note that the permission profile is statically typed --- arguments must be of the specified Brick class.

For example, this is a permission profile that takes `room` as an argument. 
To distinguish arguments and normal brackets (`{` and `}`), you should escape them with (`{{` and `}}`) in the sparql query.

```sparql
SELECT ?p WHERE {{ 
    ?e brick:feeds {room} . 
    ?e brick:hasPoint ?p . 
    ?p a ?o . 
    FILTER (?o IN (
        brick:Temperature_Sensor, 
        brick:Occupancy_Sensor, 
        brick:On_Off_Command, 
        brick:CO2_Sensor, 
        brick:Warm_Cool_Adjust_Sensor)
    ) 
}}
```

The arguments of the permission profile should be explicitly defined with their types in Brick.

```json
{"room":"brick:Room"}
```
