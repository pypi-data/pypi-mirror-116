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
__all__ = [
    '__title__',
    '__summary__',
    '__uri__',
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__copyright__',
]

__title__ = 'course-runner'
__summary__ = 'autOevaluate yoUr Student Easily'
__keywords__ = 'autoevaluate'
__uri__ = 'https://gitlab.com/course-autoevaluate/runner'
__version__ = os.getenv("AUTOEVALUATE_VERSION")
__author__ = 'Thibault Falque'
__email__ = 'thibault.falque@univ-artois.fr'

__license__ = 'LGPLv3+'
__copyright__ = '2019-2020'

import os

