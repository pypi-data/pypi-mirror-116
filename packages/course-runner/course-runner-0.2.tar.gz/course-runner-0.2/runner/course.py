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

import socket

import requests
from loguru import logger
from http import HTTPStatus
from runner.api import APIClient
from runner.config import Config

PENDING_STATUS = "PENDING"
RUNNING_STATUS = "RUNNING"
COMPILATION_ERROR_STATUS = "COMPILATION_ERROR"
OK = "OK"
SUCCESS = "SUCCESS"
WRONG_ANSWER = "WRONG_ANSWER"
ERROR = "ERROR"
TIMED_OUT = 'TIMED_OUT'
RUNTIME_ERROR = 'RUNTIME_ERROR'
SIGNALED = 'SIGNALED'


class CourseApiClient(APIClient):
    def __init__(self, config: Config):
        super().__init__(config)

    def get_first_pending_submission(self):
        route = '/api/submission/'
        url = self._construct_url(self._config.course_url, route=route,
                                  parameters={'status': PENDING_STATUS})
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.json())
            raise ValueError("Request for get pending submission failed")
        submissions = r.json()
        logger.info(f"Find {len(submissions)} submissions")
        return submissions[0] if len(submissions) > 0 else []

    def get_list_of_jobs(self, submission_id):
        logger.info(f'submission_id = {submission_id}')
        route = '/api/job/'
        url = self._construct_url(self._config.course_url, route=route,
                                  parameters={'submission': submission_id,
                                              'status': PENDING_STATUS})
        return self._get(url)

    def get_language_information(self, language_id):
        logger.info(f'language_id = {language_id}')
        route = f'/api/language/{language_id}'
        url = self._construct_url(self._config.course_url, route=route)
        return self._get(url)

    def get_exercise(self, exercise_id):
        logger.info(f'exercise_id = {exercise_id}')
        route = f'/api/exercise/{exercise_id}'
        url = self._construct_url(self._config.course_url, route=route)
        return self._get(url)

    def get_executable(self, executable_id):
        logger.info(f'executable_id = {executable_id}')
        route = f'/api/executable/{executable_id}'
        url = self._construct_url(self._config.course_url, route=route)
        return self._get(url)

    def get_test_case(self, test_case_id):
        logger.info(f'test_case_id = {test_case_id}')
        route = f'/api/testcase/{test_case_id}'
        url = self._construct_url(self._config.course_url, route=route)
        return self._get(url)

    def update_submission(self, pk, data):
        route = f'/api/submission/{pk}/'
        url = self._construct_url(self._config.course_url, route=route)
        return self._patch(data, url)

    def update_job(self, pk, data):
        route = f'/api/job/{pk}/'
        url = self._construct_url(self._config.course_url, route=route)
        return self._patch(data, url)

    def download_file(self, id, t):
        route = f'/api/file/{t}/{id}'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.info(url)
            logger.error(r.status_code)
            logger.error(r.content)
            return None
        return r.content

    def register(self):
        route = '/api/runner/'
        url = self._construct_url(self._config.course_url, route=route)
        logger.info(url)
        data = {"name": socket.gethostname()}
        return self._post(data, url)
