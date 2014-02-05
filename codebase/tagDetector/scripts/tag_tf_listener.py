mport roslib
roslib.load_manifest('tagDetector')
import rospy
import tf
import math
from hoverTracker.msg import Tag, TagArray
from tf.transformations import euler_from_quaternion
import re

PI = 3.141592
cams = ['cam0','cam1','cam2','cam3']

if __name__ == '__main__':
    rospy.init_node('tag_tf_listener')

    listener = tf.TransformListener()

    location_pub = rospy.Publisher('quadLocation', TagArray)

    rate = rospy.Rate(10.0)

    tArray = TagArray()

    while not rospy.is_shutdown():

        tArray.tag = []
        idList = [0]

        ### for each camera ###
        for c in cams:

            ### Make a list of all tag transfromations contain the current camera ###
            tfList = [s for s in listener.getFrameStrings() if c in s]

            ### For each transform in that list ##
            for s in tfList:
                t = Tag()
                ### Look Up the transform for each tag ###
                try:
                    (trans,rot) = listener.lookupTransform('/'+c+'/aprilTag.0', s, rospy.Time(0))
                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    continue

                ### Pull out ID ###
                tagID = int(re.sub('/'+c+'/aprilTag.','',s))

                ### See if tag has already been located ###
                if not tagID in idList:

                    idList.append(tagID)

                    angles = euler_from_quaternion(rot)
                    angle = angles[2] *180.0/PI

                    t.id = tagID
                    t.x = trans[0]
                    t.y = trans[1]
                    t.angle = angle
                    tArray.tag.append(t)

        ### Publish Tag Stuff ###
        tArray.size = len(tArray.tag)
        tArray.header.stamp = rospy.Time.now()
        location_pub.publish(tArray)
        rate.sleep()

