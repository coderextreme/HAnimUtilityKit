import xml.etree.ElementTree
import os
import re
import glob
import sys
import time

def animation_remove(root):

    for time_sensor_parent in root.findall('.//TimeSensor/..'):
        for time_sensor in time_sensor_parent.findall('TimeSensor'):
            time_sensor_parent.remove(time_sensor)

    for route_parent in root.findall('.//ROUTE/..'):
        for route in route_parent.findall('ROUTE'):
            route_parent.remove(route)

    for position_interpolator_parent in root.findall('.//PositionInterpolator/..'):
        for position_interpolator in position_interpolator_parent.findall('PositionInterpolator'):
            position_interpolator_parent.remove(position_interpolator)

    for orientation_interpolator_parent in root.findall('.//OrientationInterpolator/..'):
        for orientation_interpolator in orientation_interpolator_parent.findall('OrientationInterpolator'):
            orientation_interpolator_parent.remove(orientation_interpolator)
