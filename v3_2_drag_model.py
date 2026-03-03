# =========================================================
# Late-Time Higgs-Inflaton Drag Model v3.2 (final polish)
# =========================================================

!pip install emcee corner -q

import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
from scipy.integrate import odeint

# Données 2026
S8_DES, S8_DES_ERR = 0.789, 0.012
S8_CMB, S8_CMB_ERR = 0.836, 0.012
z_fsig8 = np.array([0.38, 0.51, 0.61, 0.98])
fs8_obs = np.array([0.497, 0.458, 0.436, 0.379])
fs8_err = np.array([0.012, 0.011, 0.013, 0.015])

def growth_deriv(y, a, gamma, d_drag, Omega_m0, Omega_L0=0.7):
    delta, delta_prime = y
    Omega_m_a = Omega_m0 * a**(-3) / (Omega_m0 * a**(-3) + Omega_L0)
    coeff = (3.0 - 1.5*Omega_m_a)/a
    drag = gamma * d_drag * (1.0 - Omega_m_a) / a
    return [delta_prime, -(coeff + drag)*delta_prime + 1.5*Omega_m_a*delta/a**2]

def compute_observables(theta):
    gamma, d_drag, Omega_m0 = theta
    a_range = np.logspace(-3, 0, 2000)
    y0 = [1e-3, 1.0]
    sol_m = odeint(growth_deriv, y0, a_range, args=(gamma, d_drag, Omega_m0))
    sol_s = odeint(growth_deriv, y0, a_range, args=(0., 0., Omega_m0))
    s8_model = S8_CMB * (sol_m[-1,0] / sol_s[-1,0])
    
    fs8_model = []
    for z in z_fsig8:
        a_z = 1/(1+z)
        idx = np.argmin(np.abs(a_range - a_z))
        a, delta, dprime = a_range[idx], sol_m[idx,0], sol_m[idx,1]
        f = a * dprime / delta
        sigma8_z = s8_model * (delta / sol_m[-1,0])
        fs8_model.append(f * sigma8_z)
    return s8_model, np.array(fs8_model)

def log_prior(theta):
    g, d, om = theta
    return 0.0 if (0< g <1 and 0.1<d<5 and 0.25<om<0.35) else -np.inf

def log_likelihood(theta):
    s8, fs8 = compute_observables(theta)
    chi2 = ((s8 - S8_DES)/S8_DES_ERR)**2 + np.sum(((fs8 - fs8_obs)/fs8_err)**2)
    return -0.5 * chi2

def log_probability(theta):
    lp = log_prior(theta)
    return lp + log_likelihood(theta) if np.isfinite(lp) else -np.inf

# === RUN ===
ndim, nwalkers = 3, 48
pos = np.array([0.35, 1.5, 0.31]) + 1e-4*np.random.randn(nwalkers, ndim)
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability)
sampler.run_mcmc(pos, 4000, progress=True)

samples = sampler.get_chain(discard=1000, thin=20, flat=True)
gamma, ddrag, om = np.median(samples, axis=0)
s8_best, fs8_best = compute_observables([gamma, ddrag, om])

chi2_model = -2 * log_likelihood([gamma, ddrag, om])
chi2_lcdm  = -2 * log_likelihood([0.,0.,0.315])

delta_chi2 = chi2_lcdm - chi2_model
aic_model = chi2_model + 2*3
aic_lcdm  = chi2_lcdm  + 2*1
bic_model = chi2_model + 3*np.log(len(z_fsig8)+1)
bic_lcdm  = chi2_lcdm  + 1*np.log(len(z_fsig8)+1)

print(f"\n=== v3.2 BEST-FIT ===")
print(f"γ = {gamma:.4f} | d_drag = {ddrag:.4f} | Ωm = {om:.4f}")
print(f"S8 = {s8_best:.4f} (DES: {S8_DES}) → tension {abs(s8_best-S8_DES)/S8_DES_ERR:.2f}σ")
print(f"Δχ² = {delta_chi2:.1f} | ΔAIC = {aic_lcdm - aic_model:.1f} | ΔBIC = {bic_lcdm - bic_model:.1f}")
print("→ Evidence forte pour le modèle" if (aic_lcdm - aic_model) > 10 else "→ Amélioration modérée")

# Plots
plt.style.use('dark_background')
corner.corner(samples, labels=[r"$\gamma$", r"$d_{\rm drag}$", r"$\Omega_m$"], show_titles=True)
plt.show()

# Growth + fσ8 côte à côte
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(14,6))
a = np.logspace(-3,0,1000)
ax1.plot(a, odeint(growth_deriv,[1e-3,1],a,args=(0,0,0.315))[:,0]/1, 'w-', label='ΛCDM')
ax1.plot(a, odeint(growth_deriv,[1e-3,1],a,args=(gamma,ddrag,om))[:,0]/1, '#00ffcc', lw=3, label='v3.2')
ax1.axvline(0.01, color='magenta', ls='--')
ax1.set_title("Growth factor D(a)"); ax1.legend()

ax2.errorbar(z_fsig8, fs8_obs, fs8_err, fmt='ok', label='DESI 2026')
ax2.plot(z_fsig8, fs8_best, '#00ffcc', marker='s', lw=3, label='Model')
ax2.set_title("fσ8(z)"); ax2.legend()
plt.tight_layout(); plt.show()
