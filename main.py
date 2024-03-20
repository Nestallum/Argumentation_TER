import graph_from_apx as gfa, util

file = gfa.get_command_args()
ug = gfa.read_UG_from_file(file)

print(util.Hbs(ug, 'i'))