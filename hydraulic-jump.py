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
    # Hydraulic jump design exercise

    This exercise **orientates at** Clyde Dam, on the Clutha River / Mata-Au in Central Otago, is New Zealand's largest concrete gravity dam: 490 m wide, up to 60 m high above the old riverbed, and impounding Lake Dunstan. Its gated spillway has four radial gates, each 15 m high and 10 m wide, designed to route a discharge of 3200 m$^3$/s (0.2% AEP) at a lake level of 195.1 m. The water passing the spillway descends a chute on the dam face. The high-energy flow at the toe of that chute must be dissipated in a **stilling basin**, so that the riverbed downstream is not scoured.

    > **Student challenge:** size the basin geometry so that the hydraulic jump forms inside the basin and is retained there, and scour downstream of the dam is thereby avoided.

    ## Calculation template structure

    ### Overview

    | | part | who does the work |
    |---|---|---|
    | **I** | The flow arriving at the basin: unit discharge, energy head at the chute toe and tailwater depth | **given** -- run the cells and read the results |
    | **II** | Stilling-basin & hydraulic jump design | **student** -- workflow is given, hydraulic-jump equations need to be entered |

    ### Details

    **Part I** establishes the quantities on which the jump, and therefore the basin, is designed: the discharge $Q$ and the unit discharge $q$, the energy head $H_0$ above the un-sunk basin invert, and the tailwater depth $h_{tw}$ obtained from the Manning equation.

    **Part II** contains three short functions, marked `Task 1` to `Task 3`. Each is a single equation from the lecture. The numerics around them, that is the root finding, the search over the basin depth and the plots, are given, so that an incorrect equation produces an incorrect number rather than a traceback. The equation at the centre of the exercise is the sequent-depth (Bélanger) equation of Task 2; the other two establish the state it is applied to and the criterion by which the result is judged. On completing Part II you should be able to:

    * express the energy, continuity and momentum relations that fix a hydraulic jump as code;
    * determine whether a given tailwater level retains a jump in a basin or sweeps it downstream;
    * determine the depth, length and scour protection of a basin from those relations.

    ### Notation

    Depths are denoted $h$ and heads $H$, in the lecture and here alike. The retention ratio is denoted $r_{\mathrm{t}}$ rather than the $\varepsilon$ of the German worked example from which this workflow is adapted, because $\varepsilon$ denotes the turbulent dissipation rate in the lecture.

    | symbol | meaning | unit |
    |---|---|---|
    | $Q$ | spillway design flow | m$^3$/s |
    | $w$ | width of the stilling basin | m |
    | $w_{tw}$ | tailwater river width | m |
    | $q$ | discharge per unit width, $q = Q/w$ | m$^2$/s |
    | $H_0$ | energy head above the un-sunk basin invert | m |
    | $\mathbf{d_b}$ | depth of the basin floor below the downstream bed | m |
    | $H$ | energy head above the basin floor, $H = H_0 + \mathbf{d_b}$ | m |
    | $h_1$, $v_1$, $Fr_1$ | depth, velocity and Froude number at the basin entrance (supercritical) | m, m/s, -- |
    | $h_2$ | conjugate (sequent) depth of the jump | m |
    | $h_{tw}$ | tailwater depth in the downstream reach | m |
    | $n_M$ | Manning roughness coefficient of the downstream reach | s/m$^{1/3}$ |
    | $r_{\mathrm{t}}$ | retention ratio, $(h_{tw} + \mathbf{d_b})/h_2$ | -- |
    | $S_{0,tw}$ | longitudinal bed slope of the downstream reach | -- |
    | $\Delta H$ | head loss across the jump | m |
    | $f_{l}$ | Peterka basin-length multiplier, read from $Fr_1$ | -- |
    | $l_b$, $l_s$ | basin length and scour-protection length | m |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following cell imports the Python packages and the colours used for the figures. These cells serve the functioning of the calculation template and carry no learning content.
    """)
    return


@app.cell
def _():
    import math
    from dataclasses import dataclass

    import matplotlib.patheffects as pe
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.optimize import brentq

    # Physical constants used throughout.
    G = 9.81  # gravitational acceleration [m/s2]

    # The lecture palette, so that figures and slides read as one piece.
    NAVY, BLUE, CYAN, GREEN, WARN, GREY = (
        "#0C0C48", "#00467F", "#00CAEF", "#167D61", "#C74B2A", "#4A4A4C",
    )

    plt.rcParams.update({
        "figure.figsize": (8.4, 4.2),
        "figure.dpi": 110,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "axes.labelcolor": NAVY,
        "axes.edgecolor": NAVY,
        "text.color": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
        "font.size": 9,
    })
    return (
        BLUE,
        CYAN,
        G,
        GREY,
        NAVY,
        WARN,
        brentq,
        dataclass,
        math,
        np,
        pe,
        plt,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part I: boundary conditions for the hydraulic jump design

    Everything in this part is given. Run the cells and note the quantities passed on to Part II. No hydraulic-jump calculation is performed here.

    > **Important:** only discharge, the associated lake level and gate dimensions are published figures that actually relate to Clyde Dam. The remainder of the assumptions in this exercise do not correspond to Clyde Dam. The real structure is more complex: a gate-controlled sluice with a capacity of 1,500 m³/s adjoins the spillway, which can pass the largest anticipated flood of 6,820 m³/s. Additionally, the Ministry of Works and Development developed the energy dissipation at the toe on physical models rather than through a closed-form calculation. This exercise therefore represents the initial stage in the process typically undertaken by engineers before a detailed design study involving physical or numerical models; it is not a substitute for such a study.

    | quantity | value | remark |
    |---|---|---|
    | $Q$, spillway design flow | 3200 m$^3$/s | published, at a lake level of 195.1 m |
    | $w$, width of the chute and basin | 40 m | four 10 m gate bays, idealised as one rectangular chute with the piers ignored |
    | $H_0$, energy head above the un-sunk basin invert | 50.00 m | assumed: the design flood level stands approximately 60 m above the riverbed, of which some 10 m is taken as lost down the chute |
    | $w_{tw}$, $n_M$, $S_{0,tw}$ of the Clutha downstream of the dam | 60 m, 0.045 s/m$^{1/3}$, 0.0006 | assumed |

    In New Zealand practice, catchment design floods are quoted as an annual exceedance probability, so the 100-year flood is the 1% AEP event and the 500-year flood quoted for Clyde is the 0.2% AEP event; the older average recurrence interval (ARI) denotes the same thing. A dam spillway, however, is not designed to a catchment AEP at all: under the NZSOLD *New Zealand Dam Safety Guidelines* the inflow design flood follows from the dam's Potential Impact Classification, and for a high-consequence dam it extends to the probable maximum flood.

    The following cell defines these hydrological, hydraulic and geometric boundary conditions.
    """)
    return


@app.cell
def _():
    # --- the design discharge ----------------------------------------------------
    Q_design = 3200.0  # m3/s   Clyde Dam spillway design flow at lake level 195.1 m
                       #        (published; the 500-year, 0.2% AEP flood)

    # --- the chute toe and the stilling basin below it ---------------------------
    w_chute = 40.0     # m      four 10 m gate bays, idealised as one rectangle
    H0 = 50.00         # m      energy head above the un-sunk basin invert (assumed)

    # --- the Clutha River below the dam (assumed) --------------------------------
    n_manning = 0.045   # s/m^(1/3)  Manning roughness of the downstream reach
    slope = 6.0e-4      # -          bed slope of the downstream reach
    w_tw = 60.0         # m          width of the downstream reach (rectangular idealisation)
    h_tw = 19.060       # m          tailwater depth of that reach in uniform flow

    print(f"spillway design flow Q  = {Q_design:7.1f} m3/s")
    print(f"chute and basin width w = {w_chute:7.2f} m")
    print(f"head at the invert   H0 = {H0:7.2f} m")
    return H0, Q_design, h_tw, w_chute, w_tw


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Boundary calculation
    ### Unit discharge

    For the hydraulic jump calculation, discharge per metre of width is needed:

    $$q = \frac{Q}{w}$$

    The chute delivers this flow supercritically, which is the condition for a jump to form. The critical depth printed below is the upper bound on the entry depth $h_1$, and Part II uses it as the bracket when solving the energy equation.
    """)
    return


@app.cell
def _(G, Q_design, w_chute):
    q_unit = Q_design / w_chute
    h_crit = (q_unit**2 / G)**(1 / 3)

    print(f"unit discharge   q = Q / w   = {q_unit:7.3f} m2/s")
    print(f"critical depth   h_c         = {h_crit:7.3f} m")
    print(f"critical velocity            = {q_unit / h_crit:7.3f} m/s")
    return (q_unit,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tailwater depth $h_{tw}$

    The depth in the downstream reach determines whether the jump is retained or swept out, and it is set by the reach itself rather than by the spillway. For a rectangular channel in uniform flow, the Manning equation gives

    $$Q = \frac{1}{n_M}\,A\,R^{2/3}\,\sqrt{S_{0,tw}}, \qquad A = w_{tw}\,h_{tw}, \qquad R = \frac{w_{tw}\,h_{tw}}{w_{tw} + 2\,h_{tw}}$$

    Evaluating this for the reach above gives $h_{tw} = 19.060$ m, which is assigned directly in the cell below and used from there on.

    > **Note:** Natural channels are not rectangular, and $h_{tw}$ enters the retention ratio directly. In practice the tailwater rating curve is obtained from gauging, a numerical model, or terrain data, and a range of tailwater levels is tested rather than a single value.

    The cell below also prints the critical depth of the downstream reach, since a jump can terminate in the tailwater only while that reach is subcritical.
    """)
    return


@app.cell
def _(G, Q_design, h_tw, w_tw):
    h_crit_tw = ((Q_design / w_tw)**2 / G)**(1 / 3)

    print(f"tailwater depth h_tw = {h_tw:.3f} m   (given, from the reach above)")
    print(f"critical depth of the reach = {h_crit_tw:.3f} m"
          f"   -> {'subcritical' if h_tw > h_crit_tw else 'SUPERCRITICAL'}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Define data structures & default values

    The following code block builds the required data structures and sets default values for the core part II.
    """)
    return


@app.cell
def _(H0, Q_design, dataclass, h_tw, q_unit, w_chute):
    @dataclass(frozen=True)
    class DesignData:
        Q: float       # spillway design flow [m3/s]
        q: float       # discharge per unit width [m2/s]
        H0: float      # energy head above the un-sunk basin invert [m]
        h_tw: float    # tailwater depth [m]
        w: float       # width the basin has to cover [m]


    DESIGN = DesignData(
        Q=Q_design,
        q=q_unit,
        H0=H0,
        h_tw=h_tw,
        w=w_chute,
    )

    print(f"Q      = {DESIGN.Q:8.1f} m3/s   spillway design flow")
    print(f"q      = {DESIGN.q:8.3f} m2/s   unit discharge")
    print(f"H0     = {DESIGN.H0:8.2f} m      energy head above the un-sunk invert")
    print(f"h_tw   = {DESIGN.h_tw:8.3f} m      tailwater depth")
    print(f"w      = {DESIGN.w:8.2f} m      width the basin has to cover")
    return (DESIGN,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part II: Stilling basin & hydraulic jump design

    ## The sequent depth (Bélanger) equation

    For a horizontal, rectangular channel, the position and size of the jump follow from momentum conservation, the hydrostatic pressure forces and continuity. Given that the specific force is equal upstream (1) and downstream (2) of the jump, that is, $M_1 = M_2$ with $M = q^2/(g\,h) + h^2/2$, the depth ratio is calculated by the sequent-depth equation of Bélanger:

    $$\boxed{\;\frac{h_2}{h_1} = \frac{1}{2}\left(\sqrt{1 + 8\,Fr_1^{2}} - 1\right)\;}$$

    Notably, $h_1$ and $h_2$ are the **sequent** (conjugate) depths. Every subsequent quantity in this exercise is obtained from $h_2$: the retention ratio that indicates whether the jump stays in the basin, the basin length, and the required length of downstream scour protection.

    ## Design problem

    The position of the jump is not fixed by the spillway. It is controlled by the **tailwater depth**: a jump forms where the downstream depth matches the conjugate depth $h_2$ belonging to the incoming supercritical state. Where the tailwater is too shallow the jump is **swept out** onto unprotected downstream riverbed; where it is too deep the jump is **drowned** and dissipates less.

    The single design freedom is the **basin depth** $\mathbf{d_b}$, by which the basin floor is set below the downstream riverbed. Increasing $\mathbf{d_b}$ acts in two opposing directions:

    1. it increases the energy head $H = H_0 + \mathbf{d_b}$ above the floor, so the entry flow is faster and shallower, which raises $Fr_1$ and hence $h_2$;
    2. it increases the depth available over the floor, namely $h_{tw} + \mathbf{d_b}$.

    An acceptable design is a basin depth at which both engineering objectives are satisfied simultaneously:

    $$4.5 \le Fr_1 < 9.0 \qquad\text{and}\qquad 1.05 \le r_{\mathrm{t}} = \frac{h_{tw} + \mathbf{d_b}}{h_2} \le 1.15$$

    The first engineering objective is the **steady jump** that leads to 45% to 70% head loss, and no oscillating surge to fatigue the structure. The second engineering objective requires the basin to hold slightly more water than the jump needs, so that the jump is retained with a small margin without being drowned.

    ## The workflow

    The steps run in the order of the table, and each one is either given or one of the three tasks:

    | content | hint |
    |---|---|
    | choose a trial basin depth $\mathbf{d_b}$ | here: 1.0 m (given) |
    | $h_1$ and $v_1$ from the energy equation at the entrance | given |
    | $Fr_1 = v_1/\sqrt{g\,h_1}$ | **Task 1** |
    | is $4.5 \le Fr_1 < 9.0$? if not, adjust $\mathbf{d_b}$ | given |
    | the conjugate depth $h_2$ from the Bélanger equation | **Task 2** |
    | is $1.05 \le r_{\mathrm{t}} \le 1.15$? if not, adjust $\mathbf{d_b}$ | **Task 3** + given |
    | basin length $l_b$ and scour-protection length $l_s$ | given |
    | head loss $\Delta H$ | given |

    ## The three tasks

    Each task is one equation from the lecture.

    **Replace the `raise NotImplementedError(...)` line with a `return` statement.**

    **The function names and their arguments must not be changed, because the workflow below calls them.**

    > **Important:** On completing each task, run the **self-check** cell. It marks each function `[OK]` or `[XX]` against the lecture values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Given: energy head above the basin floor

    Neglecting the approach velocity, the energy head available above the basin floor is $H = H_0 + \mathbf{d_b}$. At the basin entrance, that is, cross section 1, that head is split between depth and velocity head. With continuity $v = q/h$ for a rectangular section,

    $$H = h + \frac{v^2}{2g} = h + \frac{q^2}{2g\,h^2}$$

    The right-hand side is coded below as a function of $h$ and $q$. Read it, because the entry state of every trial basin depth comes from it: the given solver `entry_depth` further down selects the shallow, supercritical root of `energy_head(h, q) == H`, which is the branch delivered by the chute.
    """)
    return


@app.cell
def _(G):
    def energy_head(h, q, g=G):
        '''
        Given: specific energy head of a rectangular section [m].

        Parameters
        ----------
        h : flow depth [m]
        q : discharge per unit width [m2/s]

        Returns
        -------
        the energy head h + q^2 / (2 g h^2) [m]
        '''
        return h + q**2 / (2 * g * h**2)

    return (energy_head,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Froude number

    The Froude number compares the flow velocity with the shallow-water wave speed $c = \sqrt{g h}$:

    $$Fr = \frac{v}{\sqrt{g\,h}}$$

    Recall that $Fr > 1$ denotes supercritical and $Fr < 1$ subcritical flow. This step of the workflow only calculates the value of the Froude number (here: $Fr_1$) for the later comparison against the steady-jump window:
    """)
    return


@app.cell
def _(G):
    def froude_number(v, h, g=G):
        '''
        Task 1: Froude number of a rectangular section [-].

        Parameters
        ----------
        v : depth-averaged velocity [m/s]
        h : flow depth [m]
        '''
        # >>> YOUR CODE HERE
        raise NotImplementedError("Task 1: return the Froude number")

    return (froude_number,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2: sequent depth (Bélanger) equation

    **This is the central equation of the exercise.** Implement the depth ratio at cross sections 2 ($h_2$) and 1 ($h_1$):

    $$\frac{h_2}{h_1} = \frac{1}{2}\left(\sqrt{1 + 8\,Fr_1^{2}} - 1\right)$$

    > **Note:** This equation describes neither the roller between the cross sections nor the internal structure of the jump. Everything the design requires after this point, that is the retention ratio, the basin length and the scour-protection length, follows from the $h_2$ sequent depth equation returns.
    """)
    return


@app.function
def conjugate_depth(h1, Fr1):
    '''
    Task 2: conjugate (sequent) depth downstream of the jump [m].

    Parameters
    ----------
    h1  : supercritical depth upstream of the jump [m]
    Fr1 : Froude number at section 1 [-]
    '''
    # >>> YOUR CODE HERE
    raise NotImplementedError("Task 2: return the conjugate depth h2")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: retention ratio

    The water depth over the basin floor is the tailwater depth plus the basin depth. Comparing it with the depth the jump demands results in the retention ratio:

    $$r_{\mathrm{t}} = \frac{h_{tw} + \mathbf{d_b}}{h_2}$$

    $r_{\mathrm{t}} < 1$ means the basin cannot supply the conjugate depth and the jump is swept downstream; $r_{\mathrm{t}}$ well above 1 means the jump is drowned. The retention check asks for $1.05 \le r_{\mathrm{t}} \le 1.15$.
    """)
    return


@app.function
def retention_ratio(h_tw, d_b, h2):
    '''
    Task 3: retention ratio of the basin [-].

    Parameters
    ----------
    h_tw : tailwater depth in the downstream reach [m]
    d_b  : depth of the basin floor below the downstream bed [m]
    h2   : conjugate depth required by the jump [m]
    '''
    # >>> YOUR CODE HERE
    raise NotImplementedError("Task 3: return the retention ratio")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Given: basin and scour-protection lengths

    To empirically derive the required stilling basin length $l_b$, [Peterka (USBR Engineering Monograph 25)](https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB95139457.xhtml) measured the length of the jump in six test flumes and plotted it against the Froude number as a ready reckoner (his Figure 7, free jump on a horizontal apron). The curve gives a factor (here: $f_l$), which is read off at the Froude number of cross section 1 ($Fr_1$) and multiplied by the conjugate depth ($h_2$):

    | $Fr_1$ | 2.4 | 4 | 5 | 6 to 11 | 14 |
    |---|---|---|---|---|---|
    | $f_{l}$ | 4.8 | 5.8 | 6.0 | 6.13 | 6.0 |

    The function `peterka_f` below reads that table (no intervention needed) and returns $f_{l}$. It fits nothing: `np.interp` interpolates linearly between the tabulated points of a measured curve, and that curve is not a straight line.
    """)
    return


@app.cell
def _(np):
    def peterka_f(Fr1):
        '''Given: basin-length multiplier after Peterka (USBR EM 25), interpolated [-].'''
        knots_Fr = [2.4, 4.0, 5.0, 6.0, 11.0, 14.0]
        knots_f = [4.8, 5.8, 6.0, 6.13, 6.13, 6.0]
        return float(np.interp(Fr1, knots_Fr, knots_f))


    print(f"f_l at Fr1 = 5.0 : {peterka_f(5.0):.3f}")
    print(f"f_l at Fr1 = 8.0 : {peterka_f(8.0):.3f}")
    return (peterka_f,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, calculate the required basin length $l_b$ to contain the jump with the `peterka_f` function. Because the flow leaving the jump (and the basin end sill) is still turbulent, the riverbed immediately downstream of the basin has to be armoured over a length $l_s$:

    $$l_b = f_{l}(Fr_1) h_2, \qquad l_s = 3.5 l_b$$

    Both lengths are coded below, `basin_lengths` calling `peterka_f` for the multiplier.
    """)
    return


@app.cell
def _(peterka_f):
    def basin_lengths(h2, Fr1):
        '''
        Given: basin length and scour-protection length [m].

        Parameters
        ----------
        h2  : conjugate depth downstream of the jump [m]
        Fr1 : Froude number at section 1, which selects the multiplier [-]

        Returns
        -------
        (l_b, l_s) : basin length and scour-protection length [m]
        '''
        l_b = peterka_f(Fr1) * h2
        return l_b, 3.5 * l_b

    return (basin_lengths,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** For a steady jump, $l_b$ is close to the rule of thumb $l_j \approx$ 6 $h_2$, and the cells in this notebook print both $l_j$ and $l_b$. Yet, other design manuals would give different factors, which is one of the reasons why a detailed design with a physical or numerical model is critical.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Self-check

    Run this cell after completing each task. The reference values are the approximate results presented in the lecture slides, so `[OK]` on every line indicates that the three tasks reproduce the slides.
    """)
    return


@app.cell
def _(froude_number):
    CHECKS = [
        ("Task 1  froude_number(31.623, 2.5298)",
         lambda: froude_number(31.623, 2.5298), (6.348,), "-"),
        ("Task 2  conjugate_depth(2.5298, 6.348)",
         lambda: conjugate_depth(2.5298, 6.348), (21.481,), "m"),
        ("Task 3  retention_ratio(19.060, 3.5, 21.481)",
         lambda: retention_ratio(19.060, 3.5, 21.481), (1.050,), "-"),
    ]


    def check_tasks(tolerance=5e-3, verbose=True):
        '''Compare each task against the worked values from the lecture.'''
        passed = 0
        for label, call, expected, unit in CHECKS:
            try:
                value = call()
            except NotImplementedError:
                if verbose:
                    print(f"[ ] {label:<46} not implemented yet")
                continue
            got = value if isinstance(value, tuple) else (value,)
            ok = (len(got) == len(expected) and
                  all(abs(g - e) <= tolerance * max(1.0, abs(e))
                      for g, e in zip(got, expected)))
            passed += ok
            if verbose:
                mark = "OK" if ok else "XX"
                shown = ", ".join(f"{g:.3f}" for g in got)
                wanted = ", ".join(f"{e:.3f}" for e in expected)
                print(f"[{mark}] {label:<46} {shown:>19} {unit:<3}"
                      f" (expected {wanted})")
        if verbose:
            print("-" * 78)
            print(f"{passed} of {len(CHECKS)} tasks correct.")
        return passed == len(CHECKS)


    TASKS_DONE = check_tasks()
    return (TASKS_DONE,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Workflow implementation: the search over the basin depth

    **The remainder of Part II calculations is given (the follow-up question answers are not).**

    The function `basin_state` evaluates one trial basin depth end to end and calls the functions written above; `search_basin_depth` chooses the trial depths, adjusting $\mathbf{d_b}$ by bisection until it has found the **shallowest** depth at which both engineering objectives are met. The bisection logic should be read before the cell is run.

    $Fr_1$ and $r_{\mathrm{t}}$ increase with $\mathbf{d_b}$, which is what allows one to use a single bracket for both tests: too shallow a basin does not supply the depth the jump demands and sweeps it downstream, but too deep a basin supplies more than the jump requires and drowns it. Each failed trial therefore indicates which half of the bracket to retain, and in the present case the search fails in both directions before converging.

    > **Observe:** The search workflow starts from a first trial of $\mathbf{d_b}$ = 1.0 m. That trial satisfies the steady-jump window, $Fr_1$ = 6.1 already being a steady jump, and fails the retention window, the jump being swept out. The bisection then deepens the basin to 10.5 m, which drowns the jump, and works back down. An acceptable depth is not the end of the search: because a deeper basin costs excavation for no benefit, the bracket keeps closing until the **shallowest** acceptable depth is found, and that value is rounded up to the next 0.25 m for a constructible figure. The result still depends on the width of the bracket, so a report should state which bracket produced it.
    """)
    return


@app.cell
def _(DESIGN, G, brentq, dataclass, energy_head, froude_number):
    FR_WINDOW = (4.5, 9.0)     # steady-jump range
    RT_WINDOW = (1.05, 1.15)   # retention window


    @dataclass(frozen=True)
    class BasinState:
        d_b: float     # trial basin depth [m]
        H: float       # energy head above the basin floor [m]
        h1: float      # supercritical entry depth [m]
        v1: float      # entry velocity [m/s]
        Fr1: float     # entry Froude number [-]
        h2: float      # conjugate depth [m]
        Rt: float      # retention ratio [-]

        @property
        def fr_ok(self):
            return FR_WINDOW[0] <= self.Fr1 < FR_WINDOW[1]

        @property
        def rt_ok(self):
            return RT_WINDOW[0] <= self.Rt <= RT_WINDOW[1]


    def critical_depth(q, g=G):
        '''Critical depth of a rectangular section [m]; the bracket for the entry depth.'''
        return (q**2 / g)**(1 / 3)


    def entry_depth(H, q):
        '''
        The shallow, supercritical root of energy_head(h, q) = H [m].

        Both roots satisfy the energy equation. The supercritical one lies below the
        critical depth, and it is the branch the spillway delivers, so the bracket is
        closed at the critical depth.
        '''
        return brentq(lambda h: energy_head(h, q) - H, 1e-4, critical_depth(q))


    def basin_state(d_b, design=None):
        '''The workflow evaluated for one trial basin depth d_b.'''
        design = design or DESIGN
        H = design.H0 + d_b                          # head above the basin floor
        h1 = entry_depth(H, design.q)                # supercritical root
        v1 = design.q / h1                           # continuity
        Fr1 = froude_number(v1, h1)                  # Task 1
        h2 = conjugate_depth(h1, Fr1)                # Task 2
        Rt = retention_ratio(design.h_tw, d_b, h2)   # Task 3
        return BasinState(d_b=d_b, H=H, h1=h1, v1=v1, Fr1=Fr1, h2=h2, Rt=Rt)

    return FR_WINDOW, RT_WINDOW, basin_state


@app.cell
def _(FR_WINDOW, RT_WINDOW, TASKS_DONE, basin_state, math):
    def search_basin_depth(db_start=1.0, db_min=0.0, db_max=20.0, max_iter=25,
                           tol=0.005, grid=0.25, verbose=True):
        '''
        Bisection on the basin depth d_b for the SHALLOWEST depth at which both
        engineering objectives are met, rounded up to the next `grid` metres.

        Returns the accepted BasinState and the full iteration history.
        '''
        d_b = db_start
        history = []
        if verbose:
            print(f"{'iter':>4}{'d_b [m]':>9}{'Fr1':>8}{'h1 [m]':>9}{'h2 [m]':>9}"
                  f"{'Rt':>8}   verdict")
            print("-" * 66)

        for i in range(1, max_iter + 1):
            state = basin_state(d_b)
            history.append(state)
            if verbose:
                flags = []
                if not state.fr_ok:
                    flags.append("Fr1 low" if state.Fr1 < FR_WINDOW[0] else "Fr1 high")
                if not state.rt_ok:
                    flags.append("swept out" if state.Rt < RT_WINDOW[0] else "drowned")
                print(f"{i:>4}{state.d_b:>9.3f}{state.Fr1:>8.2f}{state.h1:>9.4f}"
                      f"{state.h2:>9.4f}{state.Rt:>8.3f}   "
                      f"{'accepted' if not flags else ', '.join(flags)}")

            # A deeper basin raises H, so the entry flow is shallower and faster: Fr1 and Rt increase monotonically with d_b. One bracket therefore serves both criteria, and each verdict says which way to move: a jump that is too gentle or swept out wants a deeper basin, one that is too fierce or drowned wants a shallower one. An acceptable trial is not the end of the search either, because a deeper basin than necessary costs excavation for no benefit, so it too narrows the bracket from above.
            if not state.fr_ok:
                if state.Fr1 < FR_WINDOW[0]:
                    db_min = d_b  # jump too gentle: deepen the basin
                else:
                    db_max = d_b  # jump too fierce: raise the floor
            elif state.Rt < RT_WINDOW[0]:
                db_min = d_b      # swept out: deeper basin
            else:
                db_max = d_b      # accepted or drowned: try a shallower one

            if db_max - db_min < tol:
                break
            d_b = 0.5 * (db_min + db_max)
        else:
            raise RuntimeError("no acceptable basin depth found in the search range")

        # db_max is the shallowest depth known to work; round it up to a buildable one.
        d_b = math.ceil(db_max / grid) * grid
        state = basin_state(d_b)
        history.append(state)
        if not (state.fr_ok and state.rt_ok):
            raise RuntimeError(f"rounding up to {d_b:.2f} m no longer meets the engineering objectives")
        if verbose:
            print(f"{'->':>4}{state.d_b:>9.3f}{state.Fr1:>8.2f}{state.h1:>9.4f}"
                  f"{state.h2:>9.4f}{state.Rt:>8.3f}   shallowest, rounded up")
        return state, history


    if TASKS_DONE:
        DESIGN_STATE, HISTORY = search_basin_depth()
        print(f"\naccepted basin depth d_b = {DESIGN_STATE.d_b:.3f} m")
    else:
        DESIGN_STATE, HISTORY = None, []
        print("Complete Tasks 1 to 3, then re-run this cell.")
    return (DESIGN_STATE,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Head loss across the jump

    The head loss quantifies the work the basin performs. This is not a task: the design decision has already been taken by the two engineering objectives above. The loss is computed here because it is the reason the basin exists. Combining the energy equation with the conjugate-depth relation on a horizontal bed gives the head loss in closed form,

    $$\Delta H = H_1 - H_2 = \frac{(h_2 - h_1)^3}{4 h_1 h_2} > 0$$

    $\Delta H$ is a loss of head rather than of energy: it represents the irreversible conversion of mean-flow mechanical energy into turbulence and ultimately into internal energy, the total energy being conserved throughout.
    """)
    return


@app.cell
def _(DESIGN, DESIGN_STATE, TASKS_DONE, energy_head):
    def head_loss(h1, h2):
        '''Given: head loss across the jump [m].'''
        return (h2 - h1)**3 / (4 * h1 * h2)


    if TASKS_DONE:
        delta_H = head_loss(DESIGN_STATE.h1, DESIGN_STATE.h2)
        H1 = energy_head(DESIGN_STATE.h1, DESIGN.q)

        print(f"head loss           dH        = {delta_H:8.3f} m")
        print(f"energy head at 1    H1        = {H1:8.3f} m")
        print(f"relative loss       dH / H1   = {delta_H / H1:8.1%}")
    else:
        delta_H = H1 = None
        print("Complete Tasks 1 to 3, then re-run this cell.")
    return H1, delta_H


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basin length and scour protection

    The given `basin_lengths`, evaluated at the accepted design, alongside the rule of thumb ($l_j \approx$ 6 $h_2$) against which the basin length can be checked.
    """)
    return


@app.cell
def _(DESIGN_STATE, TASKS_DONE, basin_lengths, peterka_f):
    if TASKS_DONE:
        f_peterka = peterka_f(DESIGN_STATE.Fr1)
        l_b, l_s = basin_lengths(DESIGN_STATE.h2, DESIGN_STATE.Fr1)

        print(f"Peterka multiplier  f_l  = {f_peterka:7.2f}  (at Fr1 = {DESIGN_STATE.Fr1:.2f})")
        print(f"basin length        l_b  = {l_b:7.2f} m   <- given")
        print(f"rule of thumb     6 h_2  = {6 * DESIGN_STATE.h2:7.2f} m"
              f"   ({abs(6 * DESIGN_STATE.h2 / l_b - 1):.1%} from l_b)")
        print(f"scour protection    l_s  = {l_s:7.2f} m   <- given")
    else:
        f_peterka = l_b = l_s = None
        print("Complete Tasks 1 to 3, then re-run this cell.")
    return l_b, l_s


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Result evaluation plots

    ### Engineering objective check

    The two engineering objectives are here graphically evaluated as a function of the basin depth $\mathbf{d_b}$. The shaded bands in the plots are the objectives and the dashed vertical line is the accepted design. Only one criterion is decisive: $Fr_1$ stays inside its band across all tests, but $r_{\mathrm{t}}$ enters its band and leaves it again within about 2.5 m of basin depth, between 6.79 m and 9.31 m. The retention criterion therefore selects $\mathbf{d_b}$, and it is the criterion that depends on the given tailwater depth $h_{tw}$.
    """)
    return


@app.cell
def _(
    BLUE,
    CYAN,
    DESIGN_STATE,
    FR_WINDOW,
    GREY,
    RT_WINDOW,
    TASKS_DONE,
    WARN,
    basin_state,
    np,
    plt,
):
    if TASKS_DONE:
        db_range = np.linspace(0.2, 20.0, 240)
        states = [basin_state(float(x)) for x in db_range]
        Fr_curve = np.array([s.Fr1 for s in states])
        Rt_curve = np.array([s.Rt for s in states])
        _fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6), sharex=True)
        axes[0].axhspan(*FR_WINDOW, color=CYAN, alpha=0.18, lw=0)
        axes[0].plot(db_range, Fr_curve, color=BLUE, lw=2.2)
        axes[0].set_ylabel('$Fr_1$ at the basin entrance [-]')
        axes[0].set_title('Steady-jump window')
        axes[0].set_ylim(4.3, 9.3)
        axes[0].annotate('steady jump\n$4.5 \\leq Fr_1 < 9$', (0.8, 8.4), color=BLUE, fontsize=8.5)
        axes[1].axhspan(Rt_curve.min(), RT_WINDOW[0], color=WARN, alpha=0.1, lw=0)
        axes[1].axhspan(*RT_WINDOW, color=CYAN, alpha=0.18, lw=0)
        axes[1].axhspan(RT_WINDOW[1], Rt_curve.max(), color=GREY, alpha=0.1, lw=0)
        axes[1].axhline(1.0, color=GREY, lw=0.8, ls=':')
        axes[1].plot(db_range, Rt_curve, color=BLUE, lw=2.2)
        axes[1].set_ylabel('retention ratio $r_\\mathrm{t}$ [-]')
        axes[1].set_title('Retention window')
        axes[1].set_ylim(Rt_curve.min(), Rt_curve.max())
        axes[1].annotate('jump swept out', (4.2, 0.83), color=WARN, fontsize=8.5)
        axes[1].annotate('retained', (0.8, 1.09), color=BLUE, fontsize=8.5)
        axes[1].annotate('jump drowned', (0.8, 1.42), color=GREY, fontsize=8.5)
        for _ax in axes:
            _ax.axvline(DESIGN_STATE.d_b, color=WARN, lw=1.4, ls='--')
            _ax.set_xlabel('basin depth $\\mathbf{d_b}$ [m]', color=WARN)
            _ax.set_xlim(0.2, 20.0)
        axes[0].plot([DESIGN_STATE.d_b], [DESIGN_STATE.Fr1], 'o', color=WARN, ms=6, zorder=3)
        axes[1].plot([DESIGN_STATE.d_b], [DESIGN_STATE.Rt], 'o', color=WARN, ms=6, zorder=3)
        axes[0].annotate(f'design\n$\\mathbf{{d_b}} = {DESIGN_STATE.d_b:.2f}$ m,  $Fr_1 = {DESIGN_STATE.Fr1:.2f}$', (DESIGN_STATE.d_b, DESIGN_STATE.Fr1), textcoords='offset points', xytext=(-104, 34), color=WARN, fontsize=8.5, arrowprops=dict(arrowstyle='-', color=WARN, lw=0.8))
        axes[1].annotate(f'$r_\\mathrm{{t}} = {DESIGN_STATE.Rt:.3f}$', (DESIGN_STATE.d_b, DESIGN_STATE.Rt), textcoords='offset points', xytext=(40, -58), color=WARN, fontsize=8.5, arrowprops=dict(arrowstyle='-', color=WARN, lw=0.8))  # the design variable is the one symbol set apart from the notation:
        _fig.tight_layout()  # bold and in the warn colour, on the slides and here alike
        plt.show()
    else:
        print('Complete Tasks 1 to 3, then re-run this cell.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Longitudinal section of the stilling basin

    The accepted design is drawn in the following code block to scale, with the downstream riverbed as the datum. Two depths are marked above the stilling basin floor, and the difference between them is the subject of the retention check:

    * **Available** is the depth supplied by the tailwater and the basin depth, $h_{tw} + \mathbf{d_b}$.
    * **Required** is the depth required for the jump, that is the conjugate depth $h_2$.

    Their ratio is $r_{\mathrm{t}}$, and the surplus is the margin by which the jump is retained within the basin rather than on the bed downstream. Only the end depths of the jump follow from the 1d relations, so the surface drawn between cross sections 1 and 2 is indicative.
    """)
    return


@app.cell
def _(
    BLUE,
    CYAN,
    DESIGN,
    DESIGN_STATE,
    GREY,
    NAVY,
    TASKS_DONE,
    WARN,
    l_b,
    math,
    np,
    pe,
    plt,
):
    if TASKS_DONE:
        _s = DESIGN_STATE
        floor = -_s.d_b  # basin floor, below the downstream riverbed
        h_avail = DESIGN.h_tw + _s.d_b  # depth available over the floor
        h_need = floor + _s.h2  # level the jump demands, above the datum
        top = DESIGN.H0  # energy head above the un-sunk invert
        u = l_b / 24.8  # one drawing unit, so the layout scales
        x_face, x_toe, x_end = (-7.0 * u, 0.0, l_b)
        x_tail = x_end + 0.6 * l_b
        x_j0, x_j1 = (0.26 * l_b, 0.62 * l_b)
        glow = [pe.withStroke(linewidth=2.6, foreground='white')]
        _fig, _ax = plt.subplots(figsize=(9.4, 3.4))
        _ax.plot([x_face - 2.0 * u, x_face, x_face + 3.2 * u, x_toe, x_end, x_end, x_tail], [top, top, top, floor, floor, 0.0, 0.0], color=NAVY, lw=2.4, solid_joinstyle='round')  # every label gets a white glow, so that one crossing a line stays readable
        xs = np.linspace(x_toe, x_tail, 500)
        bed = np.where(xs <= x_end, floor, 0.0)
        ramp = np.clip((xs - x_j0) / (x_j1 - x_j0), 0.0, 1.0)
        surface = floor + _s.h1 + (DESIGN.h_tw - floor - _s.h1) * (0.5 - 0.5 * np.cos(math.pi * ramp))
        surface = surface + 0.04 * (DESIGN.h_tw - floor - _s.h1) * np.exp(-((xs - x_j1) / (0.09 * l_b)) ** 2)  # --- structure and bed ---------------------------------------------------
        _ax.fill_between(xs, surface, bed, color=CYAN, alpha=0.3, lw=0)  # the chute face descends from the spillway crest to the basin floor,
        _ax.plot(xs, surface, color=BLUE, lw=2.0)  # then the floor runs to the end sill and the river bed continues downstream

        def dim(x, y0, y1, label, colour=NAVY, dx=0.7 * u, ha='left', frac=0.5, outside=False, ext=0.4 * u):
            """
            A dimension between two levels, with a tick at each end so that what it
            measures from and to is unambiguous. outside=True puts the two heads  # --- water body ----------------------------------------------------------
            beyond the span, pointing in, for a span too short to hold them.
            """
            for y in (y0, y1):
                _ax.plot([x - 0.5 * u, x + 0.5 * u], [y, y], color=colour, lw=0.8)
            if outside:
                _ax.annotate('', (x, y0), (x, y0 - ext), arrowprops=dict(arrowstyle='->', color=colour, lw=1.1))  # a small crest at the end of the jump, so that the roller reads as a roller
                _ax.annotate('', (x, y1), (x, y1 + ext), arrowprops=dict(arrowstyle='->', color=colour, lw=1.1))  # rather than as a smooth asymptote; it is schematic, like the ramp itself
            else:
                _ax.annotate('', (x, y0), (x, y1), arrowprops=dict(arrowstyle='<->', color=colour, lw=1.1))
            if label:
                _ax.text(x + dx, y0 + frac * (y1 - y0), label, color=colour, fontsize=8.2, va='center', ha=ha, path_effects=glow)
        _ax.plot([0.48 * x_end, x_end + 6.0 * u], [h_need] * 2, color=WARN, lw=1.0, ls='--')
        dim(0.5 * x_end, floor, h_need, f'required\n$h_2 \\approx {_s.h2:.1f}$ m', colour=WARN, dx=-0.7 * u, ha='right', frac=0.86)
        dim(0.86 * x_end, floor, DESIGN.h_tw, f'available\n$h_{{tw}}+\\mathbf{{d_b}} \\approx {h_avail:.1f}$ m', dx=-0.7 * u, ha='right')  # --- dimensions ----------------------------------------------------------
        x_gap = x_end + 4.6 * u
        dim(x_gap, h_need, DESIGN.h_tw, '', colour=WARN, outside=True)
        _ax.annotate(f'surplus $\\approx {h_avail - _s.h2:.1f}$ m\n(water above the level $h_2$ demands)', (x_gap, DESIGN.h_tw + 0.6 * u), textcoords='offset points', xytext=(0, 32), color=WARN, fontsize=8.2, ha='center', arrowprops=dict(arrowstyle='->', color=WARN, lw=0.9), path_effects=glow)
        _ax.annotate(f'$h_1 \\approx {_s.h1:.1f}$ m', (x_toe + 3.2 * u, floor + 0.5 * _s.h1), textcoords='offset points', xytext=(2, 54), color=NAVY, fontsize=8.2, arrowprops=dict(arrowstyle='->', color=NAVY, lw=0.9), path_effects=glow)
        dim(x_end + 2.4 * u, floor, 0.0, f'$\\mathbf{{d_b}} \\approx {_s.d_b:.1f}$ m', colour=WARN, outside=True, ext=0.8 * u, dx=1.2 * u)
        dim(x_end + 9.0 * u, 0.0, DESIGN.h_tw, f'$h_{{tw}} \\approx {DESIGN.h_tw:.1f}$ m')
        _ax.annotate('', (x_toe, floor - 0.365 * _s.h2), (x_end, floor - 0.365 * _s.h2), arrowprops=dict(arrowstyle='<->', color=NAVY, lw=1.1))
        _ax.text(0.5 * x_end, floor - 0.62 * _s.h2, f'basin length $l_b \\approx {l_b:.1f}$ m', color=NAVY, fontsize=8.2, ha='center', path_effects=glow)
        _ax.axhline(0.0, color=GREY, lw=0.7, ls=':')
        x_jump = x_j1
        y_jump = float(np.interp(x_jump, xs, surface))
        _ax.text(x_jump, y_jump + 1.75 * u, 'hydraulic jump', color=NAVY, fontsize=9, ha='center', style='italic', path_effects=glow)
        _ax.annotate('', (x_jump, y_jump + 0.25 * u), (x_jump, y_jump + 1.45 * u), arrowprops=dict(arrowstyle='->', color=NAVY, lw=0.9))
        _ax.text(x_face - 1.6 * u, top + 0.12 * _s.h2, f'from the spillway chute,  $H_0 \\approx {top:.1f}$ m', color=NAVY, fontsize=8.2, path_effects=glow)
        _ax.set_xlim(x_face - 2.5 * u, x_tail + 1.0 * u)
        _ax.set_ylim(floor - 0.75 * _s.h2, top + 0.55 * _s.h2)
        _ax.set_aspect('equal')
        _ax.set_xlabel('distance along the basin [m]')
        _ax.set_ylabel('level above the\ndownstream bed [m]')
        _ax.spines['left'].set_visible(True)
        _fig.tight_layout()
        plt.show()  # the level the jump demands, carried downstream so that it can be compared
    else:  # with the water surface; it starts right of the jump arrow, never under it
        print('Complete Tasks 1 to 3, then re-run this cell.')  # the surplus is 1.1 m on a 22 m bar, so it is named rather than left to the eye  # --- labels --------------------------------------------------------------  # the arrow points at the crest of the roller, and stays above the dashed  # level line so that it can cross neither that line nor the "required" label
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Design summary
    """)
    return


@app.cell
def _(
    DESIGN,
    DESIGN_STATE,
    FR_WINDOW,
    H1,
    RT_WINDOW,
    TASKS_DONE,
    delta_H,
    l_b,
    l_s,
):
    if TASKS_DONE:
        _s = DESIGN_STATE
        rows = [('given', 'spillway design flow', 'Q', DESIGN.Q, 'm3/s'), ('given', 'unit discharge', 'q', DESIGN.q, 'm2/s'), ('given', 'energy head above the invert', 'H0', DESIGN.H0, 'm'), ('given', 'tailwater depth', 'h_tw', DESIGN.h_tw, 'm'), ('design', 'basin depth', 'd_b', _s.d_b, 'm'), ('design', 'energy head above the floor', 'H', _s.H, 'm'), ('design', 'entry depth', 'h1', _s.h1, 'm'), ('design', 'entry velocity', 'v1', _s.v1, 'm/s'), ('design', 'entry Froude number', 'Fr1', _s.Fr1, '-'), ('design', 'conjugate depth', 'h2', _s.h2, 'm'), ('design', 'retention ratio', 'Rt', _s.Rt, '-'), ('result', 'head loss', 'dH', delta_H, 'm'), ('result', 'relative head loss', 'dH/H1', 100 * delta_H / H1, '%'), ('result', 'basin length', 'l_b', l_b, 'm'), ('result', 'scour protection length', 'l_s', l_s, 'm')]
        print(f"{'':8}{'quantity':<34}{'symbol':<14}{'value':>10}  unit")
        group = None
        for kind, name, symbol, value, unit in rows:
            if kind != group:
                print('-' * 70)
                group = kind
            print(f'{kind:<8}{name:<34}{symbol:<14}{value:>10.3f}  {unit}')
        print('=' * 70)
        print(f"windows: Fr1 in [{FR_WINDOW[0]}, {FR_WINDOW[1]}) -> {('met' if _s.fr_ok else 'NOT met')};  Rt in [{RT_WINDOW[0]}, {RT_WINDOW[1]}] -> {('met' if _s.rt_ok else 'NOT met')}")
    else:
        print('Complete Tasks 1 to 3, then re-run this cell.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Follow-up questions

    Each of the following requires a single change to one input of the code written above, to explore how uncertainties and changes in the boundary conditions act on the hydraulic jump, and therefore on the stilling basin design.

    1. **What happens if the tailwater depth is lower?** Recompute with the tailwater depth reduced by 2 m and everything else unchanged, that is, hand `basin_state` a `DesignData` whose `h_tw` is 2 m smaller. Determine the effect on $r_{\mathrm{t}}$ and its consequence for the downstream riverbed, and identify how the jump position changes.
    2. **How does the jump behave under different discharge scenarios?** The basin is designed for a 500-year flood but operates mostly at much lower discharges. So re-evaluate `basin_state` with a `DesignData` whose `q` is halved, and determine whether the jump remains steady and remains retained.

    # Limits of the simplification

    This calculation template uses simplified 1d equations, and its results are therefore subject to considerable uncertainty, related to (but not limited to):

    * hydrology, that is the derivation of the design flood;
    * the tailwater rating curve, instead of the rectangular Manning idealisation;
    * load and failure scenarios, including floods exceeding the spillway design discharge, partial-gate operation, and the sluice gates beside the spillway;
    * cavitation, air entrainment, uplift, fluctuating pressures and fatigue of the structure;
    * scour and riverbed-stability assessment downstream of the protected length;
    * geotechnical analysis and structural design;
    * fish passage and sediment management.

    # Sources

    * Chanson, *Hydraulics of Open Channel Flow*, 2nd ed., Elsevier Butterworth-Heinemann, 2004.
    * Peterka, *Hydraulic Design of Stilling Basins and Energy Dissipators*, USBR Engineering Monograph 25, revised 1978. <https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/PB95139457.xhtml>
    * Bollrich, *Technische Hydromechanik*, Dresden, Germany, 2000.
    * NZ Ministry of Works and Development, *Clyde Dam: Clutha Power*, 1987, <https://archive.org/details/clyde-dam-clutha-power>.
    """)
    return


if __name__ == "__main__":
    app.run()
