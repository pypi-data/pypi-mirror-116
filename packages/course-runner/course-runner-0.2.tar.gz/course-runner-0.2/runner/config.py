
# ##################################################################################################
#  COURSE RUNNER                                                                                   #
#  Copyright (c) 2019-2020                                                                         #
#   --------------------------------------------------------------------------                     #
#                                                                                                  #
#  This program is free software: you can redistribute it and/or modify it                         #
#  under the terms of the GNU Lesser General Public License as published by                        #
#  the Free Software Foundation, either version 3 of the License, or (at your                      #
#  option) any later version.                                                                      #
#                                                                                                  #
#  This program is distributed in the hope that it will be useful, but                             #
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY                      #
#  or FITNESS FOR A PARTICULAR PURPOSE.                                                            #
#  See the GNU General Public License for more details.                                            #
#                                                                                                  #
#  You should have received a copy of the GNU Lesser General Public License                        #
#  along with this program.                                                                        #
#  If not, see <https://www.gnu.org/licenses/>.                                                    #
# ##################################################################################################

import os

from loguru import logger


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info('Creating the object')
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init__()
            # Put any initialization here.
        logger.info(cls._instance)
        return cls._instance

    def __init__(self):
        self.camisole_url = 'http://127.0.0.1:4242'

        self.course_url = os.getenv("COURSE_URL", None)
        if self.course_url is None or len(self.course_url) == 0:
            raise ValueError("COURSE_URL environment variable can't be none !")
        self.course_api_key = os.getenv("COURSE_API_KEY", None)
        if self.course_api_key is None or len(self.course_api_key) == 0:
            raise ValueError("COURSE_API_KEY environment variable can't be none !")
        self.time_waiting = int(os.getenv("TIME_WAITING", 60))

    def __str__(self):
        return f'{self.course_url} {self.camisole_url}'
