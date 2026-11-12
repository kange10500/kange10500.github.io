# Mettre le portfolio en ligne avec cotations à jour

Le site est publié par GitHub Pages. Toutes les heures en séance, un script récupère les clôtures sur Yahoo Finance, écrit `quotes.json`, et republie le site. Aucune clé n'est nécessaire. Si Yahoo Finance ne répond pas, le site reste publié avec les clôtures intégrées au 30 décembre 2024, et la page l'indique.

## 1. Créer le dépôt

1. Sur GitHub, clique sur « New repository ».
2. Nom : `kange10500.github.io` (le site sera alors à l'adresse https://kange10500.github.io).
3. Public, sans README ni .gitignore.

## 2. Envoyer les fichiers

Décompresse l'archive. À la racine du dépôt, il doit y avoir :

```
index.html
CV_KOUAME_Ange.pdf
MISE_EN_LIGNE.md
scripts/update_quotes.py
notes/ (les cinq PDF)
.github/workflows/pages.yml
```

Le dossier `.github` est caché sur Mac et sur Windows. Deux façons de l'envoyer :
- Sur Mac, dans le Finder, affiche les fichiers cachés avec Cmd + Maj + point, puis glisse tout le contenu du dossier dans la page « Upload files » du dépôt.
- Ou crée le fichier à la main : « Add file », « Create new file », tape `.github/workflows/pages.yml` comme nom (les barres obliques créent les dossiers), puis colle le contenu du fichier.

## 3. Activer GitHub Pages

1. Dans le dépôt : Settings, puis Pages.
2. Source : choisis « GitHub Actions ».

## 4. Lancer la première publication

1. Onglet Actions, puis « Publier le portfolio », puis « Run workflow ».
2. Attends environ deux minutes. Le site apparaît à l'adresse indiquée dans Settings, Pages.
3. Dans la page du site, le point à gauche de la phrase « Cotations Yahoo Finance mises à jour… » est vert quand le flux fonctionne, gris quand le site utilise les clôtures intégrées.

Si le point reste gris, ouvre l'onglet Actions, clique sur la dernière exécution, puis sur l'étape « Récupérer les cotations » : le message d'erreur y est détaillé. L'étape est marquée en erreur sans bloquer la publication.

## Ce que fait la mise à jour

- Fréquence : toutes les heures de 9 h à 18 h (Paris) du lundi au vendredi, à chaque modification de `index.html`, et à la demande. GitHub peut retarder les exécutions planifiées de quelques minutes.
- Données : clôtures journalières ajustées, jusqu'à la séance en cours. Les cours sont différés d'environ 15 minutes, ce ne sont pas des cotations en direct.
- Contrôles : le script refuse un historique de moins de 1 000 jours, un prix nul ou négatif, ou une dernière cotation vieille de plus de 10 jours. Dans ces cas, la page garde ses données intégrées.

## Après la mise en ligne

Mets l'adresse du site dans ton profil GitHub (Settings du profil, champ « Website »), dans la section « Site web » de LinkedIn, et dans le CV.
