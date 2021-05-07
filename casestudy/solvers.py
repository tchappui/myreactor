import numpy as np
from scipy.integrate import odeint

Dt = 60

R = 8.314  # J / mol / K
V = 7.6  # m3
rho = 900.0  # kg/m3
k01 = 7e8  # g**0.42 / s / mol**0.42
k02 = 5e10  # g**0.48 / s / mol**0.48
DHr1 = -368.0  # J / g
DHr2 = -670.0  # J / g
U0 = 700.0  # W / m**2 / K
A = 7.4  # m**2
Ea1 = 83400.0  # J / mol
Ea2 = 113600.0  # J / mol
cp = 2000.0 * (1.0 / 1000.0)  # J / g / K
Cw = 670.0  # J / K
alpha = 12.0  # W / K
Tambiant = 293.0  # K
tau = 1500  # s

m = V * rho * (1000.0 / 1.0)  # g

CA0 = 15900.0 / m  # mol / g
CB0 = 15300.0 / m  # mol / g
CC0 = 0.0  # mol / g
CD0 = 0.0  # mol / g
CE0 = 100.0 / m  # mol / g
T0 = 298.0  # K
Tj0 = 298.0  # K
Tjset0 = 298.0  # K

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
        f"slider5 = {slider5} | slider6 = {slider6} | slider7 = {slider7} | slider8 = {slider8}"
    )

    def balances(variables, t):
        CA, CB, CC, CD, CE, T, Tj = variables  # mol / g

        r1 = (
            k01 * np.exp(-Ea1 / R / T) * CA ** 0.94 * CB ** 0.48
        )  # mol / g / s
        r2 = (
            k02 * np.exp(-Ea2 / R / T) * CC ** 0.83 * CE ** 0.65
        )  # mol / g / s

        RA = -r1  # mol / g / s
        RB = -r1  # mol / g / s
        RC = r1 - r2  # mol / g / s
        RD = r1  # mol / g / s
        RE = r2  # mol / g / s

        dCA = RA  # mol / g / s
        dCB = RB  # mol / g / s
        dCC = RC  # mol / g / s
        dCD = RD  # mol / g / s
        dCE = RE  # mol / g / s

        Qloss = alpha * (Tambiant - T)
        Qex = U * A * (Tj - T)
        Qr = m / CA0 * (r1 * (-DHr1) + r2 * (-DHr2))

        dT = (Qr + Qex + Qloss) / (m * cp + Cw)

        dTj = (Tjset - Tj) / tau

        return [dCA, dCB, dCC, dCD, dCE, dT, dTj]

    results = odeint(
        balances, [CA, CB, CC, CD, CE, T, Tj], np.linspace(0, Dt, 2)
    )

    if np.isnan(results).any():
        raise ValueError("Le réacteur s'est emballé!")

    return {
        'CA': results[-1, 0],
        'CB': results[-1, 1],
        'CC': results[-1, 2],
        'CD': results[-1, 3],
        'CE': results[-1, 4],
        'T': results[-1, 5],
        'Tj': results[-1, 6],
        'Tjset': Tjset,
        'U': U,
        'X': 1 - results[-1, 0] / CA0,
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