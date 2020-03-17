# Distributed Systems
 Simulation to demonstrate and understand mutual exclusion, consistency, replica, sockets and thread management
 
 To run the program:

 
1. Coded in Python 3.7.0
2. Two files attached, Server.py and Client.py
3. Run Server.py and Three instances of Client.py
4. GUI for the server and client will pop up.
5. Start (CONNECT BUTTON) the server and client (COMMUNICATE BUTTON).
6. Upon the clients connecting with the server the server will display the client's Process ID, Random integer sent by the client and the amount of time it has waited.
7. On the client side, the random number and the acknowledgement of the server stating its wait time will be displayed.
8. The 'STOP' button on the client side handles termination for each instances of the client running.
9. The server is multithreaded to handle multiple clients.