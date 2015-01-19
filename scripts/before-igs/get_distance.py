
filein = open('sample.list','r')

#qsub -v htfile="GS000a.fa.ht",seqfile="GS000a.fa" run_load.qsub

read_n = [0]*34
hit = [0]*34
count = 0

filein = ['AB','BH','IH','MH','BB','IB','MB','PB']

for line in filein:
  sample = line.rstrip()
  comb_file = sample+"tr.fq.trimmed.fq.comb"
  comb_fh = open(comb_file,'r')
  print comb_file
  read_n[count] = 0
  hit[count] = [0]*8
  for line in comb_fh:
      read_n[count] += 1
      line = line.rstrip()
      fields = line.split()[1:9]
      for s in range(8):
          if fields[s] != '0':
              hit[count][s] += 1


  count += 1
  print count
  if count == 8:
      break


distance = []
for x in range(8):
    d2 = []
    for y in range(8):
        dis = (hit[x][y] + hit[y][x])/(float(read_n[x]+read_n[y]))
        d2.append(dis)
    distance.append(d2)
fo = open('distance.txt','w')

for x in range(8):
    print distance[x]
    fo.write(str(x)+'   ')
    for y in range(8):
        fo.write(str(distance[x][y])+' ')
    fo.write('\n')


