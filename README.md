# ripe-atlas-scripts
Random scripts using RIPE Atlas API

## root-reachability.py
This scripts measures reachability to [K root server](https://www.ripe.net/analyse/dns/k-root/) from a given set of countries using DNS and Traceroute.
Obviously the target as well as country list can be modified for your own measurements.

Given that RIPE Atlas limits number of concurrent measurements toward the same destination, it yields error
messages if your request is rate limited. The script keeps track of created measurements in "meas-ids.json" file
in order to avoid creating duplicate measurements. You may want to re-run the script after a few minutes until all 
the measurements are created. You may also want to remove the sample "meas-ids.json" file if you want to create
your own set of measurements.

Please note that you have to get your own API Key from [RIPE Atlas](https://atlas.ripe.net/) website and modify the script to use your API Key.

Here is a sample measurement done using the script:

```
% ./root-reachability.py create
- Created measurement for DK
- Created measurement for NL
- Created measurement for IE
- Created measurement for DE
- Created measurement for FR
```

Now loading DNS measurements, output in CSV:
```
% ./root-reachability.py load-rtt
cc, num_probes,  avg_rtt
IE, 47, 42
FR, 48, 42
DE, 49, 49
DK, 45, 44
NL, 49, 21

```
And Traceroute measurements, output in CSV:
```
% ./root-reachability.py load-trace
cc, num_probes,  num_hops
DK, 47, 8
NL, 50, 6
IE, 47, 9
FR, 50, 11
```

