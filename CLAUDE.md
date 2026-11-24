# Outils du magasin Brico Cash Fameck

Site statique publié par GitHub Pages : https://kyllox57300-web.github.io/reglages-t7200/
Chaque outil est **un seul fichier `index.html` autonome** (logo, polices de secours et bibliothèques intégrés),
pour pouvoir aussi être copié sur le serveur du magasin et marcher sans Internet.

| Dossier | Outil |
|---|---|
| `/` | Page d'accueil, outils rangés par usage |
| `affiches/` | Affiches grand format (export Excel ou à la main, remise %, tête de gondole, PDF A4 → A0) |
| `panneaux/` | Panneaux magasin (modèles + « Mes modèles » mémorisés sur le PC ; A4, A3, A0, bandeau de rack 280 × 100) |
| `etiquettes/` | Étiquettes de bacs bleues (pictogramme Lucide ou photo, logo, planches A4) |
| `photos/` | Photos Facebook (habillage d'une photo de rayon, partage téléphone / enregistrement PC) |
| `qr/` | Feuilles QR à poser en rayon (mémorisées, réimpression, date d'impression) |
| `calcul/` | Calculateurs clients (calcul simple au m², lino, peinture, BA13, béton…) |
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
- **Affiche Arrivages 80 × 120** : marge bleue, étiquette « ARRIVAGES » rouge inclinée, visuel, pavé prix, libellé, date, logo en bas à droite.
- **Facebook (gabarit obligatoire)** : 3 bandes jaunes en haut à gauche sur fond blanc, **logo en bas et centré**.
  → L'outil `photos/` ne suit pas encore ce gabarit (logo en haut à gauche) : à adapter quand demandé.

## Styles d'affiches (outil `affiches/`, choix « Couleurs »)
- Automatique : **orange** pour le bandeau ARRIVAGE, **noir et jaune** pour BLACK FRIDAY, bleu et jaune sinon.
- « Arrivages de la charte » : modèle bleu et rouge d'après l'affiche 80 × 120.

## T7200
Réglages validés : bâche intissée 1000 mm = Enhanced Matte Paper ; adhésif Folex SIVC 914 mm = Premium Glossy Photo Paper ;
taille A0, « Ajuster à la largeur » décoché, impression des PDF en « Taille réelle » depuis Acrobat.
Bandeau de rack 280 × 100 : bâche 1000 mm, taille définie par l'utilisateur 1000 × 2800 mm, « Taille réelle ».
