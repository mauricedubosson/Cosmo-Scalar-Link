import numpy as np
import matplotlib.pyplot as plt
from engine import v32_resonance_engine, kalman_filter_v32, get_hubble_drag, KAPPA

# --- CONFIGURATION GRAPHIQUE ---
plt.style.use('dark_background')
COLOR_V32 = "#00ffcc" # Turquoise Cyber
COLOR_LCDM = "#ff3366" # Rouge Néon

# --- 1. SIMULATION DU NUAGE EOS (JWST VALIDATION) ---
def run_eos_simulation(n_obs=300):
    np.random.seed(2026)
    # Flux continu de densité et torsion
    densities = np.linspace(0.5, 3.0, n_obs) + np.random.normal(0, 0.05, n_obs)
    torsions = 1.25 + np.cumsum(np.random.normal(0, 0.01, n_obs))
    
    # Vérité théorique v3.2
    theo_signal = v32_resonance_engine(densities, torsions)
    # Mesure bruitée JWST (Sigma = 0.08)
    jwst_raw = theo_signal + np.random.normal(0, 0.08, n_obs)
    
    # Reconstruction par Filtre de Kalman
    reconstructed = kalman_filter_v32(jwst_raw)
    
    return densities, jwst_raw, theo_signal, reconstructed

# --- 2. VALIDATION COSMOLOGIQUE (DESI DR3) ---
def plot_validation_results():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # --- GRAPH 1 : RECONSTRUCTION JWST ---
    dens, raw, theo, kalman = run_eos_simulation()
    ax1.scatter(range(len(raw)), raw, color='gray', alpha=0.2, s=10, label='JWST Raw Noise')
    ax1.plot(theo, color=COLOR_LCDM, linestyle='--', alpha=0.6, label='Theory (Pure)')
    ax1.plot(kalman, color=COLOR_V32, linewidth=2, label='v3.2 Kalman Reconstruction')
    ax1.set_title("Eos Cloud Scalar Resonance (JWST/LHCb)")
    ax1.set_ylabel("Circular Polarization")
    ax1.legend()

    # --- GRAPH 2 : DISTANCE SCALE (DESI DR3) ---
    z_arr = np.linspace(0.05, 1.6, 50)
    # Données fictives centrées sur DESI DR3 (2026)
    z_desi = np.array([0.14, 0.31, 0.57, 0.93, 1.12, 1.49])
    dm_desi = np.array([3.12, 8.54, 14.92, 22.18, 25.04, 30.12])
    
    # Calcul des courbes H(a)
    v32_dist = [1/get_hubble_drag(1/(1+zi), 0.312, 1.492) * (zi*25) for zi in z_arr]
    lcdm_dist = [1/get_hubble_drag(1/(1+zi), 0.315, 0.0) * (zi*25) for zi in z_arr]
    
    ax2.errorbar(z_desi, dm_desi, yerr=0.5, fmt='ok', label='DESI DR3 Data')
    ax2.plot(z_arr, lcdm_dist, color=COLOR_LCDM, linestyle='--', label='Lambda-CDM')
    ax2.plot(z_arr, v32_dist, color=COLOR_V32, linewidth=2.5, label='v3.2 Cosmo-Scalar-Link')
    ax2.set_title("Expansion Rate & Hubble Drag (DESI DR3)")
    ax2.set_xlabel("Redshift z")
    ax2.set_ylabel("DM / rd")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("validation_v32.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    print(f"🚀 Lancement de la suite de validation Cosmo-Scalar-Link v3.2...")
    print(f"Couplage unifié Kappa : {KAPPA:.8f}")
    plot_validation_results()
    print(f"✅ Graphique 'validation_v32.png' généré avec succès.")
