#!/usr/bin/env python
import roslib; roslib.load_manifest('location')
import rospy
from geometry_msgs.msg import Transform
from april_msgs.msg import TagPoseArray
from ardrone_autonomy.msg import Navdata


class location:

	""" Main Function """
	def __init__( self ):
	
		""" Publishers and Subscribers """
		self.location = rospy.Publisher('location/location', #TODO )
		rospy.init_node('location')
		
		rospy.Subscriber('/cam0/tags', TagPoseArray, self.__aprilCallback)
		rospy.Subscriber('/ardrone/navdata', Navdata, self.__navdataCallback)

		self.location_x = 0.0
		self.location_y = 0.0
		self.location_z = 0.0
		self.location_w = 0.0

		self.velocity_x = 0.0
		self.velocity_y = 0.0

		self.delta_time = 0.0

		self.pixel_ratio = 0.0

		self.tag_tally = 0
		self.stationary = 0


	def __aprilCallback( self, data ):
		""" Get tag info """

		self.tag_tally = 0
		for tag in data.tags[]:
			self.tag_tally = self.tag_tally + 1

			


	def __navData( self, data ):
		""" Get nav info """





	def __tagInViewApprox( self, data ):
		""" Use tag(s) to approximate location """

		#Set up pixel to height ratio
		# --> for every 1 unit high, camera is 1.1 units wide

		#ONLY UPDATE LOCATION WHEN QUADCOPTER IS STATIONARY











	def __noTagApprox( self, data ):
		""" Approximate location assuming constant velocity """

		self.location_x = self.location_x + (self.velocity_x * self.delta_time)
		self.location_y = self.location_y + (self.velocity_y * self.delta_time)



if __name__ = '__main__':
	try:
		x = location()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

