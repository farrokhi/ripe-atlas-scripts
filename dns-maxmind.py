#!/usr/bin/env python3
#
# Copyright (c) 2016, Babak Farrokhi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import json
import os
import sys
from datetime import datetime


def load_ids(fn):
    """
    Loads measurement IDs from given file

    @param fn: input filename
    @type fn: str
    @return: Dictionary of loaded measurement IDs
    @rtype: dict
    """
    ids = {}

    if os.path.exists(fn):
        with open(fn, "r") as fp:  # save all ids to json
            try:
                ids = json.load(fp)
            except Exception as e:
                print(e)
                exit(1)
    return ids



def dump_dns(ids):
    for r in ids:
        try:
            rt = r.get("result")["answers"][0]["RDATA"][0]
            print(rt)
        except:
            pass


def main():
    if len(sys.argv) < 2:
        print("please provide json filename")
        exit(0)
    fn = sys.argv[1]

    ids = load_ids(fn)
    dump_dns(ids)


if __name__ == '__main__':
    main()
