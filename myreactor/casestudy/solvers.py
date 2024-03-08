import numpy as np
from scipy.integrate import odeint

Dt = 60

R = 8.314  # J / mol / K
Vmax = 5.0 # m3
V0 = 7.6  # m3
rho = 900.0  # kg/m3
k01 = 7e8  # g**0.42 / s / mol**0.42
k02 = 4e10  # g**0.48 / s / mol**0.48
DHr1 = -106000.0  # J / mol
DHr2 = -168000.0  # J / mol
U0 = 700.0  # W / m**2 / K
A = 7.4  # m**2
Ea1 = 83400.0  # J / mol
Ea2 = 123600.0  # J / mol
cp = 2000.0 * (1.0 / 1000.0)  # J / g / K
Cw = 670.0  # J / K
alpha = 12.0  # W / K
Tambiant = 293.0  # K
tau = 1500  # s

m0 = V0 * rho * (1000.0 / 1.0)  # g
mmax = Vmax * rho * (1000.0 / 1.0)  # g

NAF = 15900.0 # mol
mF = mmax - m0 # g
CAF = NAF / mF  # mol / g
CA0 = 0  # mol / g
NB0 = 15300.0 # mol
CB0 = NB0 / m0  # mol / g
CC0 = 0.0  # mol / g
CD0 = 0.0  # mol / g
CE0 = 100.0 / m0  # mol / g
T0 = 298.0  # K
Tj0 = 298.0  # K
Tjset0 = 298.0  # K

mdot0 = 1 # g / s
Vdot0 = mdot0 / 1000. / rho # m3 / s
Dmdot = 0.01 # g / s


def morton(
    CA=CA0,
    CB=CB0,
    CC=CC0,
    CD=CD0,
    CE=CE0,
    m=m0,
    T=T0,
    Tj=Tj0,
    Tjset=Tjset0,
    U=U0,
    X=0,
    mdot=mdot0,
    Vdot=Vdot0,
    Dmdot=Dmdot,
    playerid=0,
):

    def balances(variables, t):
        CA, CB, CC, CD, CE, T, Tj, m = variables  # mol / g

        r1 = k01 * np.exp(-Ea1 / R / T) * CA**0.94 * CB**0.48  # mol / g / s
        r2 = k02 * np.exp(-Ea2 / R / T) * CC**0.83 * CE**0.65  # mol / g / s

        RA = -r1  # mol / g / s
        RB = -r1  # mol / g / s
        RC = r1 - r2  # mol / g / s
        RD = r1  # mol / g / s
        RE = r2  # mol / g / s

        dm = mdot
        dCA = RA + mdot * CAF / m  # mol / g / s
        dCB = RB  # mol / g / s
        dCC = RC  # mol / g / s
        dCD = RD  # mol / g / s
        dCE = RE  # mol / g / s

        Qloss = alpha * (Tambiant - T)
        Qex = U * A * (Tj - T)
        Qr = m * (r1 * (-DHr1) + r2 * (-DHr2))
        Qfeed = 0

        dT = (Qr + Qex + Qloss + Qfeed) / (m * cp + Cw)

        dTj = (Tjset - Tj) / tau

        return dCA, dCB, dCC, dCD, dCE, dT, dTj, dm

    results = odeint(
        balances, [CA, CB, CC, CD, CE, T, Tj, m], np.linspace(0, Dt, 2)
    )

    if np.isnan(results).any():
        raise ValueError("Le réacteur s'est emballé!")
    
    CA, CB, CC, CD, CE, T, Tj, m = results.T

    return {
        "CA": CA,
        "CB": CB,
        "CC": CC,
        "CD": CD,
        "CE": CE,
        "m": m,
        "T": T,
        "Tj": Tj,
        "Tjset": Tjset,
        "U": U,
        "X": 1 - CB * m / NB0,
        "mdot": mdot,
        "Vdot": Vdot,
        "Dmdot": Dmdot,
        "playerid": playerid,
    }
