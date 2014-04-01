#!/usr/bin/env python
import roslib; roslib.load_manifest('tagDetector')
import rospy
import tf
from math import sqrt, pow, atan2
from geometry_msgs.msg import Transform
from april_msgs.msg import TagPoseArray


def handle_tag_pose(msg):
    broadcaster = tf.TransformBroadcaster()
    tags = msg.tags
    for tag in tags:
             broadcaster.sendTransform((tag.pose.position.x, 
					tag.pose.position.y, 
					tag.pose.position.z), 
				       (tag.pose.orientation.x, 
					tag.pose.orientation.y, 
					tag.pose.orientation.z, 
					tag.pose.orientation.w),
                              	       rospy.Time.now(),
                                       prefix + 'aprilTag.' + str(tag.id),
                              	       "world")

if __name__ == '__main__':
    rospy.init_node('tag_tf_broadcaster')
    rospy.Subscriber( '/tags', TagPoseArray, handle_tag_pose)

    prefix = rospy.get_param('tf_prefix', '') +'/'
    rospy.spin()

