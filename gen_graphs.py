import snap

facebook_input_path = 'facebook_combined.txt'
facebook_output_path = 'subgraphs/facebook.elist'

input_file = open(facebook_input_path, 'r')
output_file = open(facebook_output_path, 'w')

for line in input_file:
    nodes = line.split()
    if int(nodes[0]) % 5 != 0 and int(nodes[1]) % 5 != 0:
        output_file.write(nodes[0] + ' ' + nodes[1])
        output_file.write('\n')

input_file.close()
output_file.close()

"--------------------------------------------------"

twitter_input_path = 'twitter_combined.txt'
twitter_output_path = 'subgraphs/twitter.elist'

input_file = open(twitter_input_path, 'r')
output_file = open(twitter_output_path, 'w')

for line in input_file:
    nodes = line.split()
    if int(nodes[0]) % 3 == 0 and int(nodes[1]) % 3 == 0:
        output_file.write(nodes[0] + ' ' + nodes[1])
        output_file.write('\n')

input_file.close()
output_file.close()

"--------------------------------------------------"

output_path_random = 'networks/random.elist'
random_graph = snap.GenRndGnm(snap.TUNGraph, 1000, 50000)

output_file = open(output_path_random, 'w')

for EI in random_graph.Edges():
    output_file.write(str(EI.GetSrcNId()) + ' ' + str(EI.GetDstNId()))
    output_file.write('\n')

output_file.close()

"--------------------------------------------------"

Rnd = snap.TRnd(42)
Rnd.Randomize()

output_path_small_world = 'networks/smallworld.elist'
small_world_graph = snap.GenSmallWorld(1000, 50,  0.6, Rnd)

output_file = open(output_path_small_world, 'w')

for EI in small_world_graph.Edges():
    output_file.write(str(EI.GetSrcNId()) + ' ' + str(EI.GetDstNId()))
    output_file.write('\n')

output_file.close()

"--------------------------------------------------"
