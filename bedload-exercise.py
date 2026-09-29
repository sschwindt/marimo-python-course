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
    # Exercice sur le calcul du charriage

    Pour travailler de manière interactive, installez [Python](https://hydro-informatics.com/python-basics/pyinstall) et [JupyterLab](https://jupyter.org/) en local, ou travaillez dans le navigateur avec [Google Colab](https://colab.research.google.com/github/hydro-informatics/jupyter-python-course/blob/main/bedload-exercise.ipynb). L'exercice comprend trois fichiers qui doivent garder **cette structure de dossiers**. Ne téléchargez pas le fichier zip de ce dépôt (il contient tous les notebooks et toutes les données du cours) : téléchargez les trois fichiers **un par un** (sur GitHub : *Download raw file*).

    | fichier | contenu |
    |---|---|
    | [*bedload-exercise.ipynb*](https://github.com/hydro-informatics/jupyter-python-course/blob/main/bedload-exercise.ipynb) | ce notebook, le seul fichier à modifier |
    | [*fun/charriage.py*](https://github.com/hydro-informatics/jupyter-python-course/blob/main/fun/charriage.py) | le code technique : formule de Meyer-Peter & Müller (MPM), contrôle et figures |
    | [*data/hecras-arbogne.csv*](https://github.com/hydro-informatics/jupyter-python-course/blob/main/data/hecras-arbogne.csv) | l'hydraulique de 16 profils HEC-RAS 1D de l'Arbogne à Dompierre (FR) pour Q = 25 m$^3$/s |

    > **Tâche :** votre expertise est demandée pour analyser le risque d'alluvionnement dans le tronçon revitalisé de l'Arbogne. Un collègue vous a fourni l'hydraulique (1D) de 16 profils sur 890 m. Où le gravier s'arrête-t-il, et que se passe-t-il quand la végétation freine l'écoulement ?

    ## Structure de l'exercice

    | | partie | qui travaille |
    |---|---|---|
    | **I** | préparation : charger le script et les données | **donné** : exécuter les cellules |
    | **II** | données : granulométrie, rugosités $k_{st}$, seuil $\tau_{*,cr}$ | **vous** : compléter deux listes |
    | **III** | équations : rapport de rugosité $k'$ et rugosité critique $k_{st,cr}$ | **vous** : compléter deux lignes de code |
    | **IV** | résultats : calcul MPM, diagramme de Shields, profils actifs | **donné** : exécuter et interpréter |

    Il n'est pas nécessaire de savoir programmer. Une cellule s'exécute avec **Maj + Entrée** (*Shift + Enter*). Les endroits à compléter sont marqués par le commentaire `# >>> À COMPLÉTER` : remplacez chaque texte `">>> COMPLETER"` (guillemets compris) par votre valeur ou votre équation. Dans le code, les nombres décimaux s'écrivent avec un **point** (0.047 et non 0,047).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Partie I : préparation

    La cellule suivante charge le script *fun/charriage.py* sous le nom abrégé `ch` et affiche les données de *data/hecras-arbogne.csv*. Sur Google Colab, elle télécharge d'abord ces deux fichiers. Cette cellule ne contient pas de matière du cours.
    """)
    return


@app.cell
def _():
    import os, sys, urllib.request
    if "google.colab" in sys.modules:  # uniquement sur Google Colab : télécharge le script et les données
        for f in ("fun/charriage.py", "data/hecras-arbogne.csv"):
            os.makedirs(os.path.dirname(f), exist_ok=True)
            urllib.request.urlretrieve(
                f"https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/{f}", f)

    from fun import charriage as ch   # fun/charriage.py, lit data/hecras-arbogne.csv
    ch.lire_hecras()
    return (ch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le tableau affiche, pour chaque profil (de l'amont vers l'aval), la station, le débit, les cotes du fond et de l'eau, la pente de la ligne d'énergie $J_e$, le rayon hydraulique $R_h$ et la hauteur d'eau $h$. La pente $J_e$ passe de 0,0042 à l'amont à 0,0007 à l'aval : c'est là que le gravier risque de se déposer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Partie II : données

    ## Tâche 1 : granulométrie et rugosité

    Deux courbes granulométriques décrivent l'Arbogne (analyse en ligne selon Fehr, mars 2014) :

    - **« Sable (fin) »** pour estimer l'**apport** de l'amont ;
    - **« Gravier (complet) »** pour caractériser le **lit** en place.

    Quatre diamètres caractéristiques suffisent pour l'exercice :

    | courbe granulométrique | $d_m$ [mm] | $d_{84}$ [mm] | $d_{90}$ [mm] |
    |---|---|---|---|
    | « Sable (fin) » | 0,23 | pas nécessaire | pas nécessaire |
    | « Gravier (complet) » | 8,88 | 13,56 | 23,06 |

    - $d_m$ du sable représente l'apport fin qui transite ;
    - $d_m$ du gravier représente le gravier en transit ;
    - $d_{84}$ du gravier représente le lit en place (pavage) ;
    - $d_{90}$ du gravier fixe la rugosité de grain $k_r$ (Meyer-Peter & Müller 1948).

    Reportez ces valeurs, **en millimètres**, dans la liste `melanges`. Attention : en Python, la virgule décimale devient un **point** (0,23 s'écrit `0.23`). L'ordre compte : d'abord le sable, puis le gravier (le dernier mélange de la liste représente le lit).

    Reportez ensuite dans la liste `k_st` les deux coefficients de Strickler $k_{st}$ [m$^{1/3}$/s] à comparer, du plus lisse au plus rugueux :

    1. **sans végétation** : l'écoulement reste dans le lit en gravier (état de référence) ;
    2. **avec végétation** : la crue déborde dans la plaine inondable, densément végétalisée.

    La liste peut contenir d'autres valeurs : chaque $k_{st}$ ajouté devient un cas de rugosité supplémentaire.
    """)
    return


@app.cell
def _():
    # >>> À COMPLÉTER : diamètres caractéristiques en mm
    #             nom                   d_m               d_84              d_90
    melanges = [["Sable (fin)",         ">>> COMPLETER"],
                ["Gravier (complet)",   ">>> COMPLETER",  ">>> COMPLETER",  ">>> COMPLETER"]]

    # >>> À COMPLÉTER : coefficients de Strickler k_st [m^(1/3)/s], sans végétation en premier
    k_st = [">>> COMPLETER", ">>> COMPLETER"]
    return k_st, melanges


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Seuil de mise en mouvement $\tau_{*,cr}$

    MPM a été calibré avec $\tau_{*,cr}$ = 0,047, valeur utilisée dans tout l'exercice. La liste `tau_cr` accepte toutefois plusieurs valeurs, par exemple pour tester la sensibilité du résultat au seuil (voir le devoir). Pour cela, supprimez le `#` devant la deuxième ligne : chaque figure affiche alors toutes les valeurs de la liste.

    > **Note :** $\tau_{*,cr}$ ne se mesure pas. On le choisit dans une plage (environ 0,03 à 0,07 pour du gravier) et on l'annonce avec le résultat.
    """)
    return


@app.cell
def _():
    tau_cr = [0.047]
    # tau_cr = [0.030, 0.040, 0.047, 0.056, 0.070]   # variante, pas utilisée dans l'exercice
    return (tau_cr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Partie III : équations

    ## Tâche 2 : rapport de rugosité $k'$

    MPM ne compare pas au seuil toute la contrainte de cisaillement $\tau_*$, mais seulement la part qui agit sur les grains. Une partie de l'énergie est dissipée par les formes du lit, la végétation et les berges. Le rapport de rugosité $k'$ corrige $\tau_*$ en conséquence :

    $$\Phi = 8\,\left(k'\,\tau_* - \tau_{*,cr}\right)^{3/2} \qquad \text{avec} \qquad \tau_* = \frac{R_h\,J_e}{(s-1)\,d}$$

    $$\boxed{\;k' = \left(\frac{k_{st}}{k_r}\right)^{3/2} \le 1\;} \qquad \text{où} \qquad k_r = \frac{26}{d_{90}^{1/6}}$$

    - $k_{st}$ : coefficient de Strickler **total** du tronçon (la liste `k_st` de la tâche 1) ;
    - $k_r$ : coefficient de Strickler **de grain** d'un lit plat, calculé par *charriage.py* avec $d_{90}$ du gravier en mètres.

    Complétez la ligne marquée. En Python, la puissance s'écrit `**` : par exemple, $a^{3/2}$ s'écrit `a ** (3 / 2)`.
    """)
    return


@app.function
def rapport_rugosite(k_st, k_r):
    # >>> À COMPLÉTER : k' = (k_st / k_r)^(3/2)
    return ">>> COMPLETER"


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tâche 3 : rugosité critique $k_{st,cr}$

    Plus la végétation freine l'écoulement, plus $k_{st}$ diminue, et avec lui la contrainte efficace $k'\,\tau_*$. Un profil cesse de transporter quand $k'\,\tau_* = \tau_{*,cr}$. En remplaçant $k'$ par sa définition et en résolvant pour $k_{st}$, on obtient la rugosité critique de chaque profil :

    $$\boxed{\;k_{st,cr} = k_r \left(\frac{\tau_{*,cr}}{\tau_*}\right)^{2/3}\;}$$

    Un profil transporte tant que $k_{st} > k_{st,cr}$. C'est cette équation qui permet de tracer le nombre de profils actifs quand la rugosité augmente (dernière figure). Complétez la ligne marquée.
    """)
    return


@app.function
def k_st_critique(tau, k_r, tau_cr):
    # >>> À COMPLÉTER : k_st,cr = k_r * (tau_cr / tau)^(2/3)
    return ">>> COMPLETER"


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Contrôle

    Exécutez cette cellule après chaque tâche. `[OK]` signifie que la valeur correspond à la présentation, `[XX]` qu'elle est fausse, `[  ]` qu'elle n'est pas encore complétée. Corrigez puis ré-exécutez la cellule de la tâche **et** celle-ci.
    """)
    return


@app.cell
def _(ch, k_st, melanges):
    ch.verifier(melanges, k_st, rapport_rugosite, k_st_critique)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Partie IV : résultats

    ## Calcul MPM sur les 16 profils

    *charriage.py* croise vos données et applique MPM à chaque profil : chaque cas de rugosité de la liste `k_st` est calculé pour les deux classes de grain.

    | grain | ce qu'il représente | cas de rugosité |
    |---|---|---|
    | gravier, $d_m$ | le gravier en transit | sans et avec végétation |
    | sable, $d_m$ | l'apport fin de l'amont | sans et avec végétation |
    | gravier, $d_{84}$ | le lit en place, pavé | sans végétation seulement |

    Le tableau résume, pour chaque combinaison, le rapport de rugosité $k'$, le nombre de profils qui transportent encore ($\Phi > 0$), ainsi que le plus grand $\Phi$ et le plus grand charriage $q_b$ [kg/(s$\cdot$m)] du tronçon.
    """)
    return


@app.cell
def _(ch, k_st, melanges, tau_cr):
    resultats = ch.calculer(melanges, k_st, tau_cr, rapport_rugosite)
    ch.resume(resultats)
    return (resultats,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Question :** pourquoi $\Phi$ = 0 sur certains profils ? Et pourquoi le sable est-il transporté partout ?

    ## Diagramme de Shields

    Le diagramme compare les deux cas de rugosité, **sans végétation** (écoulement dans le lit) et **avec végétation** (crue débordante dans la plaine inondable), pour les deux classes de grain, **gravier et sable**. Chaque point est un profil. L'axe vertical est la contrainte efficace sur les grains $k'\,\tau_*$, celle que MPM compare à $\tau_{*,cr}$. Sous la courbe de Shields critique, il n'y a pas de charriage.

    - **couleur** : cas de rugosité (bleu sans végétation, rouge avec végétation) ;
    - **symbole** : classe de grain (rond : gravier ; triangle : sable) ;
    - **taille** : $\Phi$, une décade par classe (le plus grand $\Phi$ donne le plus grand marqueur).
    """)
    return


@app.cell
def _(ch, resultats):
    ch.diagramme_shields(resultats)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note :** avec $d_m$ = 0,23 mm, le sable est hors du domaine de validité de MPM (environ 0,4 à 30 mm). Son résultat n'est qu'un ordre de grandeur.

    > **Questions :** la végétation déplace-t-elle le gravier et le sable de la même manière ? Pour quelle classe de grain la végétation fait-elle passer les points sous la courbe ?

    ## Profils actifs quand la rugosité augmente

    La figure suivante fait diminuer $k_{st}$ pas à pas (de gauche à droite, la végétation augmente) et compte, pour le gravier, les profils où $k_{st} > k_{st,cr}$. Les lignes verticales sont vos valeurs de la liste `k_st`. L'**extinction totale** est le $k_{st}$ sous lequel plus aucun profil ne transporte.
    """)
    return


@app.cell
def _(ch, k_st, melanges, tau_cr):
    ch.profils_actifs(melanges, k_st, tau_cr, k_st_critique)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Questions :**
    > 1. Entre quelles valeurs de $k_{st}$ le charriage du gravier s'éteint-il complètement ?
    > 2. Alluvionnement ou érosion (ici maintien du chenal de seuil) : lequel des deux paramètres, le grain ou la rugosité, fait basculer le résultat ?
    """)
    return


if __name__ == "__main__":
    app.run()
