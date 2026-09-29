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
    # Hydraulische Durchbildung einer Staustufe

    Dieses Notebook fasst zwei zusammengehörige Aufgaben zusammen:

    1. **Hydraulische Vorbemessung des Wehrs** (Poleni, (n‑1)‑Regel)
    2. **Tosbeckenbemessung** (iterativer Workflow nach Bollrich / Peterka)

    Lernziele:
    - Rechengänge sehen;
    - Kernannahmen verstehen;
    - Größenordnungen prüfen können;
    - Grenzen von Vereinfachungen erkennen.
    """)
    return


@app.cell
def _():
    import math
    from scipy.optimize import brentq
    from pprint import pprint

    return brentq, math, pprint


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Teil 1: Hydraulische Vorbemessung

    ## Inhalte

    Es wird eine **überschlägige hydraulische Vorbemessung** eines vollregelnden Wehrs durchgeführt:

    - Wahl eines plausiblen Bemessungsfalls
    - Vorbemessung der erforderlichen lichten Wehrbreite
    - Aufteilung in Wehrfelder
    - Nachweis der **(n‑1)‑Regel** (DIN 19700)
    - Grober Check von Freibord
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gegebene Daten und Notation

    **Poleni-Gleichung** für den freien Überfall:

    $$
    Q = c \cdot \frac{2}{3} \cdot \mu \cdot b_{\text{eff}} \cdot \sqrt{2g} \cdot h_{\text{ü}}^{3/2}
    $$

    **Effektive Überflussbreite** (Einschnürung durch Pfeiler):

    $$
    b_{\text{eff}} = n \cdot \left(b_F - 2\,\xi_{\text{pf}}\,h_{\text{ü}}\right)
    $$

    *Herleitung: $b_{\text{eff}} = b_{\text{ges}} - \sum b_{\text{pf}} - 2\,n_{\text{pf}}\,\xi_{\text{pf}}\,h_{\text{ü}}$  mit $n_{\text{pf}} = (n-1) + 2\cdot0{,}5 = n$  Pfeileräquivalenten*

    | Symbol | Bedeutung |
    |---|---|
    | $Q$ | Durchfluss (m³/s) |
    | $b_{\text{eff}}$ | wirksame Wehrbreite (m) |
    | $h_{\text{ü}}$ | Überfallhöhe (m) |
    | $c$ | Abminderungsbeiwert bei unvollkommenem Überfall (–) |
    | $\mu$ | Abflussbeiwert (–) |
    | $h_{\text{ü,zul}}$ | zulässige Überfallhöhe bei BHQ₁ (m über Wehrkrone) |
    | $z_H$ | höchster zulässiger Oberwasserstand bei BHQ₁ **(m ü. NHN)**; $h_{\text{ü,zul}} = z_H - z_{\text{Kr}}$ |
    | $f$ | erforderlicher Freibord (m) |
    | $n$ | Anzahl Wehrfelder |
    | $b_F$ | Breite eines Wehrfelds (m) |
    | $b_{\text{pf}}$ | Breite eines Pfeilers (m) |
    | $\xi_{\text{pf}}$ | Einschnürungsbeiwert (–) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Eingangsgrößen
    """)
    return


@app.cell
def _():
    BHQ1 = 220.0    # m³/s  Bemessungshochwasser 1 (Regelfall)
    BHQ2 = 280.0    # m³/s  Bemessungshochwasser 2 (Kontrollfall)

    # h_ue_zul: zulässige Überfallhöhe über Wehrkrone bei BHQ1 (= z_H - z_Kr, relativ)
    # Nicht zu verwechseln mit z_H (absolutem Oberwasserstand in m ü. NHN, vgl. Notation)
    h_ue_zul = 1.0  # m
    f        = 1.0  # m  Freibord (DIN 19700: f ≥ 0,5 m bei BHQ1)

    mu      = 0.5  # Abflussbeiwert (bewegliches Wehr, scharfkantig)
    c       = 1.0   # Abminderungsbeiwert (vollkommener Überfall, Anfangswert)
    xi_pf   = 0.10  # Einschnürungsbeiwert (abgerundete Pfeilerköpfe)

    b_F  = 10.0              # m  gewählte Wehrfeldbreite (technisch bedingt)
    b_pf = b_F * 0.225       # m  Pfeilerbreite (Formel entspricht Drucksegmentverschlussmittel)

    g = 9.81  # m/s²

    print(f"Pfeilerbreite b_pf = {b_pf:.2f} m")
    return BHQ1, BHQ2, b_F, b_pf, c, f, g, h_ue_zul, mu, xi_pf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Poleni & erforderliche Wehrbreite

    **Entwurfsziel (DIN 19700, (n‑1)‑Regel):**
    Mit $(n-1)$ aktiven Wehrfeldern muss BHQ₁ abgeführt werden, ohne dass $h_{\text{ü}} > h_{\text{ü,zul}}$.

    Auflösung der Poleni-Gleichung nach $b_{\text{eff}}$:

    $$
    b_{\text{eff,erf}} = \frac{Q_{\text{BHQ}_1}}{c \cdot \frac{2}{3} \cdot \mu \cdot \sqrt{2g} \cdot h_{\text{ü,zul}}^{3/2}}
    $$

    Auflösung nach $h_{\text{ü}}$ (für gegebene Breite):

    $$
    h_{\text{ü}} = \left(\frac{Q}{c \cdot \frac{2}{3} \cdot \mu \cdot \sqrt{2g} \cdot b_{\text{eff}}}\right)^{2/3}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hilfsfunktionen für Poleni-Solver
    """)
    return


@app.cell
def _(b_F, g, math, mu, xi_pf):
    c_pol = (2/3) * mu * math.sqrt(2 * g)  # kombinierter Poleni-Koeffizient ohne b und h_ue

    def b_eff_von_Q(Q, h_ue, c_abd=1.0):
        """Erforderliche effektive Wehrbreite für gegebenen Durchfluss."""
        return Q / (c_abd * c_pol * h_ue**1.5)

    def h_ue_von_Q(Q, b_eff, c_abd=1.0):
        """Überfallhöhe bei gegebenem Durchfluss und effektiver Breite."""
        return (Q / (c_abd * c_pol * b_eff))**(2/3)

    def b_eff_n_felder(n_aktiv, h_ue):
        """Effektive Breite für n_aktiv nebeneinanderliegende Felder (Einschnürung berücksichtigt)."""
        return n_aktiv * (b_F - 2 * xi_pf * h_ue)

    return b_eff_n_felder, b_eff_von_Q, c_pol, h_ue_von_Q


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Erforderliche Breite und Anzahl Wehrfelder
    """)
    return


@app.cell
def _(BHQ1, b_F, b_eff_von_Q, c, c_pol, h_ue_zul, xi_pf):
    # Gesamte b_eff für (n-1)-Fall muss b_eff_erf >= b_eff_von_Q(BHQ1, h_ue_zul) erfüllen
    b_eff_erf = b_eff_von_Q(BHQ1, h_ue_zul, c)
    b_F_eff   = b_F - 2 * xi_pf * h_ue_zul     # wirksame Feldbreite je Feld

    n         = 5   # Gesamtanzahl Wehrfelder
    n_eff  = n-1 # (n-1)-Regel

    print(f"Kombinierter Poleni-Koeffizient c_pol = {c_pol:.4f}")
    print(f"Erforderliche b_eff (n-1-Fall) = {b_eff_erf:.2f} m")
    print(f"Wirksame Feldbreite b_F_eff    = {b_F_eff:.2f} m")
    print(f"Benötigte (n-1)-Felder         = {n_eff}")
    print(f"Gewählte Wehrfeldanzahl n      = {n}")
    return n, n_eff


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wehrabmessungen und Breite
    """)
    return


@app.cell
def _(b_F, b_pf, n_eff):
    n_pfeiler  = n_eff - 1               # Zwischenpfeiler
    b_licht    = n_eff * b_F             # lichte Gesamtbreite (nur Felder)
    b_pfeiler  = n_pfeiler * b_pf    # Summe Pfeilerbreiten
    b_gesamt   = b_licht + b_pfeiler # Gesamtbreite inkl. Pfeiler

    print(f"Anzahl Zwischenpfeiler : {n_pfeiler}")
    print(f"Lichte Gesamtbreite    : {b_licht:.1f} m")
    print(f"Summe Pfeilerbreiten   : {b_pfeiler:.2f} m")
    print(f"Bauwerksbreite gesamt  : {b_gesamt:.2f} m")
    return b_gesamt, b_licht


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## (n‑1) -- Nachweis -- hier: (n-2)

    **Bedingung:** Mit $(n-1)$ aktiven Feldern muss gelten: $h_{\text{ü}} \leq h_{\text{ü,zul}}$

    Zusätzlich werden BHQ₁ und BHQ₂ mit allen $n$ Feldern geprüft.
    """)
    return


@app.cell
def _(BHQ1, BHQ2, b_eff_n_felder, c, h_ue_von_Q, h_ue_zul, n, n_eff):
    faelle = [
        ("BHQ1,  n Felder",   BHQ1, n),
        ("BHQ1, (n-1) Felder",    BHQ1, n_eff),
        ("BHQ2,  n Felder",   BHQ2, n),
    ]

    print(f"{'Fall':<28} {'n_akt':>5} {'b_eff':>8} {'h_ü':>7} {'≤ h_ü,zul?':>10}")
    print("-" * 62)
    for label, Q, n_akt in faelle:
        h_ue_iter = h_ue_zul
        for _ in range(20):
            beff = b_eff_n_felder(n_akt, h_ue_iter)
            h_ue_neu = h_ue_von_Q(Q, beff, c)
            if abs(h_ue_neu - h_ue_iter) < 1e-6:
                break
            h_ue_iter = h_ue_neu
        ok = "OK" if h_ue_iter <= h_ue_zul else "!!"
        print(f"{label:<28} {n_akt:>5} {beff:>8.2f} {h_ue_iter:>7.3f} {ok:>10}")

    print(f"\n  h_ü,zul = {h_ue_zul:.2f} m  (max. zulässige Überfallhöhe bei BHQ1)")

    # h_ue bei BHQ1 mit allen n Feldern (für Zusammenfassung Teil 1)
    h_ue_n = h_ue_zul
    for _ in range(20):
        beff_n = b_eff_n_felder(n, h_ue_n)
        h_ue_n = h_ue_von_Q(BHQ1, beff_n, c)
    return (h_ue_n,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Freibord-Check

    Kronenhöhe = $h_{\text{ü,zul}} + f \quad \text{mit} \quad f \geq 0{,}5\,\text{m (BHQ}_1\text{)}$
    """)
    return


@app.cell
def _(BHQ1, b_eff_n_felder, c, f, h_ue_von_Q, h_ue_zul, n):
    # h_ue bei BHQ1, (n-1)-Felder (konservativster Fall)
    h_ue_n1 = h_ue_zul
    for _ in range(20):
        _beff_n1 = b_eff_n_felder(n - 1, h_ue_n1)
        h_ue_n1 = h_ue_von_Q(BHQ1, _beff_n1, c)
    freibord_errechnet = h_ue_zul - h_ue_n1
    kronenhoehe = h_ue_zul + f
    print(f'h_ü bei BHQ1, (n-1)-Felder       : {h_ue_n1:.3f} m')
    print(f'Freibord über h_ü bis h_ü,zul    : {freibord_errechnet:.3f} m')
    print(f'Kronenhöhe (= h_ü,zul + f)       : {kronenhoehe:.2f} m über Wehrschwelle')
    freibord_kriterium = 'OK' if f >= abs(freibord_errechnet) else 'Nicht erfüllt'
    print(f'Freibordanforderung: ' + freibord_kriterium)
    return freibord_errechnet, freibord_kriterium, kronenhoehe


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # Teil 2: Tosbeckenbemessung

    ## Konzept

    Ziel ist es, den **Wechselsprung** innerhalb des Tosbeckens zu erzwingen. Konstruktiver Freiheitsgrad: **Tosbeckeneintiefung** $e$ (in m).

    **Einstaugrad** $\varepsilon$ muss im Zielbereich liegen:
    $$
    \varepsilon = \frac{h_u + e}{h_2} \in [1{,}05;\; 1{,}15]
    $$

    **Iterativer Algorithmus** (vgl. Vorlesungsfolie):

    | Schritt | Inhalt |
    |:---:|---|
    | **A** | $e$ festlegen (Startwert) |
    | **B** | $h_1$, $v_1$ aus Bernoulli-Gleichung (Energiehöhe $H_{\text{ges}}$) |
    | **C** | $Fr_1 = v_1 / \sqrt{g\,h_1}$ |
    | **D** | $4{,}5 \leq Fr_1 < 9{,}0$?  → Nein: $e$ anpassen |
    | **E** | $h_u$ aus Manning–Strickler bzw. gemessen |
    | **F** | $h_2 = \dfrac{h_1}{2}\left(\sqrt{1+8\,Fr_1^2}-1\right)$ (Bélanger) |
    | **G** | $1{,}05 \leq \varepsilon \leq 1{,}15$?  → Nein: $e$ anpassen |
    | **+** | $l_T$ und $l_K$ berechnen |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zusätzliche Eingangsgrößen Tosbecken

    Neben den Wehrparametern werden benötigt:

    | Symbol | Bedeutung |
    |---|---|
    | $n_{\text{tos}}$ | Anzahl Wehrfelder in Teil 2 (Frage 2) |
    | $w$ | Wehrhöhe über UW-Sohle (m) |
    | $k_{St}$ | Strickler-Beiwert der UW-Strecke (m¹/³/s) |
    | $I_E$ | Sohlgefälle der UW-Strecke (–) |
    | $B_u$ | Breite der UW-Strecke (m) |
    | $H_{\text{ges}}$ | Gesamtenergielinie über Tosbeckensohle: $H_{\text{ges}} = h_{\text{ü,zul}} + w + e$ |

    Der Einheitsdurchfluss $q$ für die Tosbeckenbemessung wird konservativ aus dem **$(n_{\text{tos}}-1)$-Felder-Fall** berechnet (DIN 19700, (n‑1)‑Regel): Mit einem ausgefallenen Feld steigt $q$ je Feldbreite — das ist der maßgebende Lastfall für das Tosbecken.
    """)
    return


@app.cell
def _(BHQ1, b_eff_n_felder, c, h_ue_von_Q, h_ue_zul, n_eff):
    w_wehr = 5.0
    k_st = 32.0
    I_E = 0.0004
    b_u = 150.0
    for _ in range(20):
        _beff_n1 = b_eff_n_felder(n_eff - 1, h_ue_zul)
        h_ue_n1_1 = h_ue_von_Q(BHQ1, _beff_n1, c)
    q = BHQ1 / _beff_n1
    print(f'Anzahl Wehrfelder (Teil 2): n_tos       = {n_eff}')
    print(f'(n_tos-1)-Wehrbreite (BHQ1): b_eff       = {_beff_n1:.2f} m,  h_ü = {h_ue_zul:.3f} m')
    print(f'Einheitsdurchfluss q = BHQ1 / b_eff      = {q:.3f} m²/s')
    return I_E, b_u, h_ue_n1_1, k_st, q, w_wehr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Unterwassertiefe $h_u$ durch Manning-Strickler (Vorbereitung Schritt E)

    Für ein **Rechteckprofil** gilt:
    $$
    Q = k_{St} \cdot A \cdot R^{2/3} \cdot I_E^{1/2}
    \qquad \text{mit } A = b_u \cdot h_u,\quad R = \frac{b_u \cdot h_u}{b_u + 2\,h_u}
    $$

    /// admonition | Rechteckprofilannahme ist fehleranfällig
        type: important

    Natürliche Flüsse sind komplex und die Annahme eines Rechteckprofils ist ungenau. Es empfiehlt sich bessere Aussagen durch Messungen, numerische Modellierung oder aus digitalen Höhenmodellen bzw. Lidar-Daten abzuleiten.
    ///
    Ein numerischer 1D-Gleichungslöser für die Manning kann mittels folgender Funktion definiert und in der Folge aufgerufen werden:
    """)
    return


@app.cell
def _(BHQ1, I_E, b_u, brentq, k_st, math):
    def Q_manning(h, b, k, I):
        A = b * h
        R = (b * h) / (b + 2 * h)
        return k * A * R**(2/3) * math.sqrt(I)

    # brentq sucht h in [0.01, 20] m mit Q_manning(h) = BHQ1
    h_u = brentq(lambda h: Q_manning(h, b_u, k_st, I_E) - BHQ1, 0.01, 20.0)

    print(f"Unterwassertiefe h_u = {h_u:.3f} m")
    print(f"Probe: Q_Manning = {Q_manning(h_u, b_u, k_st, I_E):.2f} m³/s  (Soll: {BHQ1} m³/s)")
    return (h_u,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Schritte A bis G: Iterative Tosbecken-Bemessung

    ### Schritt B Herleitung von $h_1$ und $v_1$

    Energiehöhe über Tosbeckensohle (Bernoulli, vernachlässige $v_0$ da $v_0 < $ 1,0 m/s):
    $$
    H_{\text{ges}} = h_{\text{ü,zul}} + w + e
    $$

    Am schießenden Querschnitt 1 (Tosbeckeneinlauf):
    $$
    H_{\text{ges}} = h_1 + \frac{v_1^2}{2g} = h_1 + \frac{q^2}{2g\,h_1^2}
    $$

    ### Kodieren des Arbeitsablaufs
    Der Arbeitsablauf (Workflow) der Tosbeckenbemessung sowie die Ermittlung des k-Faktor in Abhängigkeit der Froude-Zahl wird in zwei Funktionen definiert, mit $e$ als Eingangsvariable:
    """)
    return


@app.cell
def _(brentq, g, h_u, h_ue_zul, math, q, w_wehr):
    def tosbecken_check(e):
        """
        Führt Schritte A-G des Tosbecken-Workflows für gegebene Eintiefung e durch.
        Gibt (Fr1, epsilon, h1, h2, ok_Fr, ok_eps) zurück.
        """
        # Schritt B: h1 aus Bernoulli (kleine, schießende Wurzel)
        H_ges = h_ue_zul + w_wehr + e
        # Suche h1 < h_grenz (kritische Tiefe) = (q**2/g)^(1/3)
        h_krit = (q**2 / g)**(1/3)
        h1 = brentq(lambda h: h + q**2 / (2 * g * h**2) - H_ges, 1e-4, h_krit)
        v1 = q / h1

        # Schritt C: Froude-Zahl
        Fr1 = v1 / math.sqrt(g * h1)

        # Schritt D: Fr1-Check
        ok_Fr = 4.5 <= Fr1 < 9.0

        # Schritt F: konjugierte Tiefe h2 (Belanger)
        h2 = (h1 / 2) * (math.sqrt(1 + 8 * Fr1**2) - 1)

        # Schritt G: Einstaugrad
        eps = (h_u + e) / h2
        ok_eps = 1.05 <= eps <= 1.15

        return Fr1, eps, h1, h2, ok_Fr, ok_eps


    # k-Faktor für Tosbeckenlänge (vgl. Peterka 1984 / USBR)
    def k_faktor(Fr1):
        if   Fr1 < 2.4:  return 4.8
        elif Fr1 < 4.0:  return 4.8 + (Fr1 - 2.4) / (4.0 - 2.4) * (5.8 - 4.8)
        elif Fr1 < 5.0:  return 5.8 + (Fr1 - 4.0) * (6.0 - 5.8)
        elif Fr1 < 6.0:  return 6.0
        elif Fr1 <= 11.0: return 6.13
        else:            return 6.0

    return k_faktor, tosbecken_check


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Iterieren über $e$
    Die Eintiefung kann nun mittels der zuvor definierten Funktionen berechnet werden, basierend auf einem Startwert und einem Wertebereich:
    """)
    return


@app.cell
def _(tosbecken_check):
    e_test   = 2.0   # m Startwert (Schritt A)
    e_min    = 0.0   # m Suchbereich untere Grenze
    e_max    = 3.0   # m Suchbereich obere Grenze
    iterationen = []

    print(f"{'Iter':>4}  {'e [m]':>7}  {'Fr1':>6}  {'Fr-OK':>6}  {'h1 [m]':>8}  {'h2 [m]':>8}  {'ε':>6}  {'ε-OK':>6}")
    print("-" * 65)

    for i in range(1, 15):
        Fr1, eps, h1, h2, ok_Fr, ok_eps = tosbecken_check(e_test)
        iterationen.append((e_test, Fr1, eps, h1, h2, ok_Fr, ok_eps))

        fr_sym  = "OK" if ok_Fr  else "Nicht erfüllt"
        eps_sym = "OK" if ok_eps else "Nicht erfüllt"
        print(f"{i:>4}  {e_test:>7.3f}  {Fr1:>6.2f}  {fr_sym:>6}  {h1:>8.4f}  {h2:>8.4f}  {eps:>6.3f}  {eps_sym:>6}")

        if ok_Fr and ok_eps:
            print("\n >>> Kriterien erfüllt: Iteration beendet.")
            break

        # Anpassungsstrategie (Bisektionslogik)
        if not ok_Fr:
            # Fr1 < 4.5 >>> e zu groß; Fr1 ≥ 9.0 >>> e zu klein
            if Fr1 < 4.5:
                e_max = e_test
            else:  # Fr1 >= 9.0
                e_min = e_test
        else:
            # ok_Fr = True, aber ok_eps = False
            if eps > 1.15:   # zu viel Einstau >>> e verringern
                e_max = e_test
            else:            # eps < 1.05 >>> zu wenig Einstau >>> e erhöhen
                e_min = e_test

        e_test = 0.5 * (e_min + e_max)  # Bisektion

    # Endwerte speichern
    e_opt  = e_test
    Fr1_opt, eps_opt, h1_opt, h2_opt, _, eps_test = tosbecken_check(e_opt)
    return Fr1_opt, e_opt, eps_opt, eps_test, h1_opt, h2_opt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tosbeckenlänge $l_T$ und Kolkschutzlänge $l_K$

    Nach Peterka (1958/1984):

    $$
    l_T = k \cdot h_2 \qquad l_K = 3{,}5 \cdot l_T
    $$

    | $Fr_1$ | 2,4 | 4 | 5 | 6–11 | 14 |
    |---|---|---|---|---|---|
    | $k$ | 4,8 | 5,8 | 6 | 6,13 | 6 |

    Tosbecken- und Kolkschutzlänge können durch Aufrufen der oben definierten Funktion für die Abschätzung des k-Faktors berechnet werden:
    """)
    return


@app.cell
def _(Fr1_opt, e_opt, eps_opt, h1_opt, h2_opt, h_u, k_faktor):
    k   = k_faktor(Fr1_opt)
    l_T = k * h2_opt
    l_K = 3.5 * l_T

    print(f"Optimierte Eintiefung   e   = {e_opt:.3f} m")
    print(f"Schießende Tiefe        h1  = {h1_opt:.4f} m")
    print(f"Froude-Zahl             Fr1 = {Fr1_opt:.2f}")
    print(f"Konjugierte Tiefe       h2  = {h2_opt:.3f} m")
    print(f"Unterwassertiefe        h_u = {h_u:.3f} m")
    print(f"Einstaugrad             ε   = {eps_opt:.3f}  (Ziel: 1,05-1,15)")
    print()
    print(f"k-Faktor (Fr1={Fr1_opt:.1f})  k   = {k:.2f}")
    print(f"Tosbeckenlänge          l_T = {l_T:.2f} m")
    print(f"Kolkschutzlänge         l_K = {l_K:.2f} m")
    return k, l_K, l_T


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zusammenfassung der hydraulischen Durchbildung inkl. Tosbeckenbemessung
    """)
    return


@app.cell
def _(
    BHQ1,
    BHQ2,
    Fr1_opt,
    b_gesamt,
    b_licht,
    e_opt,
    eps_opt,
    eps_test,
    freibord_errechnet,
    freibord_kriterium,
    h1_opt,
    h2_opt,
    h_u,
    h_ue_n,
    h_ue_n1_1,
    h_ue_zul,
    k,
    kronenhoehe,
    l_K,
    l_T,
    pprint,
):
    summary = {'Hydraulik_Wehr': {'BHQ1 (m3/s)': BHQ1, 'BHQ2 (m3/s)': BHQ2, 'h_ue_zul (m)': h_ue_zul, 'Freibord (m)': freibord_errechnet, 'Lichte Breite (m)': round(b_licht, 2), 'Gesamtbreite (m)': round(b_gesamt, 2), 'hü bei BHQ1 mit n Feldern (m)': round(h_ue_n, 3), 'hü bei BHQ1 mit (n-1) Feldern (m)': round(h_ue_n1_1, 3), 'Kronenhöhe (m)': round(kronenhoehe, 2), 'Nachweis Hochwassersicherheit': freibord_kriterium}, 'Tosbecken': {'hu (m)': round(h_u, 3), 'eopt (m)': round(e_opt, 3), 'h1 (m)': round(h1_opt, 4), 'h2 (m)': round(h2_opt, 3), 'Fr1': round(Fr1_opt, 2), 'epsilon': round(eps_opt, 3), 'k': round(k, 2), 'lT (m)': round(l_T, 2), 'lK (m)': round(l_K, 2), 'Energieumwandlung im Tosbecken': 'OK' if eps_test else 'Nicht erfüllt'}}
    pprint(summary)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Grenzen der Vereinfachung

    Dieses Notebook ersetzt **nicht**:

    - standortbezogene Hydrologie (BHQ-Bestimmung)
    - 1D/2D-Wasserstandsberechnungen für mehrere Abflüsse
    - die Rechteckannahme für das Unterwasser ist schwach und sollte durch genauere hydraulische und Geländedaten ersetzt werden
    - Nachweise für mehrere Last- und Ausfallfälle (a > 1, BHQ₂, ...)
    - geotechnische Nachweise
    - konstruktive Bemessung nach den jeweils einschlägigen Regeln
    - Nachweise für Fischdurchgängigkeit, Sedimentmanagement und Betriebssicherheit
    """)
    return


if __name__ == "__main__":
    app.run()
