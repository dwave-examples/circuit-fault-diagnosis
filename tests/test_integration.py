# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import unittest
from subprocess import Popen, PIPE ,STDOUT

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class IntegrationTests(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    def test_circuit_fault_diagnosis(self):
        demo_file = os.path.join(project_dir, 'demo.py')
        p = Popen([sys.executable, demo_file],
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(b'3\n')
        p.stdin.write(b'5\n')
        p.stdin.write(b'45\n')
        output = p.communicate()[0]
        output = str(output).upper()
        
        if os.getenv('DEBUG_OUTPUT'):
            print("Example output \n" + output)

        with self.subTest(msg="Verify if output contains 'The minimum fault diagnosis found' \n"):
            self.assertIn("The minimum fault diagnosis found".upper(), output)
        with self.subTest(msg="Verify if error string contains in output \n"):
            self.assertNotIn("ERROR", output)
        with self.subTest(msg="Verify if warning string contains in output \n"):
            self.assertNotIn("WARNING", output)

if __name__ == '__main__':
    unittest.main()
