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
'contempt','disgust','revulsion',
'envy','jealousy',
'exasperation','frustration',
'aggravation','agitation','annoyance','grouchiness','grumpiness','irritation',
'anger','bitterness','dislike','ferocity','fury','hate','hostility','loathing','outrage','rage','resentment','scorn','spite','vengefulness','wrath',
'torment',
'alarm','fear','fright','horror','hysteria','mortification','panic','shock','terror',
'anxiety','apprehension','distress','dread','nervousness','tenseness','uneasiness','worry',
'amusement','bliss','cheerfulness','delight','ecstasy','elation','enjoyment','euphoria','gaiety','gladness','glee','happiness','jolliness','joviality','joy','jubilation','satisfaction',
'contentment','pleasure',
'enthrallment','rapture',
'eagerness','hope','optimism',
'Pride','triumph',
'enthusiasm','excitement','exhilaration','thrill','zeal','zest',
'adoration','affection','attraction','caring','compassion','fondness','liking','love','sentimentality','tenderness',
'arousal','desire','infatuation','lust','passion',
'disappointment','dismay','displeasure',
'alienation','defeat','dejection','embarrassment','homesickness','humiliation','insecurity','isolation','insult','loneliness','neglect',
'depression','despair','gloom','glumness','grief','hopelessness','melancholy','misery','sadness','sorrow','unhappiness',
'guilt','regret','remorse','shame',
'agony','anguish','hurt','suffering',
'pity','sympathy',
'amazement','astonishment','surprise'
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