"""! @brief This class is used to keep track of detected bee characteristics. """
##
# @file Statistics.py
#
# @brief This class is used to keep track of detected bee characteristics
#
# @section authors Author(s)
# - Created by Fabian Hickert on december 2020
#
import json
from collections import deque
# import redis

class Statistics(object):
    """! The 'Statistics' class keeps track of all the monitoring results.
    """
    def __init__(self):
        # Connect to Redis
        # redis_host = 'localhost'  # Redis server host
        # redis_port = 6379  # Redis server port
        # redis_db = 0  # Redis database number
        # redis_password = 'pass'  # Redis server password (if any)

        # # Create a Redis client
        # self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)


        """! Initializes the statistics object
        """
        self._beesIn = 0
        self._beesOut = 0
        self._beesInOverall = 0
        self._beesOutOverall = 0
        self._wespenCount = 0
        self._wespenCountOverall = 0
        self._varroaCount = 0
        self._varroaCountOverall = 0
        self._pollenCount = 0
        self._pollenCountOverall = 0
        self._coolingCount = 0
        self._coolingCountOverall = 0
        self._processedFames = 0
        self._processedFamesOverlall = 0

    def frameProcessed(self):
        """! Increases the frame processed counter
        """
        self._processedFames += 1
        self._processedFamesOverlall += 1

    def addBeeIn(self):
        """! Increases the bee-in counter
        """
        # self.redis.publish("gate.bee_in", "1")
        print("bee in")
        self._beesIn += 1
        self._beesInOverall += 1

    def addBeeOut(self):
        """! Increases the bee-out counter
        """
        # self.redis.publish("gate.bee_out", "1")
        print("bee out")
        self._beesOut +=1
        self._beesOutOverall +=1

    def getBeeCountOverall(self):
        """! Returns the overal counted bees (bees_in, bees_out)
        @return tuple (bees_in, bees_out)
        """
        return (self._beesInOverall, self._beesOutOverall)

    def getBeeCount(self):
        """! Returns the counted bees (bees_in, bees_out)
        """
        return (self._beesIn, self._beesOut)

    def addDetection(self, tag):
        """! Adds a detected bee charcteristic by tag
             @param tag any of ("wasps", "varroa", "pollen", "cooling")
        """
        if "wasps" == tag:
            self._wespenCount += 1
            self._wespenCountOverall += 1
        if "varroa" == tag:
            self._varroaCount += 1
            self._varroaCountOverall += 1
        if "pollen" == tag:
            self._pollenCount += 1
            self._pollenCountOverall += 1
        if "cooling" == tag:
            self._coolingCount += 1
            self._coolingCountOverall += 1

    def addClassificationResult(self, trackId, result):
        """! Adds a detected bee charcteristic by classification results
             @param trackId unused
             @param result  A set containing any combination of ("wasps", "varroa", "pollen", "cooling"=
        """
        if "wasps" in result:
            self.addDetection("wasps")
        if "varroa" in result:
            self.addDetection("varroa")
        if "pollen" in result:
            self.addDetection("pollen")
        if "cooling" in result:
            self.addDetection("cooling")

    def addClassificationResultByTag(self, trackId, tag):
        """! Adds a detected bee charcteristic by tag
             @param trackId unused
             @param tag  any of "wasps", "varroa", "pollen", "cooling"
        """
        self.addDetection(tag)

    def readJSON(self)->str:
        statistics_tuple = self.readStatistics()
        statistics_dict = {
            "wespenCount": statistics_tuple[0],
            "varroaCount": statistics_tuple[1],
            "pollenCount": statistics_tuple[2],
            "coolingCount": statistics_tuple[3],
            "beesIn": statistics_tuple[4],
            "beesOut": statistics_tuple[5],
            "processedFames": statistics_tuple[6]
        }

        statistics_json = json.dumps(statistics_dict, indent=4)
        return statistics_json

    def readStatistics(self):
        """! Return the current statistics for counted wasps, varroa, pollen,
             cooling, bees in, bees out and the amount of processed frames
             @return tuple
        """
        return (self._wespenCount,
                self._varroaCount,
                self._pollenCount,
                self._coolingCount,
                self._beesIn,
                self._beesOut,
                self._processedFames)

    def readOverallStatistics(self):
        """! Return the overall statistics for counted wasps, varroa, pollen,
             cooling, bees in, bees out and the amount of processed frames
             @return tuple
        """
        return (self._wespenCountOverall,
                self._varroaCountOverall,
                self._pollenCountOverall,
                self._coolingCountOverall,
                self._beesInOverall,
                self._beesOutOverall,
                self._processedFamesOverlall)

    def resetStatistics(self):
        """! Resets the current statistics
        """
        self._wespenCount = 0
        self._varroaCount = 0
        self._pollenCount = 0
        self._coolingCount = 0
        self._beesIn = 0
        self._beesOut = 0
        self._processedFames = 0


# __dh = None
def getStatistics():
    return Statistics()
    # """! Returns the statistics object
    # #TODO: use pattern to realize singleton
    # @return The statistics instance
    # """
    # global __dh
    # if __dh == None:
    #     __dh = Statistics()

    # return __dh

