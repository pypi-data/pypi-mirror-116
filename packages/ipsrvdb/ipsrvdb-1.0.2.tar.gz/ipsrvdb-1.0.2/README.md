# ipsrvdb-python

# Feature
1. Support Python2 & Python3.
2. Support IPv4 & IPv6.
3. Support output db date, description and header.
4. Support output raw IP info and IP info in a dinctionary.
5. Support load the database into memory or using MMAP.
6. No dependent.

# Installing
```
pip install ipsrvdb
```

# Example
```
import ipsrvdb

if __name__ == "__main__":
    # mode options: MEMORY, MMAP
    a = ipsrvdb.IPSrvDB("/path/to/ipsrv.dat", mode="MEMORY")
    print(a.find('8.8.8.255'))
    print(a.findx('8.8.8.255'))
    print(a.findx('2001:250::ffff'))
    print(a.get_header())
    print(a.get_date())
    print(a.get_description())
```

# Output
```
NA,北美洲,US,美国,,,,,,
{u'isp_zh': u'', u'country_iso_code': u'US', u'country_zh': u'\u7f8e\u56fd', u'province_zh': u'', u'city_zh': u'', u'continent_code': u'NA', u'org': u'', u'continent_zh': u'\u5317\u7f8e\u6d32', u'city_code': u'', u'province_iso_code': u''}
{u'isp_zh': u'\u4e2d\u56fd\u6559\u80b2\u7f51', u'country_iso_code': u'CN', u'country_zh': u'\u4e2d\u56fd', u'province_zh': u'\u5317\u4eac\u5e02', u'city_zh': u'', u'continent_code': u'AS', u'org': u'', u'continent_zh': u'\u4e9a\u6d32', u'city_code': u'', u'province_iso_code': u'11'}
[u'continent_code', u'continent_zh', u'country_iso_code', u'country_zh', u'province_iso_code', u'province_zh', u'city_code', u'city_zh', u'isp_zh', u'org']
20210811
IPSrv, Inc. Dat database.
```
