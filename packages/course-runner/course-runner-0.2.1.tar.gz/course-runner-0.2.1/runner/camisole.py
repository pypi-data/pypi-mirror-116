
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

from runner.api import APIClient
from loguru import logger


class CamisoleAPiClient(APIClient):
    def __init__(self, config):
        super().__init__(config)

    def get_headers(self):
        return None

    def submit_job(self, lang, test_case, test_case_content, source):
        if test_case_content is None or source is None:
            logger.error("test_case content or source content can't be None !")
            return

        data = {
            "lang": lang,
            "source": source,
            "tests": [{"name": test_case.get('input'), "stdin": test_case_content}]
        }

        url = self._construct_url(self._config.camisole_url, "/run")
        return self._post(data=data, url=url)
