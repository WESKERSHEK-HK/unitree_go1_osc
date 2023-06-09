#!/usr/bin/env python

import rospy
import math
import random
from std_msgs.msg import Float64
from geometry_msgs.msg import Point, Twist

def calculate_shortest_angle(current_angle, target_angle):
    diff = target_angle - current_angle
    return ((diff + 180) % 360) - 180

def yaw_callback(data):
    global yaw
    yaw = data.data

def position_callback(data):
    global position
    position = data

def check_position():
    global position, last_position , robot_start, position_error_count, original_position ,force_quit

    while True:
        current_position = position
        rospy.sleep(0.1)
        if current_position.x == 0.0 and current_position.z == 0.0:
            if robot_start == False:
                robot_start = True
                
                position_error_count = 0
                print("Original position setup done")
                break
            else:
                if not force_quit:
                    #rospy.logwarn("Position data incorrect, waiting for an update.")
                    position_error_count += 1

            if position_error_count >= 100:
                if not force_quit:
                    print("Returning the robot to its original position.")
                    #return_function(0)
                position_error_count = 0
            continue
        
        else:
            last_position = position
            position_error_count = 0
            break

    return position

def return_function(mode):
    
    global yaw, position, original_position, pub_cmd_vel, running, return_count, force_quit

    # Rotate to 0 degrees
    target_yaw = 0
    #rospy.sleep(0.1)
    while return_count < 4:
        if return_count == 0 or return_count == 2 or return_count == 4:
            print("Rotating to 0 degrees")
            while calculate_shortest_angle(yaw, target_yaw) > 5:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                angular_speed = 0.2 if yaw < target_yaw else -0.2
                cmd = Twist()
                cmd.angular.z = angular_speed
                #print(cmd)
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)
            else:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                if return_count == 0:
                    return_count = 1
                elif return_count == 2:
                    return_count = 3
                elif return_count == 4:
                    return_count = 5
                print("Done Rotate to 0 degrees")
                rospy.sleep(1)
        
        elif return_count == 1:    

            # Move near original Z position
            target_z = original_position.z
            print("Moving to original Z position")
            while abs(position.z - target_z) > 0.01:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                #check_position()
                linear_speed = 0.2 if position.z < target_z else -0.2
                cmd = Twist()
                cmd.linear.y = linear_speed
                #print(cmd)
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)
                cmd = Twist()
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)

            else:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                return_count = 2
                print("Done Moving to original Z position")
                cmd = Twist()
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)
            
        elif return_count == 3:
            
            # Move near original X position
            target_x = original_position.x
            print("Moving to original X position")
            while abs(position.x - target_x) > 0.05:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                #check_position()
                linear_speed = 0.2 if position.x < target_x else -0.2
                cmd = Twist()
                cmd.linear.x = linear_speed
                #print(cmd)
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)
                cmd = Twist()
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)

            else:
                if force_quit and mode != 1:
                    return_count = 5
                    break
                return_count = 4
                print("Done Moving to original X position")
                cmd = Twist()
                pub_cmd_vel.publish(cmd)
                rospy.sleep(1)

        elif return_count == 5 and force_quit:
            break
    # Stop and wait for shutdown
    return_count = 0
    if not force_quit:
        print("Back to original position successful")
    cmd = Twist()
    pub_cmd_vel.publish(cmd)

def stop_function(event):
    global yaw, position, original_position, pub_cmd_vel, running, force_quit, last_movement

    #print("Stop function called. Returning the robot to its original position.")
    #force_quit = True
    #running = False

    #return_function(1)

    #print("Waiting to shutdown")
    last_movement = 'move_backward'

def performance_function():
    global pub_cmd_vel, position, running, yaw, limit_x, limit_z, last_movement
    rate = rospy.Rate(10)  # 10 Hz

    while running:
        
        # Randomly select a movement
        movement = random.choice(["rotate_left", "rotate_right"])
        cmd = Twist()
        pub_cmd_vel.publish(cmd)
        if yaw < 360 and yaw > 300:
            movement = "rotate_right"
        if yaw > 0 and yaw < 60:
            movement = "rotate_left"
        if last_movement == 'move_backward':
            movement = 'move_backward'
        

        

        rate.sleep()
        #check_position()

        cmd = Twist()
        
        # Perform the movement for 1 second
        if movement == "rotate_left":
            cmd.angular.z = 0.2
        elif movement == "rotate_right":
            cmd.angular.z = -0.2
        elif movement == "move_left":
            cmd.linear.y = 0.1
        elif movement == "move_right":
            cmd.linear.y = -0.1
        elif movement == "move_forward":
            cmd.linear.x = 0.1
        elif movement == "move_backward":
            cmd.linear.x = -0.2
        

        #print("Limit_x: {}, Limit_z: {}, Current_Position:{}".format(limit_x, limit_z, position))

        #if position.x > limit_x[1] or position.x < limit_x[0] or position.z > limit_z[1] or position.z < limit_z[0]:
            
            #print("React limit. Returning the robot to its original position.")
            #print("Limit_x: {}, Limit_z: {}, Current_Position:{}".format(limit_x, limit_z, position))
            #return_function(0)

            #continue
        #else:
        pub_cmd_vel.publish(cmd)
        if last_movement == '':
            rospy.sleep(0.2)
        else: 
            rospy.sleep(2)

        # Stop the movement
        cmd = Twist()
        pub_cmd_vel.publish(cmd)

        # Print the movement and position after movement
            
        #check_position()

        #print("Movement: {}, Position: x={}, z={}".format(movement, position.x, position.z))

        # Rest for a random time between 10 and 60 seconds
        if last_movement == 'backward':
            last_movement = ''
        rest_time = random.uniform(90, 210)
        print("Rest for {} sec".format(rest_time))
        rospy.sleep(rest_time)

def main():
    global yaw, position, original_position, pub_cmd_vel, running, robot_start, limit_x, limit_z, position_error_count, last_position, return_count, force_quit, last_movement

    rospy.init_node("robot_move", anonymous=True)
    rospy.Subscriber("yaw_data", Float64, yaw_callback, queue_size=1, buff_size=2**24)
    rospy.Subscriber("/dog/position", Point, position_callback, queue_size=1, buff_size=2**24)
    pub_cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=1)
    print('start subscriber')
    yaw = 0
    position = Point()
    last_position = Point()
    original_position = Point()
    original_position.x = 0.0
    original_position.y = 0.0
    original_position.z = 1.15
    running = True
    robot_start = False
    limit_x = [-0.15,0.28] #min, max
    limit_z = [1.145,1.165] #min, max
    position_error_count = 0
    return_count = 0
    force_quit = False
    last_movement = ''
    #original_position = check_position()

    # Schedule the stop_function to run after 30 minutes
    rospy.Timer(rospy.Duration(1260), stop_function, oneshot=True)

    print('start performance')
    performance_function()
    

if __name__ == "__main__":
    main()
