#!/usr/bin/env python
#
# Copyright 2016 Yoann Gini
# Tweaked by Steve Quirke 2017
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

"""See docstring for AWS_S3_Sync class"""

from autopkglib import Processor
from subprocess import call

#pylint: disable=no-name-in-module
try:
    from Foundation import CFPreferencesCopyAppValue
except:
    print "WARNING: Failed 'from Foundation import CFPreferencesCopyAppValue' in " + __name__
#pylint: enable=no-name-in-module

__all__ = ["AWS_S3_Sync"]


class AWS_S3_Sync(Processor):
    """Sync the files from a Munki repo to an Amazon S3 bucket. Repo location is pulled from
       the com.github.autopkg domain, and the s3 location from the com.thoughtworks.s3.sync domain"""
    description = __doc__
    input_variables = {
    }
    output_variables = {
    }
    def main(self):
        repo_path = CFPreferencesCopyAppValue(
            "MUNKI_REPO",
            "com.github.autopkg")
        s3_path = CFPreferencesCopyAppValue(
            "S3_PATH",
            "com.thoughtworks.s3.sync")
        if repo_path and s3_path:
            call(['aws', 's3', 'sync', '--exclude', '.git/*', '--delete', repo_path, s3_path])
        else:
            self.output("No munki repo set - and/or no S3 path set - nothing synchronised")

if __name__ == "__main__":
    PROCESSOR = AWS_S3_Sync()
    PROCESSOR.execute_shell()
