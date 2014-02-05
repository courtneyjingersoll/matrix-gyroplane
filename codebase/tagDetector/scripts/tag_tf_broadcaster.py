#!/usr/bin/env python
import roslib; roslib.load_manifest('tagDetector')
import rospy
import tf
from math import sqrt, pow, atan2
from geometry_msgs.msg import Transform
from april_msgs.msg import TagPoseArray


def handle_tag_pose(msg):
    br = tf.TransformBroadcaster()
    tags = msg.tags
    for x in tags:
             br.sendTransform((x.pose.position.x,x.pose.position.y,x.pose.position.z),
                              (x.pose.orientation.x,x.pose.orientation.y,x.pose.orientation.z,x.pose.orientation.w),
                              rospy.Time.now(),
                              prefix + 'aprilTag.' + str(x.id),
                              "world")

if __name__ == '__main__':
    rospy.init_node('tag_tf_broadcaster')
    rospy.Subscriber( '/tags', TagPoseArray, handle_tag_pose)

    prefix = rospy.get_param('tf_prefix', '') +'/'
    rospy.spin()

