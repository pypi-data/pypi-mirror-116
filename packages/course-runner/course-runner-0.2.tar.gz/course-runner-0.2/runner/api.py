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

from http import HTTPStatus

import requests
from loguru import logger


class APIClient:
    def __init__(self, config):
        self._config = config

    def get_headers(self):
        return {'Authorization': f'Api-Key {self._config.course_api_key}'}

    @staticmethod
    def _construct_url(api_url, route=None, parameters=None):
        if parameters is None:
            parameters = {}
        params = []
        for k, v in parameters.items():
            params.append(f'{k}={v}')
        if len(params) > 0:
            param_string = "&".join(params)
            return f'{api_url}{route}?{param_string}'
        return f'{api_url}{route}'

    def _get(self, url):
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(url)
            logger.error(r.status_code)
            logger.error(r.json())
            return None
        return r.json()

    def _patch(self, data, url):
        r = requests.patch(url, json=data, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.content)
            return False, r
        return True, r

    def _post(self, data, url):
        r = requests.post(url, json=data, headers=self.get_headers())

        if r.status_code != HTTPStatus.CREATED and r.status_code != HTTPStatus.OK:
            logger.error(HTTPStatus.OK)
            logger.error(r.status_code)
            logger.error(r.content)
            return False, r
        return True, r
