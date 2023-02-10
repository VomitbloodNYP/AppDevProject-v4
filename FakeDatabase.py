# create fake database
import shelve, Pack

# create temp dict
pack_dict = {}

# open database
db = shelve.open('pack.db', 'c')

# assign database to temp dict
pack_dict = db['Packs']

# start assigning fake packs
pack_dict["pack1"] = Pack.Pack("pack1", 1, 100)
pack_dict["pack2"] = Pack.Pack("pack2", 2, 101)
pack_dict["pack3"] = Pack.Pack("pack3", 3, 102)
