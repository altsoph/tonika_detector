import yaml
from collections import defaultdict, Counter

def get_scale_gamma_notes(desc):
    scale = desc
    if " " in scale: 
        scale,gamma = scale.split(" ",1)
        if ' ' not in gamma and gamma != 'major':
            gamma += " minor"
    else:
        if scale[0].isupper():
            gamma = 'major'
        else:
            gamma = 'natural minor'
    notes = cfg[scale]['gammas'][gamma].replace(' ^ ', ' ').replace(' - ', ' ').split(' ')[:-1]
    notes = list(map(lambda x:note2base.get(x,x),notes))
    return scale,gamma,notes

def heuristic1135(notecount,paircount,options):
    scores = dict()
    for scale,mkey,gnotes in options:
        scores[(scale,mkey)] = 3*notecount.get(gnotes[0],0) + notecount.get(gnotes[2],0)
        scores[(scale,mkey)] += paircount.get( (gnotes[4],gnotes[0]),0) + paircount.get( (gnotes[0],gnotes[4]),0) + paircount.get( (gnotes[0],gnotes[2]),0)
        if mkey == 'major':
            scores[(scale,mkey)] += notecount.get(gnotes[4],0)
        else:
            scores[(scale,mkey)] += notecount.get(gnotes[5],0)
    best = max(scores.values())
    best_options = list(filter(lambda x:scores[x]==best,scores))
    return (best_options[0][0]+" "+best_options[0][1]).replace(' major','').replace(' minor','').replace(' natural','')

def detect_tonika(notes):
    parsed_notes = [base_notes[n%12] for n in notes]
    noteset = set(parsed_notes)
    notecount = Counter(parsed_notes)
    paircount = defaultdict(int)
    for _i in range( len(parsed_notes )-1):
        if parsed_notes[_i+1] != parsed_notes[_i]:
            paircount[ (parsed_notes[_i], parsed_notes[_i+1]) ] += 1
    shortlist_gammas = list(filter(lambda x:len(noteset-set(x[2]))==0, full_gammas)) # short list of gammas which has each of tune notes
    note = ''
    current = len(notecount)
    if len(shortlist_gammas) == 0:
        start = len(notecount)
        current = start-1
        while current>0:
            shortlist_gammas = list(filter(lambda x:len(set(dict(notecount.most_common(current)).keys())-set(x[2]))==0, full_gammas))
            if len(shortlist_gammas)>0: break
            current -= 1
        note = 'reduced'
    return heuristic1135(notecount,paircount,shortlist_gammas)


cfg_fn = 'tones.yaml'
cfg = yaml.load(open(cfg_fn, encoding='utf-8').read(), Loader=yaml.FullLoader)

# 0 - c, 1 - c#, 2 - d, 3 - d#, 4 - e, 5 - f, 6 - f#, 7 - g, 8 - g#, 9 - a, 10 - b, 11 - h
base_notes = ['c','cis','d','dis','e','f','fis','g','gis','a','b','h']

note2base  = {
    'ces':'h',
    'des':'cis',
    'es':'dis',
    'ees':'dis',
    'fes':'e',
    'ges':'fis',
    'aes':'gis',
    'as':'gis',
    'bes':'a',
    'hes':'b',
    'eis':'f',
    'ais':'b',
    'bis':'h',
    'his':'c',
}

scale2tonic = dict()
gammas = defaultdict(list) # gamma2scale
for t in cfg:
    for g in cfg[t]['gammas']:
        gamma =  frozenset(map(lambda x:note2base.get(x,x),cfg[t]['gammas'][g].replace(' ^','').replace(' -','').split()))
        gammas[gamma].append( t+" "+g )
    if 'major' in cfg[t]['gammas']:
        tonic = cfg[t]['gammas']['major'].replace(' ^','').replace(' -','').split()[0]
    else:
        tonic = cfg[t]['gammas']['natural minor'].replace(' ^','').replace(' -','').split()[0]
    scale2tonic[t] = note2base.get(tonic,tonic)

full_gammas = []
for sc in cfg:
    for gm in cfg[sc]['gammas']:
        sgn = get_scale_gamma_notes(sc+" "+gm)
        full_gammas.append( sgn )