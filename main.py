import IO_graph_apx as gfa, util

UG = {"i":["a","b","g"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[], "g":["d"]}
# file = gfa.get_command_args()
# ug = gfa.read_UG_from_file(file)
# print(util.Hbs(ug, 'i'))
gfa.write_apx_from_graph("apx2", "test2", UG)