# Projet : Double Pendule & Chaos Numérique

**Auteur :** Simon Gaulon BUT1 - B1
**Module :** R1.07

## 1. Description du projet
Ce projet modélise la cinématique d'un pendule double pour explorer concrètement les notions d'intégration numérique et les limites du calcul flottant. Plutôt que de simplement tracer une courbe, l'objectif est de montrer comment les mathématiques peuvent faire "exploser" une simulation physique si l'on ne choisit pas la bonne méthode, et de visualiser la notion de chaos.

## 2. Installation et Lancement
Le projet utilise uniquement les bibliothèques standard vues en TP.
* **Prérequis :** `matplotlib`
* **Lancement :** 
  ```bash
  python main.py
  ```
Le script propose un menu interactif dans le terminal permettant de lancer trois expériences visuelles distinctes.

## 3. Ce qu'il faut observer

### Expérience 1 : Le crash d'Euler contre la stabilité de RK4
Le système compare deux méthodes pour calculer la trajectoire : Euler explicite (ordre 1) et Runge-Kutta (RK4, ordre 4). 
* **Observation :** Avec Euler, l'énergie du système augmente toute seule au fil du temps, jusqu'à faire exploser les valeurs.
* **Interprétation :**
  
* La méthode d'Euler revient à regarder la route juste devant son capot, braquer le volant dans cette direction, puis fermer les yeux pendant deux secondes en bloquant ses mains. À chaque virage, la voiture va tirer tout droit avant la prochaine correction et finir inévitablement par dériver vers le fossé (l'erreur s'accumule et l'énergie du système explose).

* RK4 agit comme un pilote expérimenté qui regarde loin devant. Pour prendre sa courbe, il analyse la direction à l'entrée du virage, l'évalue deux fois au point de corde (le milieu), et anticipe la sortie. Il combine ces quatre points d'observation pour donner un coup de volant parfaitement lissé. La voiture épouse la trajectoire idéale sans jamais déraper (l'énergie est strictement conservée et le système reste stable).

### Expérience 2 : La sensibilité aux conditions initiales (Le Chaos)
Deux pendules sont lâchés au même instant. Le premier à 90°, le second à 90.00001°.
* **Observation :** Pendant les premières secondes, les deux trajectoires se superposent parfaitement (une seule courbe est visible). Puis, soudainement, le micro-décalage explose et les deux pendules partent dans des directions totalement opposées.
* **Interprétation :** C'est exactement le comportement d'un moteur physique dans un jeu vidéo (comme sur Roblox Studio). Si l'on fait spawner deux objets avec une collision quasi-identique mais un très léger décalage d'inclinaison de $10^{-5}$, les boîtes de collision s'emballent et les objets sont éjectés de manière imprévisible. C'est la signature même d'un système chaotique.

### Expérience 3 : La limite des flottants
Même avec la méthode RK4, la simulation finit par dériver très légèrement si on la laisse tourner assez longtemps. On pourrait penser qu'il suffit de réduire le pas de temps `dt` à une valeur minuscule pour régler le problème. En réalité, si le pas est trop petit, le programme doit faire des millions d'additions supplémentaires. À cause de la précision limitée à 15 décimales des `float64` en Python, les micro-erreurs d'arrondi s'accumulent (usure numérique) et finissent par fausser la physique globale.

## Usage de l'IA
Conformément aux consignes de l'évaluation, je précise avoir utilisé un assistant IA (Gemini). Je m'en suis servi pour traduire les équations physiques complexes du pendule en code Python (les schémas RK4) et pour m'aider à rédiger tout les commentaires de code / Readme. J'ai vérifié et exécuté personnellement l'ensemble des scripts de rendu `matplotlib` et analysé les résultats obtenus.
