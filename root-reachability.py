import json
import os
import sys
from datetime import datetime

from ripe.atlas.cousteau import Traceroute, Dns, AtlasCreateRequest, AtlasSource, AtlasResultsRequest

# Globals
API_CREATE_KEY = ''


def create_measurement(cc):
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
    with open(fn, "w") as fp:  # save all ids to json
        json.dump(ids, fp)
        fp.flush()


def create_all(countries, ids):
    for cc in countries:
        if cc in ids:
            print("- measurement for %s already exists" % cc)
        else:
            res = create_measurement(cc)
            if res is not None:
                ids[cc] = res

    return ids


def dump_dns(ids):
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

            average = sum(rt_list) // len(rt_list)
            print("%s, %d, %d" % (cc, len(rt_list), average))


def dump_trace(ids):
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
    COUNTRIES = ['IR', 'EG', 'TR', 'IQ', 'SA', 'YE', 'SY', 'AE', 'IL', 'JO', 'PS', 'LB', 'OM', 'KW', 'QA', 'BH', 'AF']
    fn = "meas-ids.json"

    if len(sys.argv) < 2:
        print("please run with one of the following parameters: [create|load-dns|load-trace]")
        exit(0)
    _cmd = sys.argv[1].lower()
    if _cmd == 'create':
        ids = load_ids(fn)
        ids = create_all(countries=COUNTRIES, ids=ids)
        save_ids(fn, ids)
    elif _cmd == 'load-dns':
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
