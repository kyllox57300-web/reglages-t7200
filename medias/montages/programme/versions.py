import sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from montage import *

def seg(src, ss, dur, z0=1.0, z1=1.1, fx=(0.5, 0.5), fy=(0.5, 0.5), grade=None, dim=0, dimlow=0.35):
    d = dict(src=src, ss=ss, dur=dur, z0=z0, z1=z1, fx=fx, fy=fy, dim=dim, dimlow=dimlow)
    if grade: d['grade'] = grade
    return d

# ---------- briques communes ----------
def hook(E, FL, SH):
    plan = [seg(A, 11.9, 1.0, 1.05, 1.22, fy=(0.6, 0.62), dim=0.45, dimlow=0),
            seg(B, 15.8, 1.0, 1.0, 1.12, fx=(0.55, 0.55), dim=0.45, dimlow=0)]
    E += [El(pill('BLACK FRIDAY', 150, YEL, BLACK), 0.0, 2.0, 540, 560, 'slam'),
          El(panel(900, 610), 0.5, 2.0, 540, 965, 'pop'),
          El(big('JUSQU’À', 120, WHITE, 9), 0.5, 2.0, 540, 728, 'pop'),
          El(big('-50' + NB + '%', 420, YEL, 16), 0.5, 2.0, 540, 950, 'slam'),
          El(pill('DU 19 AU 30 NOVEMBRE', 92, WHITE, BLUE), 1.0, 2.0, 540, 1190, 'up')]
    FL += [0.0, 0.5]; SH += [(0.0, 0.25), (0.5, 0.3)]
    return plan

PRODUITS = {
    'enduit':  (seg(A, 6.55, 1.5, 1.0, 1.12, fy=(0.38, 0.36)), 'ENDUIT À BANDE EN PÂTE 25' + NB + 'KG', '11,45' + NB + '€'),
    'peinture': (seg(A, 15.65, 1.5, 1.15, 1.25, fy=(0.68, 0.68)), 'PEINTURE SATIN MOCACCINO 0,75' + NB + 'L', '13,73' + NB + '€'),
    'vasque':  (seg(B, 3.6, 1.5, 1.0, 1.1, fy=(0.45, 0.45)), 'ENSEMBLE SALLE DE BAIN 80' + NB + 'CM', '62,45' + NB + '€'),
    'cadre':   (seg(B, 9.6, 1.5, 1.0, 1.1), 'PIED CADRE 630' + NB + '×' + NB + '1060' + NB + 'MM', '34,95' + NB + '€'),
    'caisson': (seg(A, 8.15, 1.5, 1.0, 1.1, fy=(0.5, 0.5)), 'CAISSON RANGE-BOUTEILLES', '39,30' + NB + '€'),
}

def produit(key, t, E):
    s, name, price = PRODUITS[key]
    E += [El(pill(name, 78, WHITE, BLACK), t, t + s['dur'], 540, 1060, 'up'),
          El(price_tag(price), t + 0.25, t + s['dur'], 540, 1285, 'tag')]
    return s

def fin(t, dur, E, FL):
    E += [El(logo_card(780), t, t + dur, 540, 575, 'pop'),
          El(pill('BLACK FRIDAY · JUSQU’AU 30 NOVEMBRE', 74, YEL, BLACK), t + 0.4, t + dur, 540, 905, 'up'),
          El(big('ZAC DE LA FELTIÈRE · FAMECK', 70, WHITE, 6, path=BARLOW), t + 0.75, t + dur, 540, 1025, 'up'),
          El(big('DU LUNDI AU SAMEDI · 7' + NB + 'H – 19' + NB + 'H', 70, YEL, 6, path=BARLOW), t + 1.0, t + dur, 540, 1110, 'up'),
          El(pill('VIENS NOUS VOIR' + NB + '!', 140, BLACK, YEL, padx=44, pady=24), t + 1.5, t + dur, 540, 1270, 'pulse'),
          El(big('Offre dans la limite des stocks disponibles.', 38, WHITE, 3, path=BARLOW), t + 1.5, t + dur, 540, 1395, 'up')]
    FL.append(t)
    return seg('END', 26.0, dur)

# ---------- version longue ----------
def longue():
    E, FL, SH = [], [], []
    plan = hook(E, FL, SH)
    plan += [seg(C, 0.2, 1.5, 1.05, 1.2, fx=(0.5, 0.55), fy=(0.42, 0.4), grade=NIGHT)]
    E += [El(big('RENDEZ-VOUS CHEZ', 150, WHITE, 11), 2.0, 3.5, 540, 790, 'pop'),
          El(pill('BRICO CASH FAMECK', 130, WHITE, BLUE), 2.5, 3.5, 540, 975, 'slam')]
    SH.append((2.5, 0.2))
    plan += [seg(C, 4.7, 1.0, 1.0, 1.12, dim=0.3, dimlow=0), seg(C, 11.2, 1.0, 1.0, 1.12, dim=0.3, dimlow=0)]
    E += [El(big('ICI, ON SE', 200, WHITE, 12), 3.5, 5.5, 540, 820, 'left'),
          El(big('PARLE CASH' + NB + '!', 200, YEL, 12), 4.0, 5.5, 540, 1020, 'right')]
    SH.append((4.0, 0.2))
    t = 5.5
    for k in ['enduit', 'peinture', 'vasque', 'cadre', 'caisson']:
        plan.append(produit(k, t, E)); t += 1.5
    # t = 13.0 : outillage
    plan += [seg(C, 18.2, 1.0, 1.0, 1.1, dim=0.3, dimlow=0), seg(C, 26.0, 1.0, 1.0, 1.1, dim=0.3, dimlow=0), seg(C, 36.6, 1.0, 1.0, 1.1, dim=0.3, dimlow=0)]
    E += [El(big('ET PLEIN', 190, WHITE, 12), t, t + 3.0, 540, 760, 'pop'),
          El(big('D’AUTRES', 190, WHITE, 12), t + 0.5, t + 3.0, 540, 945, 'pop'),
          El(big('BONS PLANS' + NB + '!', 190, YEL, 12), t + 1.0, t + 3.0, 540, 1130, 'slam')]
    SH.append((t + 1.0, 0.25)); t += 3.0
    # t = 16.0 : allée, slogan
    plan.append(seg(C, 15.70, 2.0, 1.0, 1.15, dim=0.3, dimlow=0))
    E += [El(pill('+ DE STOCK', 170, WHITE, BLUE), t, t + 2.0, 540, 830, 'left'),
          El(pill('+ DE PRIX BAS', 170, BLACK, YEL), t + 0.5, t + 2.0, 540, 1040, 'right')]
    t += 2.0
    # t = 18.0 : quantités limitées (bannière du magasin)
    plan.append(seg(C, 23.6, 1.5, 1.0, 1.1, dim=0.3, dimlow=0))
    E += [El(big('QUANTITÉS LIMITÉES', 170, WHITE, 12), t, t + 1.5, 540, 790, 'slam'),
          El(pill('PREMIERS ARRIVÉS,', 110, BLACK, YEL), t + 0.5, t + 1.5, 540, 960, 'up'),
          El(pill('PREMIERS SERVIS' + NB + '!', 110, BLACK, YEL), t + 0.75, t + 1.5, 540, 1100, 'up')]
    SH.append((t, 0.25)); FL.append(t); t += 1.5
    plan.append(fin(t, 5.0, E, FL)); t += 5.0
    return plan, E, FL, SH, t

# ---------- version courte ----------
def courte():
    E, FL, SH = [], [], []
    plan = hook(E, FL, SH)
    plan += [seg(C, 0.4, 1.0, 1.05, 1.18, fx=(0.5, 0.55), fy=(0.42, 0.4), grade=NIGHT)]
    E += [El(pill('BRICO CASH FAMECK', 130, WHITE, BLUE), 2.0, 3.0, 540, 900, 'slam')]
    SH.append((2.0, 0.2))
    t = 3.0
    for k in ['enduit', 'peinture', 'vasque']:
        plan.append(produit(k, t, E)); t += 1.5
    plan.append(seg(C, 26.0, 1.0, 1.0, 1.1, dim=0.3, dimlow=0))
    E += [El(big('ET PLEIN', 190, WHITE, 12), t, t + 1.0, 540, 760, 'pop'),
          El(big('D’AUTRES', 190, WHITE, 12), t + 0.25, t + 1.0, 540, 945, 'pop'),
          El(big('BONS PLANS' + NB + '!', 190, YEL, 12), t + 0.5, t + 1.0, 540, 1130, 'slam')]
    SH.append((t + 0.5, 0.25)); t += 1.0
    plan.append(fin(t, 4.0, E, FL)); t += 4.0
    return plan, E, FL, SH, t

if __name__ == '__main__':
    which, out = sys.argv[1], sys.argv[2]
    plan, E, FL, SH, total = {'longue': longue, 'courte': courte}[which]()
    json.dump({'total': total, 'cuts': [sum(p['dur'] for p in plan[:i]) for i in range(len(plan))], 'flashes': FL, 'shakes': [s for s, _ in SH]},
              open(out + '.json', 'w'))
    render(plan, E, FL, SH, out, total)
