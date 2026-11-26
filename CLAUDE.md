# Outils du magasin Brico Cash Fameck

Site statique publié par GitHub Pages : https://kyllox57300-web.github.io/reglages-t7200/
Chaque outil est **un seul fichier `index.html` autonome** (logo, polices de secours et bibliothèques intégrés),
pour pouvoir aussi être copié sur le serveur du magasin et marcher sans Internet.

| Dossier | Outil |
|---|---|
| `/` | Page d'accueil, outils rangés par usage |
| `affiches/` | Affiches grand format (export Excel ou à la main, remise %, tête de gondole, PDF A4 → A0) |
| `panneaux/` | Panneaux magasin (modèles + « Mes modèles » mémorisés sur le PC ; A4, A3, A0, bandeau de rack 280 × 100) |
| `etiquettes/` | Étiquettes de bacs bleues (pictogramme Lucide ou photo, logo en haut à droite ou au milieu, taille d'écriture au choix, bouton Dupliquer, flèche ⬆ ⬇ facultative par étiquette (bande jaune à gauche, flèche bleue), planches A4 ; bandeau 287 × 60 mm en A4 paysage) |
| `photos/` | Photos Facebook (habillage d'une photo de rayon, partage téléphone / enregistrement PC) |
| `qr/` | Feuilles QR à poser en rayon (mémorisées avec leur date d'impression dans la liste, pas sur la feuille ; réimpression ; toujours imprimées sur A4 : A5 = 2 par feuille, A6 = 4) |
| `calcul/` | Calculateurs clients (calcul simple au m², lino — rouleaux de 1 à 4 m, choisis par le client ou conseillés, un seul QR —, peinture, BA13, béton…) |
| `sav/` | Photos SAV : le téléphone envoie les photos d'un n° de dossier, le PC les reçoit, les enregistre puis les supprime (Firebase du propriétaire, projet `depenses-noel` partagé avec l'appli « dépenses de Noël » : Firestore + code secret du magasin) |
| `t7200/` | Réglages Epson SureColor T7200 (`bache.ssf`, `adhesif.ssf`) |

L'outil **Affiches prix cuisine** n'est **pas** ici : il reste sur le serveur du magasin, que l'équipe met à jour.

## Règles à respecter
- **Confidentialité** : ne jamais lire ni afficher le **prix d'achat (PA)**, les **marges** ni le **stock**.
  Les outils lisent l'export Excel **dans le navigateur** (colonnes LIBELLE, P VENTE, ITM 8, EAN, ECO-PART, ACTIF) ; rien n'est envoyé.
- Interface et textes **en français**, ton simple ; tutoiement pour l'équipe, vouvoiement pour les clients (calculateurs).
- Vérifier chaque changement : rendu à l'écran **et** PDF (la capture html2canvas ne dessine pas les dégradés répétés : utiliser une image SVG).

## Charte graphique Brico Cash (communication externe, version du 23/01/24)
- **Couleurs** : jaune `#fab61f` (RVB 250-183-33), bleu RVB 0-120-191 (`#0078bf`), blanc, noir pour les textes,
  gris `#575656` (bas de page, bandeaux stockage), **rouge Arrivages `#e30513`** (prix blanc sur rouge).
  Fond OSB possible, toujours avec les couleurs principales.
- **Logo** : fichier fourni, jamais modifié (couleurs, proportions, typo). Sur fond bleu, blanc ou photo lisible.
- **Typographies** : Dreamwalker / Regular pour les accroches (opérations commerciales : Regular tout en capitales),
  DIN Next LT Pro pour les textes. Polices payantes : substitut en ligne **Bebas Neue** (titres).
- **Ton** : « on se parle cash » — phrases courtes, directes, une pointe d'humour.
- **Bloc prix** : courant = blanc sur bleu ; Arrivages = blanc sur rouge, « STOCK LIMITÉ ! » sur gris, garanties en noir sur orange.
- **Facebook (gabarit obligatoire)** : 3 bandes jaunes en haut à gauche sur fond blanc, **logo en bas et centré**.
  → L'outil `photos/` ne suit pas encore ce gabarit (logo en haut à gauche) : à adapter quand demandé.

## Affiches grand format (outil `affiches/`) : 4 modèles validés par le patron
4 opérations, **la couleur est imposée par l'opération** :
- **Black Friday** : noir et jaune ;
- **Soldes** : bleu et jaune ;
- **Promo** : orange ;
- **Déstockage** : bleu et jaune.
- **Prix rayon** (affiche de prix normal en rayon) : bleu et jaune, pas de bandeau (simple trait jaune sous le logo), toujours sans remise.
Plus un modèle libre **« Autre texte »** : le seul où l'équipe choisit le texte du bandeau (vide = sans bandeau)
et les couleurs (bleu et jaune, noir et jaune, orange). À garder.
Les autres bandeaux (Arrivage, Prix choc…) et le modèle « Arrivages de la charte » ont été retirés : ne pas les remettre sans demande.

## Photos SAV (`sav/`)
- **Uniquement des photos du produit et un n° de dossier** : jamais de nom, téléphone, adresse ni note libre (demande explicite).
- Pas de compte : un **code secret du magasin** `SAV-` + 12 caractères, créé sur le PC du SAV et mémorisé sur chaque appareil
  (les téléphones le reçoivent en scannant le QR « Relier un téléphone », via `#c=` dans l'adresse). Le code n'est jamais dans le dépôt.
- Données : `sav/{code}/dossiers/{id}` (`dossier`, `count`, `ready`, `saved`, `created`) et `…/photos/{n}` (`n`, `data` en base64, < 1 Mo).
  Règles à publier dans la console : `sav/firestore.rules` (garde aussi les règles de l'appli Noël, même projet).
- Photos réduites (≈ 1600 px, < 900 Ko) : pas de Cloud Storage (payant). Le `firebaseConfig` (non secret) est intégré au build.

## T7200
Réglages validés : bâche intissée 1000 mm = Enhanced Matte Paper ; adhésif Folex SIVC 914 mm = Premium Glossy Photo Paper ;
taille A0, « Ajuster à la largeur » décoché, impression des PDF en « Taille réelle » depuis Acrobat.
Bandeau de rack 280 × 100 (économie d'encre cochée d'office : fond blanc) : bâche 1000 mm, taille définie par l'utilisateur 1000 × 2800 mm, « Taille réelle ».
