from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-e", "--embedding", dest = "emb_path",
    required = True, help = "path to your embedding")

args = parser.parse_args()

words = {'American', 'Arafat', 'Brazil', 'CD', 'FBI', 'Freud', 'Harvard',
'Israel', 'Jackson', 'Japanese', 'Jerusalem', 'Maradona', 'Mars', 'Mexico',
'OPEC', 'Palestinian', 'Wednesday', 'Yale', 'abuse', 'accommodation',
'activity', 'admission', 'airport', 'alcohol', 'aluminum', 'animal',
'announcement', 'antecedent', 'anxiety', 'approach', 'architecture', 'archive',
'area', 'arrangement', 'arrival', 'article', 'artifact', 'association',
'astronomer', 'asylum', 'atmosphere', 'attempt', 'attitude', 'automobile',
'avenue', 'baby', 'bank', 'baseball', 'basketball', 'bed', 'benchmark', 'bird',
'bishop', 'block', 'board', 'book', 'boxing', 'boy', 'brandy', 'bread',
'brother', 'buck', 'butter', 'cabbage', 'calculation', 'canyon', 'car', 'card',
'carnivore', 'cash', 'cat', 'category', 'cell', 'cemetery', 'center', 'century',
'challenge', 'championship', 'chance', 'change', 'chemistry', 'children',
'chord', 'citizen', 'clinic', 'closet', 'clothes', 'coast', 'cock', 'coffee',
'cognition', 'collection', 'combination', 'communication', 'company',
'competition', 'computation', 'computer', 'concert', 'conclusion', 'confidence',
'constellation', 'consumer', 'country', 'crane', 'credibility', 'credit',
'crew', 'crisis', 'criterion', 'critic', 'cucumber', 'culture', 'cup',
'currency', 'dawn', 'day', 'death', 'decoration', 'defeat', 'defeating',
'delay', 'departure', 'deployment', 'deposit', 'depression', 'development',
'direction', 'disability', 'disaster', 'discipline', 'discovery', 'dividend',
'doctor', 'dollar', 'drink', 'drought', 'drug', 'ear', 'earning', 'eat',
'ecology', 'effort', 'egg', 'emergency', 'energy', 'entity', 'environment',
'equality', 'equipment', 'evidence', 'example', 'exhibit', 'experience', 'eye',
'family', 'fauna', 'fear', 'feline', 'fertility', 'fighting', 'film',
'fingerprint', 'five', 'flight', 'flood', 'focus', 'food', 'football',
'forecast', 'forest', 'fruit', 'fuck', 'furnace', 'gain', 'galaxy', 'game',
'gem', 'gender', 'gin', 'girl', 'glass', 'government', 'governor', 'graveyard',
'grocery', 'group', 'hardware', 'health', 'hike', 'hill', 'history', 'holy',
'hospital', 'hotel', 'hundred', 'hypertension', 'image', 'impartiality',
'implement', 'importance', 'index', 'industry', 'information', 'infrastructure',
'inmate', 'institution', 'insurance', 'interest', 'internet', 'interview',
'investigation', 'investor', 'isolation', 'issue', 'jaguar', 'jazz', 'jewel',
'journal', 'journey', 'keyboard', 'kilometer', 'kind', 'king', 'laboratory',
'lad', 'landscape', 'laundering', 'law', 'lawyer', 'lesson', 'liability',
'library', 'life', 'line', 'liquid', 'listing', 'live', 'lobster', 'loss',
'love', 'lover', 'luxury', 'madhouse', 'magician', 'maker', 'mammal', 'man',
'manslaughter', 'marathon', 'market', 'marriage', 'match', 'medal', 'media',
'memorabilia', 'metal', 'midday', 'mile', 'mind', 'minister', 'ministry',
'minority', 'money', 'monk', 'month', 'moon', 'morality', 'mother', 'motto',
'mouth', 'movie', 'murder', 'museum', 'music', 'nation', 'nature', 'network',
'news', 'noon', 'number', 'nurse', 'object', 'observation', 'office', 'oil',
'opera', 'operation', 'oracle', 'organism', 'paper', 'party', 'payment',
'peace', 'people', 'percent', 'performance', 'personnel', 'phone', 'physics',
'place', 'plan', 'plane', 'planet', 'planning', 'popcorn', 'population',
'possession', 'possibility', 'potato', 'practice', 'precedent', 'prejudice',
'preparation', 'preservation', 'president', 'price', 'problem', 'production',
'professor', 'profit', 'project', 'prominence', 'property', 'proton',
'proximity', 'psychiatry', 'psychology', 'quarrel', 'queen', 'rabbi', 'racism',
'racket', 'radio', 'reason', 'recess', 'recognition', 'recommendation',
'record', 'recovery', 'registration', 'report', 'reservation', 'rock', 'rook',
'rooster', 'round', 'row', 'school', 'science', 'scientist', 'sea', 'seafood',
'season', 'secret', 'secretary', 'seepage', 'senate', 'serial', 'series',
'seven', 'sex', 'shore', 'shower', 'sign', 'similarity', 'situation', 'size',
'skin', 'slave', 'smart', 'smile', 'soap', 'soccer', 'software', 'space',
'sprint', 'star', 'start', 'stock', 'stove', 'street', 'string', 'stroke',
'student', 'stupid', 'substance', 'sugar', 'summer', 'sun', 'surface',
'tableware', 'team', 'telephone', 'television', 'tennis', 'term', 'territory',
'terror', 'theater', 'thunderstorm', 'ticket', 'tiger', 'tool', 'tournament',
'trading', 'train', 'travel', 'treatment', 'troops', 'type', 'valor', 'victim',
'victory', 'video', 'viewer', 'virtuoso', 'vodka', 'volunteer', 'voyage', 'war',
'warning', 'water', 'wealth', 'weapon', 'weather', 'wine', 'withdrawal',
'wizard', 'woman', 'wood', 'woodland', 'word', 'world', 'year', 'yen', 'zoo'}

for row in open(args.emb_path):

    word, *_ = row.split()

    if word in words:
        print(row, end = "")
