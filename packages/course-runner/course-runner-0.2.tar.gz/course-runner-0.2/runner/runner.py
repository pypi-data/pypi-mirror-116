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

import hashlib
import json
import os
import sched
import stat
import time
import subprocess

from loguru import logger

from runner.config import Config
from runner.camisole import CamisoleAPiClient
from runner.course import RUNNING_STATUS, COMPILATION_ERROR_STATUS, CourseApiClient, OK, \
    WRONG_ANSWER, ERROR, SUCCESS, TIMED_OUT, RUNTIME_ERROR, SIGNALED

EXIT_AC = 42
EXIT_WA = 43

s = sched.scheduler(time.time, time.sleep)


class Runner:
    def __init__(self, submission, course_api_client: CourseApiClient,
                 camisole_api_client: CamisoleAPiClient):
        self._submission = submission
        self._course_api_client = course_api_client
        self._camisole = camisole_api_client
        self._path_submission = None
        self._submit_content = None

    def _download_submission_file(self):
        content = self._course_api_client.download_file(self._submission.get('id'), "submission")
        logger.debug(content)
        return content

    def _download_compare_script(self, executable):
        content = self._course_api_client.download_file(executable.get('id'), "executable")
        logger.debug(content)
        return content

    def _verify_checksum(self, sha, correct):
        return sha == correct

    def _verify_submission_file(self, content):
        sha = hashlib.sha256(content).hexdigest()
        correct_sum = self._submission.get('file_sha')
        if not self._verify_checksum(sha, correct_sum):
            logger.warning(f"{sha}!={correct_sum}")
            return False
        return True

    def _run_jobs(self, j, language, source_content):
        logger.info(f"Start job {j.get('id')} with test_case_id {j.get('test_case')} ")
        ok, resp = self._course_api_client.update_job(pk=j.get('id'), data={"status": 'RUNNING'})
        os.mkdir(f'{self._path_submission}/{j.get("id")}')
        logger.info(f'job_dir={self._path_submission}/{j.get("id")}')
        self._get_compare_script(j.get("id"))

        if not ok:
            logger.warning(f"Updating job {j.get('id')} via API not working. We stop the "
                           f"execution of the job ")
            return None

        test_case = self._course_api_client.get_test_case(j.get('test_case'))

        test_case_content_input = self._course_api_client.download_file(
            test_case.get('id'), "input")
        if test_case_content_input is None:
            self._course_api_client.update_job(j.get('id'),
                                               data={"status": ERROR,
                                                     "log": json.dumps({
                                                         'msg': 'problem when download input test case'})})
            return None

        test_case_content_input = test_case_content_input.decode("utf-8")

        test_case_content_output = self._course_api_client.download_file(
            test_case.get('id'), "output")

        if test_case_content_output is None:
            self._course_api_client.update_job(j.get('id'),
                                               data={"status": ERROR,
                                                     "log": json.dumps({
                                                         'msg': 'problem when download output test case'})})
            return None

        test_case_content_output = test_case_content_output.decode("utf-8")

        logger.info(test_case_content_input)
        logger.info(test_case_content_output)

        ok, response = self._camisole.submit_job(language.get("name"), test_case,
                                                 test_case_content_input,
                                                 source_content)

        if not ok:
            logger.warning("Request for submit the job failed ! ")
            self._course_api_client.update_job(j.get('id'),
                                               data={"status": ERROR,
                                                     "log": json.dumps(response.json())})
            return None

        status = self._check_response(j, response.json(), test_case_content_input,
                                      test_case_content_output)

        logger.info(f"end job {j.get('id')}")
        return status

    def _init_directory_submission(self):
        logger.info(f"create work directory for submission {self._submission.get('id')}")

        self._path_submission = f"work/{self._submission.get('id')}_{time.time()}"
        os.mkdir(self._path_submission)

    def _get_submission(self):
        self._submit_content = self._download_submission_file()

        if self._submit_content is None or not self._verify_submission_file(self._submit_content):
            logger.warning("We stop the execution because the hash sums do not match.")
            return False
        with open(f'{self._path_submission}/program', 'w') as f:
            f.write(self._submit_content.decode())
        return True

    def _get_compare_script(self, job_id):
        exercise_id = self._submission.get('exercise')

        logger.debug(self._submission)

        logger.info(f"Get exercise_id={exercise_id}")

        exercise = self._course_api_client.get_exercise(exercise_id)
        if exercise is None:
            return
        logger.debug(exercise)
        executable_id = exercise.get('executable')
        executable = self._course_api_client.get_executable(executable_id)
        logger.debug(executable)
        content = self._download_compare_script(executable)

        file_name = executable.get("file").split('/')[-1]

        logger.info('Create compare script')
        with open(f'{self._path_submission}/{job_id}/{file_name}', 'w') as f:
            f.write(content.decode())

        logger.info('Create the script for build compare program')

        with open(f'{self._path_submission}/{job_id}/build', 'w') as f:
            for line in executable.get('build_command').split('\n'):
                logger.debug(f'line={line}')
                if len(line) == 0 or line[0] == '\n':
                    continue
                f.write(line.strip())
                f.write("\n")
        st = os.stat(f'{self._path_submission}/{job_id}/build')
        os.chmod(f'{self._path_submission}/{job_id}/build', st.st_mode | stat.S_IEXEC)

        logger.info('Build the compare program')
        cmd = [f'{self._path_submission}/{job_id}/build', f'{self._path_submission}/{job_id}/'
                                                          f'{file_name}',
               f'{self._path_submission}/'
               f'{job_id}/run']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
            logger.info(proc.stdout.read())

    def run(self):

        self._init_directory_submission()
        if not self._get_submission():
            return

        _ = self._course_api_client.update_submission(self._submission.get('id'),
                                                      {"status": RUNNING_STATUS})

        jobs = self._course_api_client.get_list_of_jobs(submission_id=self._submission.get("id"))
        language = self._course_api_client.get_language_information(
            language_id=self._submission.get("language"))
        if len(jobs) == 0:
            logger.warning("pending submission  with 0 jobs")
            return
        if language is None:
            logger.warning("Language not found")
            return

        all_status = []
        for index, j in enumerate(jobs):
            tmp = self._run_jobs(j, language, self._submit_content.decode("utf-8"))
            all_status.append(tmp)
            if tmp != OK:
                for j2 in jobs[index+1:]:
                    self._course_api_client.update_job(j2.get('id'),
                                                       data={'status': 'CANCEL'})
                self._course_api_client.update_submission(self._submission.get('id'), data={
                    "status": ERROR if tmp is None else COMPILATION_ERROR_STATUS
                })
                break

        if all([st == OK for st in all_status]):
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": SUCCESS
            })
        elif any([st == WRONG_ANSWER for st in all_status]):
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": WRONG_ANSWER
            })
        elif any([st == TIMED_OUT for st in all_status]):
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": TIMED_OUT
            })
        elif any([st == RUNTIME_ERROR for st in all_status]):
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": RUNTIME_ERROR
            })
        elif any([st == SIGNALED for st in all_status]):
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": SIGNALED
            })
        else:
            self._course_api_client.update_submission(self._submission.get('id'), data={
                "status": ERROR
            })

    def _check_response(self, j, response, test_case_content_input, test_case_content_output):
        result_compilation = self._check_compilation(j, response)
        if result_compilation != "OK":
            logger.info("compilation error")
            return result_compilation
        result_exit_status = self._check_exit_status(j, response)
        if result_exit_status != "OK":
            logger.info("exit status problem")
            return result_exit_status
        logger.info("check answer")
        return self._check_answer(j, response, test_case_content_input, test_case_content_output)

    def _check_answer(self, j, response, test_case_input, test_case_content_output):
        tests_object = response.get('tests')
        first_test = tests_object[0]
        stdout = first_test.get("stdout")

        feedback_dir = f'{self._path_submission}/{j.get("id")}'

        with open(f'{feedback_dir}/in', 'w') as f:
            f.write(test_case_input)

        with open(f'{feedback_dir}/ans', 'w') as f:
            f.write(test_case_content_output)

        cmd = [f'{self._path_submission}/{j.get("id")}/run',
               f'{self._path_submission}/{j.get("id")}/in',
               f'{self._path_submission}/{j.get("id")}/ans',
               f'{self._path_submission}/{j.get("id")}']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, )
        out = proc.communicate(input=stdout.encode())[0]
        logger.info(out.decode().strip())

        return_code = proc.returncode
        logger.info(f"compare script exited with exit_code={return_code}")

        if return_code == EXIT_AC:
            ok, _ = self._course_api_client.update_job(j.get('id'),
                                                       data={"status": OK,
                                                             "log": json.dumps(response)})
            self._warn_message(ok, "error when updating jobs")
            return OK if ok else ERROR
        else:
            ok, _ = self._course_api_client.update_job(j.get('id'),
                                                       data={"status": WRONG_ANSWER,
                                                             "log": json.dumps(response)})
            self._warn_message(ok, "error when updating jobs")
            return WRONG_ANSWER if ok else ERROR

    @staticmethod
    def _warn_message(ok, msg):
        if not ok:
            logger.warning(msg)

    def _check_exit_status(self, j, response):
        logger.debug(response)
        tests_object = response.get('tests')
        if tests_object is None or len(tests_object) == 0:
            logger.info("test is none or empty")
            return "ERROR"
        first_test = tests_object[0]
        first_test_meta = first_test.get('meta', {})
        if "OK" not in first_test_meta.get('status').strip():
            logger.info(f"status is not OK '{first_test_meta.get('status')}'")
            logger.info(type(first_test_meta.get('status')))
            ok, _ = self._course_api_client.update_job(j.get('id'),
                                                       data={"status": first_test_meta.get(
                                                           'status'),
                                                           "log": json.dumps(response)})
            self._warn_message(ok, 'error when updating jobs')
            return first_test_meta.get('status')
        return "OK"

    def _check_compilation(self, j, response: dict):
        if 'error' in response or 'compile' not in response:
            ok, _ = self._course_api_client.update_job(j.get('id'),
                                                       data={"status": COMPILATION_ERROR_STATUS,
                                                             "log": json.dumps(response)})
            self._warn_message(ok, 'error when updating jobs')
            return COMPILATION_ERROR_STATUS

        compile_object = response.get('compile')
        if compile_object.get('exitcode') != 0 or compile_object.get('meta').get('exitcode') != 0 or \
                compile_object.get('meta').get('status') != 'OK':
            ok, _ = self._course_api_client.update_job(j.get('id'),
                                                       data={"status": COMPILATION_ERROR_STATUS,
                                                             "log": json.dumps(response)})
            self._warn_message(ok, 'error when updating jobs')
            return COMPILATION_ERROR_STATUS
        return 'OK'


def init_configuration(c):
    api_client = CourseApiClient(c)
    ok, answer = api_client.register()
    if not ok:
        logger.warning('Register KO')
        return
    logger.info('Register runner OK')
    if not os.path.exists("work"):
        os.mkdir("work")
    with open('.config', 'w') as f:
        f.close()


def run_camisole_server():
    logger.info("Run Camisole server")
    cmd = ['/usr/local/bin/camisole', 'serve', '-h', '127.0.0.1', '-p', '4242']
    p = subprocess.Popen(cmd)
    with open('.config', 'w') as f:
        f.write(str(p.pid))
    logger.info(f"The pid of camisole server is {p.pid}")


def run(sc):
    logger.info("Run thread")
    c = Config()
    logger.info(f"API COURSE URL: {c.course_url}")
    api_client = CourseApiClient(c)
    camisole_api_client = CamisoleAPiClient(c)
    try:
        next_submission = api_client.get_first_pending_submission()
    except ValueError:
        s.enter(c.time_waiting, 1, run, (sc,))
        return
    if len(next_submission) == 0:
        s.enter(c.time_waiting, 1, run, (sc,))
        return
    logger.info(next_submission)
    logger.info(f"Start execution of submission {next_submission['id']}")
    runner = Runner(next_submission, api_client, camisole_api_client)
    runner.run()
    logger.info(f"End execution of submission {next_submission['id']}")
    s.enter(c.time_waiting, 1, run, (sc,))
