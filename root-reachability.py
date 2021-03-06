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

from ripe.atlas.cousteau import Traceroute, Dns, AtlasCreateRequest, AtlasSource, AtlasResultsRequest

# Globals
API_CREATE_KEY = ''


def create_measurement(cc):
    """
    Creates DNS and Traceroute measurements for given country code

    @param cc: Two characters (ISO) country code
    @type cc: str
    @return: tuple of measurement ids
    @rtype: tuple
    """
    global API_CREATE_KEY

    traceroute = Traceroute(af=4, target="193.0.14.129", protocol="ICMP",
                            description="Traceroute from %s to K Root" % cc)
    dns = Dns(af=4, target="193.0.14.129", query_argument="com.", query_type="NS", query_class="IN",
              description="DNS Response time fromt %s to K Root" % cc)

    source = AtlasSource(value=cc,
                         requested=50,
                         type="country",
                         action="add")
    request = AtlasCreateRequest(start_time=datetime.utcnow(),
                                 key=API_CREATE_KEY,
                                 measurements=[traceroute, dns],
                                 sources=[source],
                                 is_oneoff=True)

    (is_success, response) = request.create()

    if is_success:
        print("- Created measurement for %s" % cc)
        return list(response['measurements'])
    else:
        print("- Failed to create measurement for %s: %s" % (cc, response))
        return None


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


def save_ids(fn, ids):
    """
    Saves given dictionary of measurement IDs to file

    @param fn: input filename
    @type fn: str
    @param ids: Dictionary of IDs
    @type ids: dict
    @return: None
    """
    with open(fn, "w") as fp:  # save all ids to json
        json.dump(ids, fp)
        fp.flush()


def create_all(countries, ids):
    """"
    Iterates over list of given country codes and creates atlas measurement for each,
    if it is not already created considering list of IDs

    @param countries: list of country codes
    @type countries: list
    @param ids: dictionary of existing measurement IDs
    @type ids: dict
    @return updated dictionary of ids
    @rtype: dict
    """
    for cc in countries:
        if cc in ids:
            print("- measurement for %s already exists" % cc)
        else:
            res = create_measurement(cc)
            if res is not None:
                ids[cc] = res

    return ids


def dump_dns(ids):
    """
    fetches and calculates and dumps to console the DNS measurements for all countries given in IDs dict

    @param ids: dict of measurement ids
    @type ids: dict
    @return: None
    """
    print("cc, num_probes,  avg_rtt")
    for cc, mid in ids.items():
        is_success, results = AtlasResultsRequest(msm_id=mid[1]).create()
        rt_list = []
        if is_success:
            for r in results:
                try:
                    rt = r.get("result")["rt"]
                    if rt > 0:
                        rt_list.append(rt)
                except:
                    pass

            if len(rt_list)>0:
                average = sum(rt_list) // len(rt_list)
            else:
                average = 0
            print("%s, %d, %d" % (cc, len(rt_list), average))


def dump_trace(ids):
    """
    fetches and calculates and dumps to console the Traceroute measurements for all countries given in IDs list

    @param ids: dict of measurement ids
    @type ids: dict
    @return: None
    """
    print("cc, num_probes,  num_hops")
    for cc, mid in ids.items():
        is_success, results = AtlasResultsRequest(msm_id=mid[0]).create()
        hop_counts = []
        if is_success:
            for r in results:
                try:
                    trace = r.get("result")
                    hops = len(trace)
                    hop_counts.append(hops)
                except:
                    hops = 0

            average = sum(hop_counts) // len(hop_counts)
            print("%s, %d, %d" % (cc, len(hop_counts), average))


def main():
    COUNTRIES = "UZ UA TM TJ RU LV KZ KG GE EE BY AZ AM".split()
    fn = "meas-ids.json"

    if len(sys.argv) < 2:
        print("please run with one of the following parameters: [create|load-rtt|load-trace]")
        exit(0)
    _cmd = sys.argv[1].lower()
    if _cmd == 'create':
        ids = load_ids(fn)
        ids = create_all(countries=COUNTRIES, ids=ids)
        save_ids(fn, ids)
    elif _cmd == 'load-rtt':
        ids = load_ids(fn)
        dump_dns(ids)
    elif _cmd == 'load-trace':
        ids = load_ids(fn)
        dump_trace(ids)
    else:
        print("invalid parameter:", _cmd)
        exit(1)


if __name__ == '__main__':
    main()
