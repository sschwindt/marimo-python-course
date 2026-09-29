import marimo

__generated_with = "0.25.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Freibord und Eintauchtiefe

    Parameterdefinitionen:
    """)
    return


@app.cell
def _():
    rho_k =  870. # kg / m3 - Holzdicht
    rho_f = 1000. # kg / m3 - Wasserdichte
    g = 9.81      # N / kg - Erdbeschleunigung
    b_x = 1.5     # m - Kastenbreite
    b_y = 2.0     # m - Kastenlänge
    h = 1.5       # m - Kastenhöhe
    w = 0.01      # m - Wandstärke
    return b_x, b_y, g, h, rho_f, rho_k, w


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Berechnung der Gewichtskraft $ F_g = \rho_k \cdot g \cdot V_k = \rho_k \cdot g \cdot \left[b_x \cdot b_y \cdot h - \left(h - w\right) \cdot  \left(b_x - 2 w\right) \cdot \left(b_y - 2 w\right)\right] $ :
    """)
    return


@app.cell
def _(b_x, b_y, g, h, rho_k, w):
    V_k = b_x * b_y * h - (b_x - 2 * w) * (b_y - 2 * w) * (h - w)
    F_g = V_k * rho_k * g
    print(f'Koerpervolumen V_k = {V_k:.2f} m3\nGewichtskraft: {F_g:.2f} N')
    return F_g, V_k


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Berechnung des Verdrängungsvolumens $ V_v = F_g / \left(\rho_f \cdot g \right) $ :
    """)
    return


@app.cell
def _(F_g, g, rho_f):
    V_v = F_g / (rho_f * g)
    print(f'Verdraengungsvolumen: {V_v:.2f} m3')
    return (V_v,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Berechnung der Eintauchtiefe $ d = V_v / \left(b_x \cdot b_y\right) $ und des Freibords $ f = h - d $ :
    """)
    return


@app.cell
def _(V_v, b_x, b_y, h):
    d = V_v / b_x * b_y
    f = h - d
    print(f'Eintauchtiefe d = {d:.2f} m\nFreibord f = {f:.2f} m')
    if f >= 0:
        print("Schwimmender Körper")
    if f < 0:
        print("Der Körper geht unter.")
    return (d,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Schwimmstabilität
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Flächenträgheitsmoment

    Berechnung des Flächenträgheitsmoments $I_0 = \frac{b_{\text{x}} ^3 \cdot b_{\text{y}} }{12}$ bezüglich 0:
    """)
    return


@app.cell
def _(b_x, b_y):
    I_0 = b_x**3 * b_y / 12
    print(f'Flaechentraegheitsmoment I_0 = {I_0:.2f} m4')
    return (I_0,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Höhenlagen

    Höhe $h_g$ des Gewichtsschwerpunkts:
    """)
    return


@app.cell
def _(V_k, b_x, b_y, h, w):
    V_k_lat_waende = 2 * (b_y - 2 * w) * (h - w) * w 
    V_k_front_back = 2 * b_x * (h - w) * w
    V_k_boden = b_x * b_y * w
    h_g = ((V_k_lat_waende + V_k_front_back) * (w + h / 2) + V_k_boden * w / 2) / V_k
    print(f'h_g = {h_g:.2f} m')
    return (h_g,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Höhe $h_v$ des Verdrängungsschwerpunkts:
    """)
    return


@app.cell
def _(d):
    h_v = d / 2
    print(f'Hoehe des Verdraengungsschwerpunkts h_v = {h_v:.2f} m')
    return (h_v,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Höhendifferenz $h_{gv}$ zwischen Gewichtsschwerpunkt und Verdrängungsschwerpunkt:
    """)
    return


@app.cell
def _(h_g, h_v):
    h_gv = h_g - h_v
    print(f'Hoehendifferenz h_gv = {h_gv:.2f} m')
    return (h_gv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Höhe $h_M$ des Metazentrums und Schwimmstabilität:
    """)
    return


@app.cell
def _(I_0, V_v, h_gv):
    h_M = I_0 / V_v - h_gv
    print(f'Hoehe des Metazentrums h_M = {h_M:.2f} m')

    if h_M > 0:
        print("Stabile Lage.")
    elif h_M < 0:
        print("Labile Lage.")
    else:
        print("Indifferente Lage.")
    return


if __name__ == "__main__":
    app.run()
