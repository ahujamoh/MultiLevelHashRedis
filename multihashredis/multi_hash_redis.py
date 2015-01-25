# -*- coding: utf-8 -*-

# 3rd party lib
from redis import Redis
import msgpack
from msgpack import ExtraData


class MultiHashRedis(Redis):
    """
    """

    def __init__(self, **kwargs):
	super(MultiHashRedis, self).__init__(**kwargs)

    def mhset(self, key, field, mh_field, mh_value):
	"""
	"""
	value = self.hget(key, field)
	if value:
            value = self._load_msgpack_value(value)
	
	    if isinstance(value, dict):
                value[mh_field] = mh_value
            else:
		print("invalid type:{}".format(type(value)))
                return 1L
	else:
	    value = { mh_field: mh_value } 
        return self.hset(key, field, msgpack.dumps(value))
    

    def mhget(self, key, field, mh_field):
	"""
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
        """
        value = super(MultiHashRedis, self).hget(key, field)
        if not multihash:
            return value
        return self._load_msgpack_value(value)

    def mhgetall(self, key, field):
        """
        """
        value = self.hget(key, field)
        if value:
            value = self._load_msgpack_value(value)
            return value
        return None

    def hgetall(self, key, multihash=False):
	"""
	Override
	"""
        fields = super(MultiHashRedis, self).hgetall(key)
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
	"""
        value = self.hget(key, field)
        if value:
            value = self._load_msgpack_value(value)

            if isinstance(value, dict):
                value.pop(mh_field, None)
		return self.hset(key, field, msgpack.dumps(value))
        return 1L

    def  _load_msgpack_value(self, value):
        """
        """
        try:
            return msgpack.loads(value)
        except ExtraData:
            return value
