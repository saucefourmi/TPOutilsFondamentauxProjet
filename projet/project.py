import math
import matplotlib.pyplot as plt

# ==========================================
# 1. CALCUL NUMÉRIQUE ET FLOTTANTS
# ==========================================
def is_close(a, b, epsilon=1e-9):
    """Vérifie l'égalité de deux flottants avec une tolérance epsilon."""
    return abs(a - b) <= epsilon

# ==========================================
# 2. ARITHMÉTIQUE
# ==========================================
def direction_simplifiee(dx, dy):
    """
    Simplifie un vecteur de direction sur une grille entière en utilisant le PGCD.
    """
    pgcd = math.gcd(abs(int(dx)), abs(int(dy)))
    if pgcd == 0:
        return 0, 0
    return int(dx)//pgcd, int(dy)//pgcd

# ==========================================
# 3. GÉOMÉTRIE DU PLAN
# ==========================================
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, autre_point):
        """Distance euclidienne entre deux points."""
        return math.sqrt((self.x - autre_point.x)**2 + (self.y - autre_point.y)**2)

class ObstacleCirculaire:
    def __init__(self, centre, rayon):
        self.centre = centre
        self.rayon = rayon
        
    def contient_point(self, p):
        """Vérifie si un point est à l'intérieur de l'obstacle (collision)."""
        dist = p.distance(self.centre)
        if dist < self.rayon or is_close(dist, self.rayon):
            return True
        return False

# ==========================================
# 4. MATRICES ET SYSTÈMES LINÉAIRES (Sans Numpy)
# ==========================================
def resoudre_systeme_lineaire(A, B):
    """
    Résout le système linéaire A*X = B via la méthode du pivot de Gauss.
    """
    n = len(B)
    # Création de la matrice augmentée [A | B]
    M = [ligne[:] + [B[i]] for i, ligne in enumerate(A)]
    
    for i in range(n):
        # Recherche du pivot maximum pour la stabilité numérique
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        
        pivot = M[i][i]
        if is_close(pivot, 0.0):
            raise ValueError("Le système n'a pas de solution unique (Matrice singulière).")
        
        # Normalisation de la ligne du pivot
        for j in range(i, n + 1):
            M[i][j] /= pivot
            
        # Élimination des autres lignes
        for k in range(n):
            if k != i:
                facteur = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= facteur * M[i][j]
                    
    # Extraction du vecteur solution X
    return [M[i][n] for i in range(n)]

def trouver_polynome_trajectoire(points):
    """
    Trouve les coefficients du polynôme passant par 4 points 
    en résolvant un système linéaire de Vandermonde.
    """
    A = []
    B = []
    for p in points:
        x, y = p.x, p.y
        # Ligne de la matrice de Vandermonde : [x^3, x^2, x^1, x^0]
        A.append([x**3, x**2, x, 1])
        B.append(y)
        
    return resoudre_systeme_lineaire(A, B)

# ==========================================
# 5. POLYNÔMES ET RECHERCHE DE RACINES
# ==========================================
def evaluer_polynome(coeffs, x):
    """Évalue le polynôme (méthode de Horner pour la stabilité numérique)."""
    resultat = 0
    for c in coeffs:
        resultat = resultat * x + c
    return resultat

def chercher_intersection_frontiere(coeffs, y_frontiere, a, b, tol=1e-6, max_iter=100):
    """
    Recherche de l'abscisse de franchissement par dichotomie.
    """
    def f(x):
        return evaluer_polynome(coeffs, x) - y_frontiere

    if f(a) * f(b) > 0:
        return None # Pas de racine garantie

    for _ in range(max_iter):
        m = (a + b) / 2.0
        if is_close(f(m), 0.0, tol) or (b - a) / 2.0 < tol:
            return m
        
        if f(m) * f(a) < 0:
            b = m
        else:
            a = m
            
    return (a + b) / 2.0

# ==========================================
# EXÉCUTION DU PROJET ET VISUALISATION
# ==========================================
if __name__ == "__main__":
    print("=== DÉBUT DE LA SIMULATION DU DRONE ===")

    # 1. Arithmétique
    dx_initial, dy_initial = 100, 25
    dir_x, dir_y = direction_simplifiee(dx_initial, dy_initial)
    print(f"Vecteur direction initial (100, 25) simplifié par PGCD : ({dir_x}, {dir_y})")

    # 2. Matrices (Pivot de Gauss)
    points_controle = [Point(0, 1), Point(1, 3), Point(2, 2), Point(3, 4)]
    coeffs_traj = trouver_polynome_trajectoire(points_controle)
    print(f"\nCoefficients du polynôme de trajectoire (ax^3 + bx^2 + cx + d):")
    print(f"a={coeffs_traj[0]:.2f}, b={coeffs_traj[1]:.2f}, c={coeffs_traj[2]:.2f}, d={coeffs_traj[3]:.2f}")

    # 3. Flottants et Géométrie
    centre_obs = Point(1.5, 2.5)
    rayon_obs = 0.8
    obstacle = ObstacleCirculaire(centre=centre_obs, rayon=rayon_obs)
    
    # 4. Recherche de racines
    y_cible = 3.5
    x_inter = chercher_intersection_frontiere(coeffs_traj, y_cible, a=2.0, b=3.0)
    
    if x_inter:
        print(f"\nRecherche de racine (Dichotomie) :")
        print(f"Le drone franchit la frontière y={y_cible} à l'abscisse x={x_inter:.4f}")
        
    print("\nGénération du graphique en cours...")

    # ==========================================
    # PARTIE VISUELLE AVEC MATPLOTLIB
    # ==========================================
    # Préparation des données pour le tracé de la courbe
    x_valeurs = []
    y_valeurs = []
    nb_points_trace = 100
    for i in range(nb_points_trace):
        x = i * (3.2 / (nb_points_trace - 1)) # Échantillonnage de x=0 à x=3.2
        x_valeurs.append(x)
        y_valeurs.append(evaluer_polynome(coeffs_traj, x))

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer la trajectoire
    ax.plot(x_valeurs, y_valeurs, label='Trajectoire du drone', color='green', linewidth=2)
    
    # Tracer les points de contrôle
    x_points = [p.x for p in points_controle]
    y_points = [p.y for p in points_controle]
    ax.scatter(x_points, y_points, color='blue', s=100, label='Points de contrôle (P0 à P3)', zorder=5)
    
    # Tracer l'obstacle
    cercle_obs = plt.Circle((centre_obs.x, centre_obs.y), rayon_obs, color='red', alpha=0.3, label='Obstacle circulaire')
    ax.add_patch(cercle_obs)
    
    # Tracer la frontière y = 3.5
    ax.axhline(y=y_cible, color='orange', linestyle='--', label=f'Frontière y={y_cible}')
    
    # Tracer le point d'intersection trouvé par dichotomie
    if x_inter:
        ax.scatter([x_inter], [y_cible], color='red', s=100, edgecolor='black', zorder=6, label=f'Intersection trouvée ({x_inter:.2f}, {y_cible})')

    # Finitions du graphique
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(0, 5)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_title('Simulation de Vol de Drone 2D - TP Mathématiques')
    ax.set_xlabel('Position X')
    ax.set_ylabel('Position Y')
    ax.legend(loc='lower right')

    # Affichage de la fenêtre (bloque le script jusqu'à fermeture)
    plt.show()