import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# 1. PARAMÈTRES PHYSIQUES
# =====================================================================
G = 9.81  # Gravité
M1 = 1.0  # Masse 1
M2 = 1.0  # Masse 2
L1 = 1.0  # Longueur tige 1
L2 = 1.0  # Longueur tige 2

# =====================================================================
# 2. MOTEUR PHYSIQUE 
# =====================================================================
def derivees(Y):
    """Calcule l'évolution instantanée du pendule."""
    t1, w1, t2, w2 = Y
    delta = t1 - t2
    den = 2 * M1 + M2 - M2 * np.cos(2 * t1 - 2 * t2)
    
    num1 = -G * (2 * M1 + M2) * np.sin(t1) - M2 * G * np.sin(t1 - 2 * t2) \
           - 2 * np.sin(delta) * M2 * (w2**2 * L2 + w1**2 * L1 * np.cos(delta))
    a1 = num1 / (L1 * den)
    
    num2 = 2 * np.sin(delta) * (w1**2 * L1 * (M1 + M2) \
           + G * (M1 + M2) * np.cos(t1) + w2**2 * L2 * M2 * np.cos(delta))
    a2 = num2 / (L2 * den)
    
    return np.array([w1, a1, w2, a2])

def energie_mecanique(Y):
    """Calcule l'énergie totale (doit rester constante en théorie)."""
    t1, w1, t2, w2 = Y[..., 0], Y[..., 1], Y[..., 2], Y[..., 3]
    Ek = 0.5 * M1 * L1**2 * w1**2 + 0.5 * M2 * (
        L1**2 * w1**2 + L2**2 * w2**2 + 2 * L1 * L2 * w1 * w2 * np.cos(t1 - t2)
    )
    Ep = -(M1 + M2) * G * L1 * np.cos(t1) - M2 * G * L2 * np.cos(t2)
    return Ek + Ep

def positions_cartesiennes(Y):
    """Traduit les angles en coordonnées (x,y) pour dessiner sur l'écran."""
    t1, t2 = Y[..., 0], Y[..., 2]
    x1, y1 = L1 * np.sin(t1), -L1 * np.cos(t1)
    x2, y2 = x1 + L2 * np.sin(t2), y1 - L2 * np.cos(t2)
    return x1, y1, x2, y2

# =====================================================================
# 3. SCHÉMAS D'INTÉGRATION 
# =====================================================================
def resoudre_euler(Y0, dt, n_steps):
    """Méthode basique : trace tout droit (génère des bugs d'énergie)."""
    trajectoire = np.zeros((n_steps, 4))
    trajectoire[0] = Y0
    for i in range(1, n_steps):
        trajectoire[i] = trajectoire[i-1] + dt * derivees(trajectoire[i-1])
    return trajectoire

def resoudre_rk4(Y0, dt, n_steps):
    """Méthode pro : anticipe les courbes pour rester stable."""
    trajectoire = np.zeros((n_steps, 4))
    trajectoire[0] = Y0
    for i in range(1, n_steps):
        Y = trajectoire[i-1]
        k1 = derivees(Y)
        k2 = derivees(Y + dt/2 * k1)
        k3 = derivees(Y + dt/2 * k2)
        k4 = derivees(Y + dt * k3)
        trajectoire[i] = Y + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)
    return trajectoire

# =====================================================================
# 4. EXPÉRIENCES
# =====================================================================
def experience_A_energie():
    """Montre pourquoi la méthode d'Euler explose (Dérive numérique)."""
    dt = 0.01
    n_steps = 1000  # 10 secondes
    temps = [i * dt for i in range(n_steps)]
    Y0 = np.array([np.pi/2, 0.0, np.pi/2, 0.0]) # Lâché à 90°
    
    traj_euler = resoudre_euler(Y0, dt, n_steps)
    traj_rk4 = resoudre_rk4(Y0, dt, n_steps)
    
    E0 = energie_mecanique(Y0)
    
    plt.figure(figsize=(8, 5))
    plt.plot(temps, energie_mecanique(traj_euler) - E0, label="Euler")
    plt.plot(temps, energie_mecanique(traj_rk4) - E0, label="RK4")
    plt.axhline(0, color='black', linestyle='--')
    plt.title("Dérive de l'énergie : Euler vs RK4")
    plt.xlabel("Temps (s)")
    plt.ylabel("Erreur d'énergie (Joules)")
    plt.legend()
    plt.show()

def experience_B_chaos_roblox():
    """Le 'Glitch Roblox' : 0.0001° de différence au départ."""
    dt = 0.01
    n_steps = 1500 # 15 secondes
    
    Y0_normal = np.array([np.pi/2, 0.0, np.pi/2, 0.0])
    Y0_glitch = np.array([np.pi/2 + 0.0001, 0.0, np.pi/2, 0.0])
    
    traj_normal = resoudre_rk4(Y0_normal, dt, n_steps)
    traj_glitch = resoudre_rk4(Y0_glitch, dt, n_steps)
    
    _, _, x2_n, y2_n = positions_cartesiennes(traj_normal)
    _, _, x2_g, y2_g = positions_cartesiennes(traj_glitch)
    
    plt.figure(figsize=(8, 8))
    plt.plot(x2_n, y2_n, label='Pendule Normal', color='blue', alpha=0.7)
    plt.plot(x2_g, y2_g, label='+0.0001° au départ', color='red', alpha=0.7)
    plt.scatter([0], [0], color='black', marker='x') # Origine
    plt.title("L'effet papillon : Deux trajectoires qui divergent brusquement")
    plt.axis("equal")
    plt.legend()
    plt.show()

def experience_C_interactive():
    """Permet de tester ses propres angles."""
    try:
        t1 = float(input("Angle de départ masse 1 (degrés) : "))
        t2 = float(input("Angle de départ masse 2 (degrés) : "))
    except ValueError:
        print("Saisie invalide, on utilise 90° et 180°.")
        t1, t2 = 90.0, 180.0
        
    Y0 = np.array([np.radians(t1), 0.0, np.radians(t2), 0.0])
    traj = resoudre_rk4(Y0, 0.01, 1000)
    x1, y1, x2, y2 = positions_cartesiennes(traj)
    
    plt.figure(figsize=(8, 8))
    plt.plot(x1, y1, label='Trajectoire Masse 1', alpha=0.5)
    plt.plot(x2, y2, label='Trajectoire Masse 2', linewidth=1)
    plt.scatter([0], [0], color='black', marker='x')
    plt.title(f"Simulation ({t1}°, {t2}°) sur 10 secondes")
    plt.axis("equal")
    plt.legend()
    plt.show()

# =====================================================================
# 5. MENU PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    while True:
        print("\n=== PROJET : DOUBLE PENDULE & CHAOS ===")
        print("1. Analyser le bug d'énergie d'Euler (Euler vs RK4)")
        print("2. L'effet Roblox : Sensibilité aux conditions initiales (Chaos)")
        print("3. Tester des angles personnalisés")
        print("4. Quitter")
        
        choix = input("Votre choix : ")
        if choix == '1': experience_A_energie()
        elif choix == '2': experience_B_chaos_roblox()
        elif choix == '3': experience_C_interactive()
        elif choix == '4': break
        else: print("Choix invalide.")
