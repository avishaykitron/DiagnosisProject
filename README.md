# This is project for Roni Stern #
This project consist of some parts - 
 - Systems generator
 - Problems generator
 - Daignosis 
 ## Systems generator ##
  System Generator code writen in java .
  The idea of the generator is to generate random system that consist of linear combination components. 
  Because of the randomly behavior of the system, there are some assumptions that we assume in order to generate random system in any  
  size or type of components. 
  
  ##Assumptions##:
   - Any input's component, have one argument . which means have one paramter in the linear combination. 
   - The system without cycles. 
   - There are cases that the system not fully conected , due to the randomly behavior.
  
  To generate new system you should run The File Program.java
  There are some parameters that define the system. you should insert the next properties. 
   - number of component in the system
   - number of component that will be input of the system
   - number of component that will be output of the system (thats define the level of probing in the system)
   - number of component with 1 argument. (pay attention that this number is equal or gratter than the number of input components)
   - number of component with 2 arguments. 
   - number of component with 3 arguments. (in case you want to add components with number of arguments gratter than 3 you can change it in      the file problem.java . the system allowed it.
   
 

