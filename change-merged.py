#!/usr/bin/env python
#
# Copyright (c) 2012, JT Olds <hello@jtolds.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
    Gerrit Webhook
"""

__author__ = "JT Olds"
__author_email__ = "hello@jtolds.com"

GERRIT_URL = "http://gerrit.example.com/"
GERRIT_NAME = "Gerrit Code Review"
GERRIT_DESCRIPTION = ""
GERRIT_OWNER_NAME = "Admin"
GERRIT_OWNER_EMAIL = "admin@example.com"
GERRIT_PORT = 29418
GERRIT_SERVER = "localhost"
WEBHOOK_URL = "http://webhook.example.com/new-commit"

import json
import time
import urllib
import urllib2
import subprocess
from optparse import OptionParser


def getCommitInfo(commit_hash):
    try:
        result = json.loads(subprocess.check_output(
                ["ssh", "-p", str(GERRIT_PORT), GERRIT_SERVER, "gerrit",
                 "query", "--commit-message", "--format", "json",
                 commit_hash]).split("\n")[0])
        return (result["commitMessage"], result["lastUpdated"],
                result["owner"]["name"], result["owner"]["email"])
    except Exception, e:
        return ("Failed getting commit message, %s: %s" % (
                    e.__class__.__name__, e),
                int(time.time()), "unknown user", "unknown@example.com")


def webhook(commit_hash, branch, name, email, change_url, message, timestamp):
    data = {
        "before": "",
        "after": commit_hash,
        "ref": "refs/heads/%s" % branch,
        "repository": {
            "url": GERRIT_URL,
            "name": GERRIT_NAME,
            "description": GERRIT_DESCRIPTION,
            "owner": {
                "name": GERRIT_OWNER_NAME,
                "email": GERRIT_OWNER_EMAIL}},
        "commits": [{"id": commit_hash,
                     "author": {"name": name, "email": email},
                     "url": change_url,
                     "message": message,
                     "timestamp": timestamp}]}
    urllib2.urlopen(WEBHOOK_URL,
                    urllib.urlencode({"payload": json.dumps(data)})).read()


def main():
    parser = OptionParser(usage="usage: %prog <required options>")
    parser.add_option("--change", help="Change identifier")
    parser.add_option("--change-url", help="Change url")
    parser.add_option("--project", help="Project path in Gerrit")
    parser.add_option("--branch", help="Branch name")
    parser.add_option("--topic", help="Topic name")
    parser.add_option("--submitter", help="Submitter")
    parser.add_option("--commit", help="Git commit hash")

    options, args = parser.parse_args()
    message, timestamp, name, email = getCommitInfo(options.commit)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))
    webhook(options.commit, options.branch, name, email, options.change_url,
            message, timestamp)


if __name__ == "__main__":
    main()
