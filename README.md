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
   - each component as one result and it the solution of the linear combination. 
   - output of component can be input for many other components. 
  
  To generate new system you should run The File Program.java
  There are some parameters that define the system. you should insert the next properties. 
   - number of component in the system
   - number of component that will be input of the system
   - number of component that will be output of the system (thats define the level of probing in the system)
   - number of component with 1 argument. (pay attention that this number is equal or gratter than the number of input components)
   - number of component with 2 arguments. 
   - number of component with 3 arguments. (in case you want to add components with number of arguments gratter than 3 you can change it in      the file problem.java . the system allowed it.
   
   The output of this code is a csv file that represent a system. 
   for each component of the system, a line in the csv file - shows form which other component it gets inputs. 
   for example in line j - that represent the j' component. 
   if the i' component is input to j' component then in cell [j][i] will be number of argument in j' linear equation that get it.
   if the i' component isn't input to j' component then in cell [j][i] will be '-1'.
   
   in addition the last row in the file shows which component is an output component.
   and the last column shows which component is an input component. 
   
   ##Problems generator##
   
   
   ##Daignosis##
   
   This code writen in python.
   After that we generate system and many problems, we save the porblems in a directory. 
   
   each problem file represent a specific problem which means that it has the properties. 
    - sub-systems
    - input components
    - outputs component
    - number of normal observations
    - the normal observations.
    - number of buggy observations.
    - the buggy observations. 
    - the id of the buggy components.
    - range of inputs.
    
    
   the simple algorithm save the normal observations in hase tables, and than for each suspect
   observation , if it buggy observation , we check if the algorithm found it. in case that we found it
   we define it as an hit. 
   the sucess rate define as - hits/number of buggy observation. 
    
   the algorithm with regression idea in addition to the hase table, generate regression model for each 
   subsystem, and if the system have enough normal observation, we try to found buggy observation
   with the model. 
    
   the file program.py has to functions. 
   the first function get a diretory path and run the simple algorithm for each file in the directory,
   and save the results of the runs in a csv file. 
    
   the second function do the same thing with the regression algorthim. 
    
    
    

 

