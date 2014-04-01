#!/usr/bin/env python
import roslib
roslib.load_manifest('tagDetector')
import rospy
import tf
import math
from tagDetector.msg import Tag, TagArray
from tf.transformations import euler_from_quaternion
import re

PI = 3.141592
cameras = ['cam0']

if __name__ == '__main__':
    rospy.init_node('tag_tf_listener')

    listener = tf.TransformListener()

    location_pub = rospy.Publisher('quadLocation', TagArray)

    rate = rospy.Rate(10.0)

    tagArray = TagArray()

    while not rospy.is_shutdown():

        tagArray.tag = []
        idList = [0]

        ### for each camera ###
        for cam in cameras:

            ### Make a list of all tag transfromations contain the current camera ###
            tfList = [string for string in listener.getFrameStrings() if cam in string]

            ### For each transform in that list ##
            for string in tfList:
                tag = Tag()
                ### Look Up the transform for each tag ###
                try:
                    (trans,rot) = listener.lookupTransform('/' + cam + '/aprilTag.0', string, rospy.Time(0))
                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    continue

                ### Pull out ID ###
                tagID = int(re.sub('/' + cam + '/aprilTag.', '', string))

                ### See if tag has already been located ###
                if not tagID in idList:

                    idList.append(tagID)

                    angles = euler_from_quaternion(rot)
                    angle = angles[2] *180.0/PI

                    tag.id = tagID
                    tag.x = trans[0]
                    tag.y = trans[1]
                    tag.angle = angle
                    tagArray.tag.append(t)

        ### Publish Tag Stuff ###
        tagArray.size = len(tagArray.tag)
        tagArray.header.stamp = rospy.Time.now()
        location_pub.publish(tagArray)
        rate.sleep()

