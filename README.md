# MultiLevelHashRedis
This provides multi-level hash that can read and write dictionary on Hash Set field
Multi-level hash is to be able to store key-value pairs in Hash Set like:

<pre>
KEY: 
  FIELD:
    MHFIELD:
      VALUE
</pre>

For example, 

<pre>
"food":
  "meet":
    "spam":
      "good"
    "ham":
      "no good"
  "vegitable":
    "broccoli":
      "good"
</pre>

## How to use

<pre>
>>> import multihashredis
>>> redis = multihashredis.MultiLevelHashRedis()
>>> redis.mhset("food", "meet", "spam", "good")
1L
>>> redis.mhget("food", "meet", "spam")
good
>>> redis.mhset("food", "vegitable", "broccoli", "good")
1L
>>> redis.mhset("food", "meet", "ham", "no good")
1L
>>> redis.hget("food", "meet", multihash=True)
{ "spam": "good", "ham": "no good" }
>>> redis.hgetall("food", multihash=True)
{ "meet": { "spam": "good", "ham": "no good" } , "vegitable": { "broccoli", "good" } }
>>> redis.mhdel("food", "meet", "ham")
1L
>>> redis.hget("food", "meet", multihash=True)
{ "spam": "good" }
</pre>
