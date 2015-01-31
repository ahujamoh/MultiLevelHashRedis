# -*- coding: utf-8 -*-

# 3rd party lib
from redis import Redis
import msgpack
from msgpack import ExtraData


class MultiLevelHashRedis(Redis):
    """
    """

    def __init__(self, **kwargs):
	super(MultiLevelHashRedis, self).__init__(**kwargs)

    def mhset(self, key, field, mh_field, mh_value):
	"""
	Sets multi-level hash value in Hash set.
	If field already exists in the hash, it is overwritten.
	key: 
	  field:
	    mh_field: mh_value 
	"""
	value = self.hget(key, field)
	if value:
            value = self._load_msgpack_value(value)
	
	    if isinstance(value, dict):
                value[mh_field] = mh_value
            else:
		print("invalid type:{}".format(type(value)))
                return 0
	else:
	    value = { mh_field: mh_value } 
        return self.hset(key, field, msgpack.dumps(value))
    

    def mhget(self, key, field, mh_field):
	"""
	Gets value in multi-level hash field in Hash set.
	If field does not exist, this returns None.
	key:
	  field:
	    mh_field: (ret_val)
	"""
	value = self.hget(key, field)
	if value:
            value = self._load_msgpack_value(value)

            if isinstance(value, dict):
                if mh_field in value:
                    return value[mh_field]
        return None
	
	return msgpack.loads(self.hget(key, field))

    def hget(self, key, field, multihash=False):
        """
	Override from hget in Redis.
	If multihash option is True, this gets a dict of multi level hash by decoding msgpack.
	key:
	  field:
	     (ret_val)
        """
        value = super(MultiLevelHashRedis, self).hget(key, field)
        if not multihash:
            return value
        return self._load_msgpack_value(value)

    def mhgetall(self, key, field):
        """
        Gets a dict of multi level hash by decoding msgpack. 
	This is equivalent to hget with multihash option having True.
	key:
	  field:
	    (ret_val)
        """
        value = self.hget(key, field)
        if value:
            value = self._load_msgpack_value(value)
            return value
        return None

    def hgetall(self, key, multihash=False):
	"""
	Override from hgetall in Redis.
	If multihash option is True, this gets a dict of multi level hash by decoding msgpack.
	key:
	  (ret_val)
	"""
        fields = super(MultiLevelHashRedis, self).hgetall(key)
        if not multihash:
	    return fields
        ret =  {}
        if fields:
            for key, val in fields.iteritems():
    	        try:
                    ret[key] = msgpack.loads(val)
                except ExtraData:
                    # when faild to load msgpack, proceed as text
    	            ret[key] = val
        return ret

    def mhdel(self, key, field, mh_field):
        """
	Deletes value of mh_filed in Multi level hash set of Hash set.
	If field does not exist, return 0.
	key:
	  field:
	    mh_field: (delete_val)
	"""
        value = self.hget(key, field)
        if value:
            value = self._load_msgpack_value(value)

            if isinstance(value, dict):
                value.pop(mh_field, None)
		return self.hset(key, field, msgpack.dumps(value))
        return 0

    def hdel(self, key, field, multihash=False):
        """
        Deletes value of field in Multi level hash set or Hash set.
        """
	return super(MultiHashRedis, self).hdel(key, field)

    def  _load_msgpack_value(self, value):
        """
        """
	if value is None:
	    return
        try:
            return msgpack.loads(value)
        except ExtraData:
            return value
