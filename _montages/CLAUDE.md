# Montages vidéo TikTok : Brico Cash Fameck

Dossier des pubs vidéo du magasin : rushs bruts → montage → vidéos finies prêtes à publier.
Il est rangé dans le dépôt du site d'outils ; le « _ » du nom de dossier le tient **hors du site publié** (GitHub Pages ignore les dossiers en « _ »).
**Tous les chemins ci-dessous partent de `_montages/`** ; lancer les commandes depuis ce dossier (`cd _montages`).
Interface, textes et explications **en français**, ton simple. Sur TikTok on tutoie (« Viens nous voir ! »).

## Le magasin
- **Brico Cash Fameck**, ZAC de la Feltière, avenue François-Mitterrand, 57290 Fameck.
- **Horaires** : du lundi au samedi, 7 h – 19 h (fermé le dimanche). Vérifier les jours fériés et horaires spéciaux avant chaque vidéo.
- **Slogan** : « + de stock, + de prix bas ». **Ton** : « on se parle cash », phrases courtes, une pointe d'humour.

## Dossiers
| Dossier | Contenu |
|---|---|
| `rushs/` | Photos et vidéos brutes, un sous-dossier par projet : `rushs/AAAA-MM-sujet/` (ex. `rushs/2026-11-black-friday/`). **Ne jamais modifier ni écraser un rush.** |
| `musiques/` | Sons **libres de droits pour un usage commercial** uniquement. Chaque fichier est listé dans `musiques/LISEZMOI.md` avec sa source et sa licence. |
| `logo/` | Logo du magasin (`brico-cash-fameck.jpg`, fond blanc). Ne jamais le modifier (couleurs, proportions, typo) : le poser sur une carte blanche ou un fond lisible. |
| `exports/` | Vidéos finies : `exports/AAAA-MM-sujet/BricoCash_Fameck_<Sujet>_<durée>s_<avec\|sans>_musique.mp4` |
| `polices/` | Polices de la charte : Bebas Neue (titres, substitut de Dreamwalker) et Barlow Condensed (textes, substitut de DIN Next). Licence OFL. |
| `outils/` | Moteur de montage « motion design » (textes animés, étiquettes prix, carton de fin) et générateur de musique maison. |
| `../.claude/skills/ffmpeg-skill/` | Skill de montage local (kajisho5/ffmpeg-skill 4.7.1, MIT, relu : aucun envoi réseau). Voir `PROVENANCE.txt`. |

## Règles de montage (obligatoires)
1. **Format TikTok** : vertical 9:16, **1080 × 1920**, **MP4 H.264** (High, yuv420p, 30 images/s), son AAC 48 kHz.
   Toujours une version de **20 à 30 s** et, si demandé, une courte de **10 à 15 s**.
2. **Les 2 premières secondes accrochent** : le plus beau produit ou l'offre, texte choc (« −50 % », prix, question cash), petit zoom/flash.
3. **Plans courts et rythmés** : 0,5 à 2 s par plan, **coupes sur les temps de la musique** (120 BPM = une coupe toutes les 0,5 s ou 1 s).
   Couper les passages flous, mal cadrés, trop bougés ou inutiles ; ne jamais faire chevaucher un plan sur une coupe du rush (repérer les coupes avec `scenes.py` ou `select='gt(scene,0.12)'`). Zooms doux (1,0 → 1,1) sur les produits.
4. **Textes gros, lisibles et au centre** : contour noir épais ou fond plein (pastille), police Bebas Neue.
   **Zone sûre** : x entre 120 et 940 px, y entre 250 et 1450 px. **Jamais en bas (y > 1500) ni à droite (x > 940)** : les boutons et la légende TikTok les cachent.
   Orthographe française soignée : accents en capitales (É, À), espace insécable avant « ! » et « % », prix au format `11,45 €`.
5. **Toujours finir** (3 à 5 s) par : logo ou nom du magasin, **adresse**, **horaires** et un **appel à l'action** (« Viens nous voir ! »).
6. **Musique** : uniquement **libre de droits pour un usage commercial** (source et licence notées dans `musiques/LISEZMOI.md`), volume −14 LUFS.
   **Toujours livrer aussi une version sans musique** (l'équipe ajoute la musique dans TikTok, bibliothèque commerciale pour un compte pro).
7. **Améliorer l'image** : luminosité, contraste et saturation (`eq`), netteté (`unsharp`), sans exagérer ; plans de nuit sans écraser les noirs.

## Dépôt public : faire attention
Le dépôt est **public** (obligatoire pour le site gratuit) : tout le monde peut voir et télécharger ce qui y est mis, mais personne ne peut le modifier sans invitation.
- N'y mettre que ce qui pourrait passer sur TikTok : pas de documents internes, d'export Excel, de prix d'achat, de marges, de stock chiffré, de plannings, de visages de clients, de numéros de téléphone ou d'adresses e-mail.
- Couper ou flouter au montage tout ce qui est sensible dans un rush (écran de caisse, document sur un bureau, plaque d'immatriculation, client reconnaissable).
- Dans le doute, ne pas déposer et demander d'abord.

## Autres règles
- **Prix et promos** : recopier exactement ce qui est écrit sur les affiches/étiquettes filmées (prix, %, dates, « dans la limite des stocks »). N'inventer aucune offre, aucun chiffre.
- **Confidentialité** : jamais de prix d'achat, de marge ni de stock chiffré dans une vidéo.
- **Personnes** : pas de client reconnaissable sans son accord ; l'équipe seulement si elle est d'accord.
- **Charte** : jaune `#fab61f`, bleu `#0078bf`, noir, blanc, gris `#575656`. Black Friday = noir et jaune ; rouge `#e30513` réservé aux Arrivages.
- Rushs reçus en petite définition (envoi depuis la Photothèque iPhone) : le signaler et conseiller l'envoi depuis l'app **Fichiers**.
- S'il manque des images, dire exactement quoi filmer : plan, durée (5 à 8 s), angle, téléphone **vertical**, **1080p 30 i/s**.

## Comment monter
- **Opérations simples** (couper, recadrer en 9:16, logo, titre, musique, volume, export, contrôle) : skill `ffmpeg-skill`
  (`python3 ../.claude/skills/ffmpeg-skill/scripts/<outil>.py …`, voir son `SKILL.md`).
- **Pub promo avec textes animés et étiquettes prix** : copier `outils/black_friday_2026.py` en `outils/<projet>.py`,
  changer les plans (`seg(fichier, début, durée, zoom…)`) et les textes, puis
  `python3 outils/<projet>.py longue exports/<projet>/longue.mp4` (moteur : `outils/montage.py`).
- **Musique maison libre de droits** (120 BPM) : `python3 outils/musique.py DUREE DEBUT_CARTON_FIN sortie.wav`.

## Vérifier la vidéo finale AVANT de la donner
1. `python3 ../.claude/skills/ffmpeg-skill/scripts/check.py FICHIER.mp4 --platform tiktok` : tout doit passer (1080 × 1920, H.264, 30 i/s).
2. `ffprobe` : durée dans la fourchette demandée ; décodage complet sans erreur (`ffmpeg -v error -i FICHIER.mp4 -f null -`).
3. **Regarder les images** : planche de 8 à 10 images clés (`look.py FICHIER.mp4 --tiles 3x3`, ou extraction aux moments où chaque texte est entier),
   avec la zone interdite dessinée : aucun texte coupé, caché ou hors zone sûre ; pas de plan flou ou d'une autre prise.
4. Relire chaque texte : orthographe, accents, prix identiques aux affiches.
5. Version avec musique : environ −14 LUFS (`ebur128`), pas de saturation.

## Livrer
- Mettre les vidéos dans `exports/AAAA-MM-sujet/`, faire un commit et pousser la branche de travail (jamais directement sur `main` sans accord : `main` publie le site) ; envoyer aussi les fichiers dans la conversation.
- Proposer 3 idées de légende avec hashtags locaux (#Fameck #Thionville #Moselle #Lorraine #ValDeFensch #Hayange #Florange #Uckange…).
- GitHub refuse les fichiers de plus de 100 Mo (25 Mo par l'envoi du navigateur) : découper ou réduire les rushs trop lourds.
