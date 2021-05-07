import numpy as np
from scipy.integrate import odeint

Dt = 60

R = 8.314  # J / mol / K
V0 = 600  # L
Vin = 0.5 * V0
Vmax = Vin + 0.4 * V0
rho = 1  # g / L
DHr = -5.6e5  # J / mol
Ea = 9200 * R  # J / mol
Cp = 4180  # J / g / K
tau = 10  # s
F0max = 1  # L/s


CA0 = 1.6  # M
CB0 = 0.45  # M
CC0 = 0  # M
CD0 = 0  # M
CBdosage = 2.4  # M
CE0 = 0  # M
k0 = 6.85e11  # L / mol / s
T0 = 298  # K
Tj0 = 298  # K
Tjset0 = 298  # K
Tmax = 150 + 273  # K
U0 = 250  # W / m**2 / K

# Définition du volume du réacteur BESOIN DE BOUTON 600 OU 5 L
A = 1.4  # m2

slider10 = 0
slider20 = 0
slider30 = 0
slider40 = 0
slider50 = 0
slider60 = 0
slider70 = 0
slider80 = 0
slider90 = 0


def model(
    t=0,
    CA=CA0,
    CB=CB0,
    CC=CC0,
    CD=CD0,
    CE=CE0,
    T=T0,
    Tj=Tj0,
    Tjset=Tjset0,
    U=U0,
    X=0,
    V=Vin,
    playerid=0,
    slider1=slider10,
    slider2=slider20,
    slider3=slider30,
    slider4=slider40,
    slider5=slider50,
    slider6=slider60,
    slider7=slider70,
    slider8=slider80,
    slider9=slider90,
):
    print(
        f"slider1 = {slider1} | slider2 = {slider2} | slider3 = {slider3} | slider4 = {slider4}\n"
        f"slider5 = {slider5} | slider6 = {slider6} | slider7 = {slider7} | slider8 = {slider8}\n"
        f"t = {t} min | V = {V} L"
    )

    F0 = float(slider1) / 100 * F0max  # L / s
    TB = float(slider2) / 100 * Tmax  # K

    # Définition des équations différentielles décrivant les profils des concentrations
    def eq(valeurs, t, F0):
        NA, NB, T, Tj = valeurs

        Vi = V + F0 * t

        if Vi >= Vmax:
            F0 = 0
            Vi = Vmax

        CA = NA / Vi
        CB = NB / Vi

        U = float(slider3) * U0 / 100 * 5.98 + 5

        k = k0 * np.exp(-Ea / R / T)

        r = k * CA * CB

        RA = -r
        RB = -2 * r

        dNA = RA * Vi
        dNB = RB * Vi + CBdosage * F0
        dT = (
            F0 * (TB - T) / Vi
            - DHr * r / rho / Cp
            - U * A * (T - Tj) / Vi / rho / Cp
        )
        dTj = (Tjset - Tj) / tau
        return [dNA, dNB, dT, dTj]

    results = odeint(
        eq, [CA * V, CB * V, T, Tj], np.linspace(0, Dt, 10), (F0,)
    )

    if np.isnan(results).any():
        raise ValueError("Le réacteur s'est emballé!")

    V = V + F0 * t

    return {
        't': t + 1,
        'CA': results[-1, 0] / V,
        'CB': results[-1, 1] / V,
        'CC': CC,
        'CD': CD,
        'CE': CE,
        'T': T,
        'Tj': Tj,
        'Tjset': Tjset,
        'U': U,
        'X': X,
        'V': V,
        'playerid': playerid,
        'slider1': slider1,
        'slider2': slider2,
        'slider3': slider3,
        'slider4': slider4,
        'slider5': slider5,
        'slider6': slider6,
        'slider7': slider7,
        'slider8': slider8,
        'slider9': slider9,
    }