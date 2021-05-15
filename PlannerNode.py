#!/usr/bin/env python3

import sys
import rospy
import math

from path_planning.msg import direction, map_detail
from MapClass import Map
global closed_set,closed_set_2 
closed_set= set()
closed_set_2 = set()
closed_set.add((0,0))

class PlannerNode:
    def __init__(self):
        self.direction_publisher = rospy.Publisher("/direction", direction, queue_size=10)
        # This is the publisher which will publish the direction for the bot to move
        # A general format for publishing has been given below

        self.walls_subscriber = rospy.Subscriber("/walls", map_detail, self.wall_callback)
        # This is the subscriber that will listen for the details about the map that the bot will aquire
        # This data will be send to the wall_callback function where it should be handled

        rospy.sleep(5) # a delay of some time to let the setup of the subscriber and publisher be completed

        # Since we know that the first step the bot will take will be down, we can simply do it here
        temp_val = direction() # make an object of the message type of the publisher
        temp_val.direction = 'down' # assign value to the object. Refer the custom direction.msg in the msg directory
        self.direction_publisher.publish(temp_val) # publish the object

    def heurisitc_value(self,tuple1):

        dx = abs((tuple1[0]-7))
        dy = abs((tuple1[1]-7))
        h = math.hypot(dx,dy)
        return h


    def wall_callback(self, map_detail):
        # this function will be called everytime the map sends data regarding the map on the '/walls' topic
        # you will recieve the data in the form of the map_detail variable which is an object of custom message type map_detail.msg from the msg directory
        print(map_detail)
        pass # Your code goes here. You need to figure out an algorithm to decide on the best direction of movement of the bot based on the data you have.
        # after deciding on the direction, you need to publish it using the publisher created.
        if (map_detail.current_x == map_detail.end_x) and (map_detail.current_y == map_detail.end_y):
            print("goal is reached")
            return
        
        start = (map_detail.current_x,map_detail.current_y) 
        #print(start)
        current = start
        if current in closed_set:
            closed_set_2.add((current[0],current[1]))

        r = (current[0],(current[1]+1))
        l = (current[0],(current[1]-1))
        u = ((current[0]-1),current[1])
        d = ((current[0]+1),current[1])
        closed_set.add((current[0],current[1]))
        print(closed_set)

        if map_detail.current_value == 14:
            temp_val = direction()
            temp_val.direction = 'down'
            self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 7:
            temp_val = direction()
            temp_val.direction = 'up'
            self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 11:
            temp_val = direction()
            temp_val.direction = 'left'
            self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 13:
            temp_val = direction()
            temp_val.direction = 'right'
            self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 6:
            if u in closed_set:
                temp_val = direction()
                temp_val.direction = 'down'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'up'
                self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 9:
            if l in closed_set:
                temp_val = direction()
                temp_val.direction = 'right'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'left'
                self.direction_publisher.publish(temp_val)
        
        elif map_detail.current_value == 12:
            if r in closed_set:
                temp_val = direction()
                temp_val.direction = 'down'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'right'
                self.direction_publisher.publish(temp_val)
        
        elif map_detail.current_value == 10:
            if l in closed_set:
                temp_val = direction()
                temp_val.direction = 'down'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'left'
                self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 5:
            if u in closed_set:
                temp_val = direction()
                temp_val.direction = 'right'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'up'
                self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 3:
            if l in closed_set:
                temp_val = direction()
                temp_val.direction = 'up'
                self.direction_publisher.publish(temp_val)
            else:
                temp_val = direction()
                temp_val.direction = 'left'
                self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 4:
            if u in closed_set:
                h1 = self.heurisitc_value(r)
                h2 = self.heurisitc_value(d)
                if (h1 < h2 and r not in closed_set_2) or (h2 < h1 and d  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            elif r in closed_set:

                h1 = self.heurisitc_value(u)
                h2 = self.heurisitc_value(d)
                if (h1 < h2 and u not in closed_set_2) or (h2 < h1 and d  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            else:
                h1 = self.heurisitc_value(u)
                h2 = self.heurisitc_value(r)
                if (h1 < h2 and u not in closed_set_2)  or (h2 < h1 and r  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
        
        elif map_detail.current_value == 8:
            if l in closed_set:
                h1 = self.heurisitc_value(r)
                h2 = self.heurisitc_value(d)
                if (h1 < h2 and r not in closed_set_2)  or (h2 < h1 and d  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            elif r in closed_set:

                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(d)
                if (h1 < h2 and l not in closed_set_2)  or (h2 < h1 and d  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            else:
                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(r)
                if h1 < h2 and l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 2:
            if l in closed_set:
                h1 = self.heurisitc_value(u)
                h2 = self.heurisitc_value(d)
                if h1 < h2 and u not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            elif u in closed_set:

                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(d)
                if h1 < h2 and l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            else:
                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(u)
                if h1 < h2 and l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)

        elif map_detail.current_value == 1:
            if l in closed_set:
                h1 = self.heurisitc_value(r)
                h2 = self.heurisitc_value(u)
                if (h1 < h2 and r not in closed_set_2) or(h2<h1 and u  not in closed_set_2 ):

                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
            elif r in closed_set:

                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(u)
                if (h1 < h2 and l not in closed_set_2)  or (h2 < h1 and u  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
            else:
                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(r)
                if (h1 < h2 and l not in closed_set_2)  or (h2 < h1 and d  in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)

        else :
            if l in closed_set:
                h1 = self.heurisitc_value(r)
                h2 = self.heurisitc_value(d)
                h3 = self.heurisitc_value(u)
                a = min(h1,h2,h3)
                if (a ==  h1 and r not in closed_set_2):

                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                elif (a == h2 and d not in closed_set_2):
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)
            elif r in closed_set:

                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(d)
                h3 = self.heurisitc_value(u)
                a = min(h1,h2,h3)
                if a == h1 and l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                elif a == h2 and d not in closed_set_2:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)

            elif u in closed_set:
                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(r)
                h3 = self.heurisitc_value(d)
                a = min(h1,h2,h3)
                if a == h1 and l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                elif a == h2 and r not in closed_set_2:
                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'down'
                    self.direction_publisher.publish(temp_val)
            else:
                h1 = self.heurisitc_value(l)
                h2 = self.heurisitc_value(r)
                h3 = self.heurisitc_value(u)
                a = min(h1,h2,h3)
                if a == h1 and  l not in closed_set_2:

                    temp_val = direction()
                    temp_val.direction = 'left'
                    self.direction_publisher.publish(temp_val)
                elif a == h2 and r not in closed_set_2:
                    temp_val = direction()
                    temp_val.direction = 'right'
                    self.direction_publisher.publish(temp_val)
                else:
                    temp_val = direction()
                    temp_val.direction = 'up'
                    self.direction_publisher.publish(temp_val)



if __name__ == '__main__':
    rospy.init_node('planner_node')
    PlannerNode()
    rospy.spin()
