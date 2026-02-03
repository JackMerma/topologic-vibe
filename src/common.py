# Topologic
from topologicpy.Topology import Topology
from topologicpy.Dictionary import Dictionary

def assign_name(obj, name: str):
    keys = ["name"]
    values = [name]
    config = Dictionary.ByKeysValues(keys, values)
    obj = Topology.SetDictionary(obj, config)
    return obj