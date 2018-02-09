# API

## User Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/user | GET | List Users |
| /api/user | POST | Add a User |
| /api/user/{id} | GET, POST | Read and edit a User |
| /api/user/{id} | DELETE | Delete a User |


## Schedule Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/schedule | GET | List Schedules |
| /api/schedule | POST | Add a Schedule |
| /api/schedule/{id} | GET, POST | Read and edit a Schedule |
| /api/schedule/{id} | DELETE | Delete a Schedule |


## Action Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/action | GET | List Action |
| /api/action | POST | Add an Action |
| /api/action/{id} | GET, POST | Read and edit an Action |
| /api/action/{id} | DELETE | Delete an Action |


## ActionProcess Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/actionprocess | GET | List ActionProcesses |
| /api/actionprocess | POST | Add an ActionProcess |
| /api/actionprocess/{id} | GET, POST | Read and edit an ActionProcess |
| /api/actionprocess/{id} | DELETE | Delete an ActionProcess |
| /api/actionprocess/action/{id} | GET | get current ActionProcess for the Action id |


## Sensor Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/sensor | GET | List Sensor |
| /api/sensor | POST | Add an Sensor |
| /api/sensor/{id} | GET, POST | Read and edit an Sensor |
| /api/sensor/{id} | DELETE | Delete an Sensor |


## Outlet Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/outlet | GET | List Outlet |
| /api/outlet | POST | Add an Outlet |
| /api/outlet/{id} | GET, POST | Read and edit an Outlet |
| /api/outlet/{id} | DELETE | Delete an Outlet |
| /api/outlet/{id}/toggle | POST | Toggle ON/OFF state of the outlet |
| /api/outlet/{id}/on | POST | Switch Outlet ON |
| /api/outlet/{id}/off | POST | Switch Outlet OFF |


## Measurement Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/measurement/{start}/{end} | GET | List Measurements between start and end times |
| /api/measurement | POST | Add a Measurement |
| /api/measurement/{id} | GET, POST | Read and edit a Measurement |
| /api/measurement/{id} | DELETE | Delete a Measurement |


## AggregateMeasurement Model
| URL | METHODS | NOTES |
| --- | ------ | ----- |
| /api/aggregatemeasurement/{start}/{end} | GET | List AggregateMeasurements between start and end times |
| /api/aggregatemeasurement | POST | Add an AggregateMeasurement |
| /api/aggregatemeasurement/{id} | GET, POST | Read and edit an AggregateMeasurement |
| /api/aggregatemeasurement/{id} | DELETE | Delete an AggregateMeasurement |
