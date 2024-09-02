ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------


def pick_up(): #initialized pick up function pick container up from same location each time and return to home
    arm.move_arm(0.406,0.0,0.483)
    time.sleep(2)
    arm.move_arm(0.59, 0.055, -0.014) #container location
    time.sleep(2)
    arm.control_gripper(33)
    time.sleep(2)
    arm.move_arm(0.406,0.0,0.483)
    

def rotate_base(container_ID): #rotate base function initialized to rotate q-arm until autoclave colour is detected - once container is picked up
    old = potentiometer.right()

    while not arm.check_autoclave(container_ID): #while loop runs until autoclave is detected
        new = potentiometer.right()
        delta = new - old #is the change in how much the potentiometer moves
        turn = 348*delta #incriment value
        arm.rotate_base(turn) #q-arm turns using right potentiometer
        time.sleep(1)
        old = new 


#drop off location function is created because of the uncertainty value of the q-arm when it gets close to the autoclave
#by using coordinates, the container will be dropped off accurately every time
        
def drop_off_location(container_ID, size): #drop off location function gives the location as to where the exact location for drop off is
    colour_location = [0,(-0.013, -0.648, 0.294),(-0.030, 0.648, 0.294),(-0.662, 0.241, 0.314),(0.0,-0.409,0.174),(0.0, 0.424, 0.189),(-0.405, 0.207, 0.25)]

    if size == "small":
        if container_ID == "red":
            return colour_location[1]
        elif container_ID == "green":
            return colour_location[2]
        else:
            return colour_location[3]
    else:
        if container_ID == "red":
            return colour_location[4]
        elif container_ID == "green":
            return colour_location[5]
        else:
            return colour_location[6]


def drop_off(container_ID, size): #drop off function takes two arguments and drops off container to its respective location

    container_location = drop_off_location(container_ID, size) #drop off location is called using previous function and stored using container_location variable

    box_dropped = False
    while not box_dropped: #while loop that allows drop off 
        x = potentiometer.left()

        if size == "small": #checks the size (small) of the container using the parameters
            if (x > 0.5 and  x < 1): #for size small, left potentiometer should be in between 0.5 and 1 - once it is, q-arm drops container to accurate location
                arm.activate_autoclaves()
                arm.move_arm(container_location[0], container_location[1], container_location[2])
                time.sleep(2)
                arm.control_gripper(-20)
                box_dropped = True #while loop stops
                time.sleep(2)
                arm.home()

        else:
            if (x == 1): #checks if left potentiometer is at 1, only if the size is NOT small
                arm.activate_autoclaves()
                arm.open_autoclave(container_ID)
                time.sleep(1)
                arm.move_arm(container_location[0], container_location[1], container_location[2]) #q-arm drops container to accurate location
                time.sleep(1)
                arm.control_gripper(-20)
                box_dropped = True
                time.sleep(2)
                arm.home()
                arm.open_autoclave(container_ID,False)
                time.sleep(1)
                arm.deactivate_autoclaves()


def main():
    colours = [1, 2, 3, 4, 5, 6] #list of all colours using their ID
    for container in range (len(colours)): #loop that goes through all colours in range of 6
        random_spawn = random.choice(colours)  
        container_spawn = arm.spawn_cage(random_spawn) #variable that is assigned to random container spwan from the list
        colours.remove(random_spawn) #removes the random spwan colour ID
        
    #list gets rid of 1 colour and loop runs with a range of n-1 until no more colour ID's in loop
    
        pick_up() #executes pick up function


        if (container_spawn == 1 or container_spawn == 4): 
            container_ID = 'red'
        elif (container_spawn == 2 or container_spawn == 5):
            container_ID = 'green'
        else:
            container_ID = 'blue'

        if (random_spawn == 1 or random_spawn == 2 or random_spawn == 3):
            size = "small"
        else:
            size = "big"


        rotate_base(container_ID) #executes rotate_base function 

        time.sleep(2)
        
        drop_off(container_ID, size) #executes drop_off function



#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    
