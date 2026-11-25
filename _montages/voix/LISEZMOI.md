# Voix off de synthèse

Personne de l'équipe ne parle dans les vidéos : la voix off est une **voix de synthèse** générée ici, hors ligne.

| Élément | Source | Licence |
|---|---|---|
| Moteur | Piper (`pip install piper-tts`) | MIT |
| Voix `modeles/fr_FR-siwis-medium.onnx` | rhasspy/piper-voices (Hugging Face), voir `modeles/MODEL_CARD` | Modèle : MIT · données SIWIS French Speech Synthesis Database : **CC BY 4.0** (usage commercial autorisé, avec mention) |

**Mention à mettre dans la légende TikTok** (exigée par la licence CC BY 4.0) :
`Voix de synthèse : SIWIS French Speech Synthesis Database (CC BY 4.0)`

## Faire une voix off
1. Écrire le texte calé sur les plans dans `voix/AAAA-MM-sujet/script_XXs.json` : `{"lignes": [[début_en_s, "phrase"], ...]}`.
   Écrire comme ça se prononce : « Blak Fraille-dé » (Black Friday), « Zak » (ZAC), nombres en toutes lettres,
   prix « onze quarante-cinq ». Un mot mal lu peut s'écrire en phonèmes : `[[ ɑ̃dɥˈi, ]]` pour « enduit ».
2. `python3 outils/voix_off.py voix/…/script_24s.json exports/…/video_sans_musique.mp4 musique.wav exports/…/Prefixe`
   → `Prefixe_voix_sans_musique.mp4` et `Prefixe_voix_et_musique.mp4` (la musique baisse sous la voix, −14 LUFS).
3. Vérifier : chaque phrase tombe sur son plan (le programme affiche les horaires), contrôle TikTok, et si possible
   une transcription automatique (Whisper) pour s'assurer que tout est compréhensible.
