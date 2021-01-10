from replit import db

fun_command_lst = [
        'roll',
        'emotion',
        'inspire',
        'quote',
        'someone',
				'yesno',
        ]

utility_command_lst = [
        'help',
        'delay',
        'infoserv',
        'time',
				'ping',
				'counter',
        ]

game_command_lst = [
				'guess',
				'roll-duel',
				'sequencer',
]

emotion_msg=[
'worthless','embarrassed','hopeful','resentful','satisfied','inspired','motivated','insecure','love','frustrated','peaceful','amazed','relieved','bored','envious','eager','comfortable','grieving','nervous','excited','terrified','depressed','happy','disgusted','jealous','annoyed','scared','silly','energetic','content','stupid','determined','disdain','sad','proud','lonely','furious','foolish','anxious','uncomfortable','shocked','inadequate','miserable','worried','conscious','hurt','joy','angry','ashamed',
]

greeting_msg=[
'hi!','hello','heya','hoi!','o/','o.','hey!'
]

cute_msg=[
'aww~','you\'re cute too~',"no u ♥",'fufufu~','u too ♥',"♥","big blobheart for you ♥",'how cute~','kawaii~',"😳"
]

yesno_msg=[
	'yes',
	'no',
	'probably yes',
	'probably no',
	'mmm...',
	'definitively no',
	'YES YES YES',
	'well perhaps...',
	'no way',
	'not so certain',
	'questionnable',
	'most unlikely',
	'bruh',
	'no doubt',
	'certainly',
	'unthinkable',
]

choosen_msg =[]

def add_in(msg,keyname):
  if keyname in db.keys():
    lst = db[keyname]
    lst.append(msg)
    db[keyname] = lst
  else:
    db[keyname] = [msg]

def is_in(msg,keyname):
  if keyname in db.keys():
    data = db[keyname]
    try: 
      return data.index(msg)
    except:
      return False

  else: 
    return False

def remove_out(msg,keyname):
  i = is_in(msg,keyname)
  if (i):
    data = db[keyname]
    db[keyname] = data.pop(i)

def list_keys():
  return db.keys()

def list_keys_prefix(prefix):
  return db.prefix(prefix)