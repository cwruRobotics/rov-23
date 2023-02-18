# GUI Package
The GUI comprises PyQt `modules` (imported and positioned by app.py) which
communicate with the logical layer through `event_nodes`. `event_nodes` should
handle all multithreading to prevent GUI hangs. Each module should only send
PyQt signals within itself.

## Node Graph
![GUI Node Graph](images/GUINetwork.jpg)

## Topics
- `task_request`: service topic; GUI's client requests task changes by
`task_scheduler` and `task_scheduler` returns response.
- `task_feedback`: pub/sub topic; `task_requester` tells the GUI to change its
dropdown to reflect network state.
- `/rosout`: pub/sub topic; ROS logging topic that the GUI logger listens to.