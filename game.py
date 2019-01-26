import msvcrt
import os

def getvariable(currentlevel):
  entitees = {}
  l = 0
  while (l<len(currentlevel)):
    c = 0
    while (c<len(currentlevel[l])):
      if not currentlevel[l][c] in entitees:
        entitees[currentlevel[l][c]] = []
      entitees[currentlevel[l][c]].append({'l': l, 'c': c})
      c += 1
    l += 1
  return entitees
  
def getmatrix(l,c,entitees):
  currentlevel = []
  i = 0
  while(i<l):
    currentlevel.append([])
    j = 0
    while(j<c):
      currentlevel[len(currentlevel)-1].append(1)
      j += 1
    i += 1
  i = 0
  while(i<len(entitees)):
    j = 0
    while(j<len(entitees[i])):
      currentlevel[entitees[i][j]['l'],entitees[i][j]['c']] = entitees[i]
      j += 1	
    i += 1
  return currentlevel

def ifcollisions(currentlevel,entitees,inv,b,var,op,val,then,Else,l,c,playerid):
  if (((op == "==" or op == "=") and inv[var] == val) or
      (op == "!=" and inv[var] != val) or 
      (op == ">" and inv[var] > val) or
      (op == "<" and inv[var] < val) or
      (op == ">=" and inv[var] >= val) or
      (op == "<=" and inv[var] <= val)):
    i = 0
    while(i<len(then)):
      if (then[i]['type'] == 'mouv'):
        currentlevel,entitees,inv,b = mouv(int(then[i]['sens'].split(",")[0]),int(then[i]['sens'].split(",")[1]),currentlevel,entitees,inv,b,playerid)
      elif (then[i]['type'] == 'inv'):
        inv[then[i]['val']] += then[i]['coef']
      if (inv['pv'] == -1):
        b = "VOUS ESTS MORT"
      elif (then[i]['type'] == 'FIN'):
        b = "NIVEAU REUSSI"
      elif (then[i]['type'] == "put"):
        currentlevel[l][c] = then[i]['id']
      elif (then[i]['type'] == 'if'):
        EElse = []
        if 'else' in then[i]:
          EElse = then[i]['else']
        currentlevel,entitees,inv,b = ifcollisions(currentlevel,entitees,inv,b,then[i]['var'],then[i]['op'],then[i]['val'],then[i]['then'],EElse,l,c,playerid)
      i += 1
  else:
    i = 0
    while(i<len(Else)):
      if (Else[i]['type'] == 'mouv'):
        currentlevel,entitees,inv,b = mouv(int(Else[i]['sens'].split(",")[0]),int(Else[i]['sens'].split(",")[1]),currentlevel,entitees,inv,b,playerid)
      elif (Else[i]['type'] == 'inv'):
        inv[Else[i]['val']] += Else[i]['coef']
      if (inv['pv'] == -1):
        b = "VOUS ETES MORT"
      elif (Else[i]['type'] == 'FIN'):
        b = "NIVEAU REUSSI"
      elif (Else[i]['type'] == "put"):
        currentlevel[l][c] = Else[i]['id']
      elif (Else[i]['type'] == 'if'):
        EElse = []
        if 'else' in Else[i]:
          EElse = Else[i]['else']
        currentlevel,entitees,inv,b,playerid = ifcollisions(currentlevel,entitees,inv,b,Else[i]['var'],Else[i]['op'],Else[i]['val'],Else[i]['then'],EElse,l,c,playerid)
      i += 1
  return currentlevel,entitees,inv,b,playerid

def aff(currentlevel):
  l = 0
  while (l<len(currentlevel)):
    line = ""
    c = 0
    while (c<len(currentlevel[l])):
      #print "wesh " + str(currentlevel[l][c])
      line += graphics[currentlevel[l][c]]
      c += 1
    print line
    l += 1

def mouv(l,c,currentlevel,entitees,inv,b,playerid):
  cell = currentlevel[entitees[playerid][0]['l']+l][entitees[playerid][0]['c']+c]
  if (cell == 1 or cell == 5 or cell == 6 or cell == 7):
    currentlevel[entitees[playerid][0]['l']][entitees[playerid][0]['c']] = 1
    currentlevel[entitees[playerid][0]['l']+l][entitees[playerid][0]['c']+c] = playerid
    val = collisions['on'][cell]
    i = 0
    while (i<len(val)):
      if (val[i]['type'] == 'mouv'):
        currentlevel,entitees,inv,b,playerid = mouv(int(val[i]['sens'].split(",")[0])*l,int(val[i]['sens'].split(",")[1])*c,currentlevel,entitees,inv,b,playerid)
      elif (val[i]['type'] == 'inv'):
        inv[val[i]['val']] += val[i]['coef']
        if (inv['pv'] == -1):
          b = "VOUS ETES MORT"
      elif (val[i]['type'] == 'FIN'):
        b = "NIVEAU REUSSI"
      elif (val[i]['type'] == 'put'):
        currentlevel[entitees[playerid][0]['l']][entitees[playerid][0]['c']] = val[i]['id']
      elif (val[i]['type'] == 'if'):
        Else = []
        if 'else' in val[i]:
          Else = val[i]['else']
        currentlevel,entitees,inv,b,playerid = ifcollisions(currentlevel,entitees,inv,b,val[i]['var'],val[i]['op'],val[i]['val'],val[i]['then'],Else,entitees[playerid][0]['l'],entitees[playerid][0]['c'],playerid)
      i += 1
    entitees = getvariable(currentlevel)
  return currentlevel,entitees,inv,b,playerid
  

def interactmouv(l,c,currentlevel,entitees,inv,playerid):
  b = 1
  lplayer = entitees[playerid][0]['l']
  cplayer = entitees[playerid][0]['c']
  lpoint = lplayer+l
  cpoint = cplayer+c
  del entitees[playerid]
  #playeridold = playerid
  if (l == -1 and c == 0):
    playerid = 10
  elif (l == 1 and c == 0):
    playerid = 20
  elif (l == 0 and c == -1):
    playerid = 30
  elif (l == 0 and c == 1):
    playerid = 40
  currentlevel[lplayer][cplayer] = playerid
  entitees[playerid] = [{'l': lplayer, 'c': cplayer}]
  lim = len(collisions['mouv'][currentlevel[lpoint][cpoint]])
  val = collisions['mouv'][currentlevel[lpoint][cpoint]]
  #if (playeridold == playerid):
  i = 0
  while (i<lim):
    if (val[i]['type'] == 'mouv'):
      currentlevel,entitees,inv,b,playerid = mouv(int(val[i]['sens'].split(",")[0])*l,int(val[i]['sens'].split(",")[1])*c,currentlevel,entitees,inv,b,playerid)
    elif (val[i]['type'] == 'inv'):
      inv[val[i]['val']] += val[i]['coef']
      if (inv['pv'] == -1):
        b = "VOUS ETES MORT"
    elif (val[i]['type'] == 'FIN'):
      b = "NIVEAU REUSSI"
    elif (val[i]['type'] == 'put'):
        currentlevel[lpoint,cpoint] = val[i]['id']
    elif (val[i]['type'] == 'if'):
        Else = []
        if 'else' in val[i]:
          Else = val[i]['else']
        currentlevel,entitees,inv,b,playerid = ifcollisions(currentlevel,entitees,inv,b,val[i]['var'],val[i]['op'],val[i]['val'],val[i]['then'],Else,lpoint,cpoint,playerid)
    i += 1
  return currentlevel,entitees,inv,b,playerid
  
def interact(currentlevel,entitees,inv,playerid,sens):
  b = 1
  lplayer = entitees[playerid][0]['l']
  cplayer = entitees[playerid][0]['c']
  if (sens == "all"):
    concerns = [{'val': currentlevel[lplayer-1][cplayer], 'l': lplayer-1, 'c': cplayer},
                {'val': currentlevel[lplayer+1][cplayer], 'l': lplayer+1, 'c': cplayer},
                {'val': currentlevel[lplayer][cplayer-1], 'l': lplayer, 'c': cplayer-1},
                {'val': currentlevel[lplayer][cplayer+1], 'l': lplayer, 'c': cplayer+1}]
  elif (sens == "frontof"):
    if (playerid == 10):
      concerns = [{'val': currentlevel[lplayer-1][cplayer], 'l': lplayer-1, 'c': cplayer}]
    elif (playerid == 20):
      concerns = [{'val': currentlevel[lplayer+1][cplayer], 'l': lplayer+1, 'c': cplayer}]
    elif (playerid == 30):
      concerns = [{'val': currentlevel[lplayer][cplayer-1], 'l': lplayer, 'c': cplayer-1}]
    elif (playerid == 40):
      concerns = [{'val': currentlevel[lplayer][cplayer+1], 'l': lplayer, 'c': cplayer+1}]
  j = 0
  while(j<len(concerns)):
    i = 0
    val = collisions['interact'][concerns[j]['val']]
    while(i<len(val)):
      print val[i]['type']
      if (val[i]['type'] == 'mouv'):
        currentlevel,entitees,inv,b,playerid = mouv(int(val[i]['sens'].split(",")[0]),int(val[i]['sens'].split(",")[1]),currentlevel,entitees,inv,b,playerid)
      elif (val[i]['type'] == 'inv'):
        inv[val[i]['val']] += val[i]['coef']
        if (inv['pv'] == -1):
          b = "TES MORT SALE MERDE"
      elif (val[i]['type'] == 'FIN'):
        b = "NIVEAU REUSSI"
      elif (val[i]['type'] == 'put'):
        currentlevel[concerns[j]['l']][concerns[j]['c']] = val[i]['id']
      elif (val[i]['type'] == 'if'):
        Else = []
        if 'else' in val[i]:
          Else = val[i]['else']
        currentlevel,entitees,inv,b,playerid = ifcollisions(currentlevel,entitees,inv,b,val[i]['var'],val[i]['op'],val[i]['val'],val[i]['then'],Else,concerns[j]['l'],concerns[j]['c'],playerid)
      i += 1
    j += 1
  return currentlevel,entitees,inv,b,playerid



def start(level):
  inv = {"keys": 0, 'pv': 5}
  currentlevel = levels[level][0]
  playerid = levels[level][1]
  entitees = getvariable(currentlevel)
  b = 1
  while (b == 1):
    os.system("cls")
    aff(currentlevel)
    print "pv = " + str(inv['pv']) + " ; keys = " + str(inv['keys'])
    print "e pour interagir devant"
    print "f pour interagir tout autour"
    print "z,q,s,d pour se deplacer"
    char = msvcrt.getch()
    if (char == "z"):
      currentlevel,entitees,inv,b,playerid = interactmouv(-1,0,currentlevel,entitees,inv,playerid)
    elif (char == "s"):
      currentlevel,entitees,inv,b,playerid = interactmouv(1,0,currentlevel,entitees,inv,playerid)
    elif (char == "q"):
      currentlevel,entitees,inv,b,playerid = interactmouv(0,-1,currentlevel,entitees,inv,playerid)
    elif (char == "d"):
      currentlevel,entitees,inv,b,playerid = interactmouv(0,1,currentlevel,entitees,inv,playerid)
    elif (char == "e"):
      currentlevel,entitees,inv,b,playerid = interact(currentlevel,entitees,inv,playerid,"frontof")
    elif (char == "f"):
      currentlevel,entitees,inv,b,playerid = interact(currentlevel,entitees,inv,playerid,"all")
  print b
  os.system("pause")
  

graphics = { 10: '^', 20: 'V', 30: '<', 40: '>', 1: ' ', 2: '|', 3: '$', 4: '#', 5: "K", 6: "F", 7: "L" }

collisions = { 'mouv': { 1: [{'type': 'mouv', 'sens': '1,1'}], 2: [], 3: [], 4: [{'type': 'inv', 'val': 'pv', 'coef': -1},{'type': 'mouv', 'sens': '-1,-1'}], 5: [{'type': 'mouv', 'sens': '1,1'}], 6: [{'type': 'mouv', 'sens': '1,1'}], 7: [{'type': 'mouv', 'sens': '1,1'}]},
               'on' :  {1: [], 2: [], 3: [], 4: [], 5: [{'type': 'if', 'var': 'keys', 'op': '<', 'val': 20, 'then': [{'type': 'inv', 'val': 'keys', 'coef': 1}], 'else': [{'type': 'put', 'id': 5}]}], 6: [{'type': 'FIN'}], 7: [{'type': 'if', 'var': 'pv', 'op': '<', 'val': 15, 'then': [{'type': 'inv', 'val': 'pv', 'coef': 1}], 'else': [{'type': 'put', 'id': 7}]}]},
			   'interact' :  {1: [], 2: [], 3: [{'type': 'if', 'var': 'keys', 'op':'>', 'val': 0, 'then': [{'type': 'put', 'id': 1},{'type': 'inv', 'val': 'keys', 'coef': -1}]}], 4: [{'type': 'if', 'var': 'pv', 'op':'>', 'val': 0, 'then': [{'type': 'put', 'id': 1},{'type': 'inv', 'val': 'pv', 'coef': -1}]}], 5: [{'type': 'if', 'var': 'keys', 'op': '<', 'val': 20, 'then': [{'type': 'put', 'id': 1},{'type': 'inv', 'val': 'keys', 'coef': 1}]}], 6: [{'type': 'FIN'}], 7: [{'type': 'if', 'var': 'pv', 'op': '<', 'val': 15, 'then': [{'type': 'put', 'id': 1},{'type': 'inv', 'val': 'pv', 'coef': 1}]}]}}

levels = {'salle_vide': [[[2,2,2,2,2,2,2,2,2,2,2,2],
                          [2,5,1,1,1,1,1,1,1,1,1,2],
                          [2,1,1,1,1,1,1,1,1,4,1,2],
                          [2,1,1,1,2,2,2,2,1,1,1,2],
                          [2,1,1,1,2,1,1,2,1,1,1,2],
                          [2,1,4,1,3,1,1,3,1,1,1,2],
                          [2,1,1,1,2,6,1,2,1,1,1,2],
                          [2,4,1,1,2,2,2,2,1,1,1,2],
                          [2,1,1,1,1,1,1,1,1,1,1,2],
                          [2,1,1,1,1,10,1,1,1,1,1,2],
                          [2,2,2,2,2,2,2,2,2,2,2,2]],10], 

 'niveau_lambda':   [[[4,1,4,1,1,1,1,1,1,1],
                      [1,1,1,1,4,1,4,1,4,1],
                      [1,4,1,4,1,1,4,1,1,1],
                      [1,1,1,1,1,4,1,1,1,1],
                      [1,4,1,4,1,1,4,1,1,4],
                      [1,1,1,1,1,1,1,1,1,1],
                      [4,1,1,1,4,1,1,1,4,1],
                      [1,1,4,1,10,1,4,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1]],10],

        'parcourt': [[[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                      [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
                      [2,2,2,2,2,1,1,4,1,1,1,1,1,1,1,30,1,2],
                      [2,6,3,3,3,1,1,1,1,1,1,1,1,1,1,1,4,2],
                      [2,2,2,2,2,1,1,1,1,1,1,1,1,4,1,4,1,2],
                      [2,1,1,1,1,4,1,1,1,1,4,1,1,1,1,1,1,2],
                      [2,1,1,1,1,1,1,4,2,2,1,1,4,1,4,1,1,2],
                      [2,1,1,1,4,1,4,1,1,1,4,1,1,1,1,1,1,2],
                      [2,1,4,1,1,1,2,1,4,1,1,4,4,1,1,4,1,2],
                      [2,4,1,4,1,4,4,1,1,2,1,1,1,1,4,1,1,2],
                      [2,1,4,1,1,1,1,4,1,2,1,4,1,1,4,1,1,2],
                      [2,1,1,4,4,1,4,2,1,2,1,4,1,1,4,4,4,2],
                      [2,1,4,1,1,1,1,2,1,2,1,4,1,4,1,1,1,2],
                      [2,4,5,1,1,4,1,2,5,2,1,4,1,1,1,4,5,2],
                      [2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2]],30],
 
         'couloir': [[[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                      [2,7,7,7,7,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,2,2,2],
                      [2,7,7,7,1,1,2,4,4,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,6,2],
                      [2,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,1,1,1,1,4,1,4,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,1,1,1,1,4,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,2,2,2,2,2,4,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,40,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,2,2,2,2,2,2,2,1,1,1,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2],
                      [2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2],
                      [2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,2],
                      [2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                      [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,7,7,2],
                      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]],40]}

print "il ya " + str(len(levels)) + " niveaux : \n"
for name in levels:
   print name
print ""
level = raw_input("rentre le nom du niveau ou aller : ")
start(level)