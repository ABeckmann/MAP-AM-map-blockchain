import hashlib

FAMILY_NAME = 'map'
FAMILY_VERSION = '1.0'
NAMESPACE = hashlib.sha512(FAMILY_NAME.encode("utf-8")).hexdigest()[0:6]
#PAYLOAD_SEARIALISATION = action, name_id, owner, new_owner, usage, value, signed_value, remove_signed_value, repairs, security_tag_public_key, parent, child, blueprint, list_of_blueprint_connections


DISTRIBUTION_NAME = 'sawtooth-map'

def _hash62(name):
    return _hash(name, 62)

def _hash64(name):
    return _hash(name, 64)


def _hash(name, length):
    return hashlib.sha512(name.encode('utf-8')).hexdigest()[:length]

def make_address_video_licence_contract(id):
     return NAMESPACE + _hash64(id)  
