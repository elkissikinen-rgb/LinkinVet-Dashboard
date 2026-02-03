# dashboard.py
# LinkinVet — Tableau de bord marché vétérinaire (Canada / Québec)
# Données officielles et vérifiables issues de :
# - CVMA (Economic Impact 2024 Update, 2023-24) : https://www.canadianveterinarians.net/media/jo4hqvwc/cvma_final-report-en.pdf
# - OMVQ (Portrait démographique au 26 septembre 2024) : https://www.omvq.qc.ca/DATA/TEXTEDOC/2024---Portrait-de-la-profession-veterinaire---Document.pdf

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="LinkinVet — Marché vétérinaire (Canada/Québec)",
    layout="wide",
)

st.title("LinkinVet — Marché vétérinaire (Canada/Québec)")
st.markdown(
    """
Ce tableau de bord présente des **indicateurs de marché** basés sur des **sources publiques officielles**.
Les éléments affichés suivent trois niveaux :

- **Officiel** : chiffres explicitement reportés dans les documents CVMA / OMVQ.
- **Indicateur dérivé** : calcul simple et transparent à partir des chiffres officiels (ex. ratio).
- **Scénario (estimation)** : outil d’exploration basé sur hypothèses ; **non** présenté comme un fait.

L’objectif est de fournir une vue synthétique et vérifiable, utilisable en contexte de **présentation à des partenaires financiers**.
"""
)

# -----------------------------
# Données officielles — CVMA (Canada) — Economic Impact 2024 Update (2023-24)
# -----------------------------
# Officiel (CVMA PDF) :
CAN_REGISTERED_VETS_2024 = 16317  # "registered veterinarians"
CAN_ACTIVE_VETS_2023_24 = 15278   # "actively-practicing veterinarians"
CAN_ACCREDITED_FACILITIES_2023_24 = 4328  # "accredited facilities"

# Officiel (CVMA PDF, Table 1 — Canada, 2023-24) :
CAN_OUTPUT_MCAD = 16946.8
CAN_GDP_MCAD = 9549.3
CAN_EMPLOYMENT_FTE = 81920
CAN_TAX_FED_MCAD = 873.1
CAN_TAX_PROV_MCAD = 797.3
CAN_TAX_MUNI_MCAD = 158.2
CAN_OUTPUT_DIRECT_MCAD = 10044.5
CAN_GDP_DIRECT_MCAD = 5567.6
CAN_EMPLOYMENT_DIRECT_FTE = 51660

# Officiel (CVMA PDF, Figure 1 — Actively practicing veterinarians by province, 2023-24)
# Provinces/territories: ON QC AB BC SK NS MB NB PE NL YK NT
# Valeurs 2023-24 explicitement indiquées dans la figure.
vets_active_2023_24 = {
    "Ontario (ON)": 5386,
    "Québec (QC)": 3212,
    "Alberta (AB)": 2099,
    "Colombie-Britannique (BC)": 2141,
    "Saskatchewan (SK)": 724,
    "Nouvelle-Écosse (NS)": 495,
    "Manitoba (MB)": 458,
    "Nouveau-Brunswick (NB)": 167,
    "Île-du-Prince-Édouard (PE)": 238,
    "Terre-Neuve-et-Labrador (NL)": 158,
    "Yukon (YK)": 34,
    "Territoires du Nord-Ouest (NT)": 4,
}

# Officiel (CVMA PDF, Figure 2 — Accredited veterinary practice facilities by province, 2023-24)
# Note CVMA: changement de modèle d'accréditation en Ontario en 2023 (comparabilité 2022-23 limitée pour ON).
facilities_2023_24 = {
    "Ontario (ON)": 1760,
    "Québec (QC)": 942,
    "Alberta (AB)": 608,
    "Colombie-Britannique (BC)": 688,
    "Saskatchewan (SK)": 135,
    "Nouvelle-Écosse (NS)": 155,
    "Manitoba (MB)": 152,
    "Nouveau-Brunswick (NB)": 92,
    "Île-du-Prince-Édouard (PE)": 25,
    "Terre-Neuve-et-Labrador (NL)": 31,
    "Yukon (YK)": 14,
    "Territoires du Nord-Ouest (NT)": 4,
}

df_ca = pd.DataFrame(
    [{"Juridiction": k, "Vétérinaires actifs (2023-24)": v} for k, v in vets_active_2023_24.items()]
).merge(
    pd.DataFrame([{"Juridiction": k, "Établissements accrédités (2023-24)": v} for k, v in facilities_2023_24.items()]),
    on="Juridiction",
    how="left",
)

# Indicateur dérivé (calcul transparent)
df_ca["Ratio (vétos / établissement) — indicateur dérivé"] = (
    df_ca["Vétérinaires actifs (2023-24)"] / df_ca["Établissements accrédités (2023-24)"]
)

# -----------------------------
# Données officielles — OMVQ (Québec) — Portrait au 26 septembre 2024
# -----------------------------
QC_OMVQ_MEMBERS_TOTAL = 2804  # "membres actifs en sol québécois" (OMVQ)
QC_OMVQ_ACTIVE_STATUS_N = 2381  # "statut actif (85%; n=2 381)" (OMVQ)
QC_OMVQ_FEMALE_N = 2025         # "Féminin 72%; n=2 025" (OMVQ)
QC_OMVQ_MALE_N = 779            # "Masculin 28%; n=779" (OMVQ)

# Officiel (OMVQ — Pratique principale, base: membres OMVQ)
# "Base: les médecins vétérinaires membres de l’OMVQ" : 1 674, 305, 172, ...
qc_practice_main = pd.DataFrame([
    {"Pratique principale": "Animaux de compagnie", "Effectif": 1674},
    {"Pratique principale": "Grands animaux", "Effectif": 305},
    {"Pratique principale": "Santé publique", "Effectif": 172},
    {"Pratique principale": "Services-conseils", "Effectif": 149},
    {"Pratique principale": "Équins", "Effectif": 94},
    {"Pratique principale": "Enseignement", "Effectif": 95},
    {"Pratique principale": "Administration", "Effectif": 76},
    {"Pratique principale": "Petits ruminants", "Effectif": 0},
    {"Pratique principale": "Grandes populations animales", "Effectif": 42},
    {"Pratique principale": "Faune et zoos", "Effectif": 15},
    {"Pratique principale": "Animaux de bassecour", "Effectif": 1},
])
qc_practice_main["Part (%)"] = (qc_practice_main["Effectif"] / QC_OMVQ_MEMBERS_TOTAL * 100).round(1)

# Officiel (OMVQ — constats pour animaux de compagnie)
QC_COMPANION_MONTÉRÉGIE_N = 405  # "Montérégie (24%; n=405)"
QC_COMPANION_MONTRÉAL_N = 352    # "Montréal (21%; n=352)"
QC_COMPANION_ABITIBI_N = 20      # "Abitibi-Témiscamingue (1%; n=20)"
QC_COMPANION_GASPÉSIE_N = 10     # "Gaspésie–Îles-de-la-Madeleine (1%; n=10)"
QC_COMPANION_CÔTE_NORD_N = 9     # "Côte-Nord (1%; n=9)"
QC_COMPANION_NORD_DU_QC_N = 2    # "Nord-du-Québec (<1%; n=2)"

# -----------------------------
# Interface
# -----------------------------
tab_ca, tab_qc, tab_scen, tab_sources = st.tabs([
    "Canada (CVMA)",
    "Québec (OMVQ)",
    "Scénarios (estimation)",
    "Sources (liens)"
])

# -----------------------------
# Canada (CVMA)
# -----------------------------
with tab_ca:
    st.subheader("Canada — Indicateurs nationaux (CVMA, 2023-24)")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vétérinaires enregistrés (2024)", f"{CAN_REGISTERED_VETS_2024:,}".replace(",", " "))
    c2.metric("Vétérinaires actifs (2023-24)", f"{CAN_ACTIVE_VETS_2023_24:,}".replace(",", " "))
    c3.metric("Établissements accrédités (2023-24)", f"{CAN_ACCREDITED_FACILITIES_2023_24:,}".replace(",", " "))
    c4.metric("Ratio (vétos / établissement) — indicateur dérivé", f"{CAN_ACTIVE_VETS_2023_24 / CAN_ACCREDITED_FACILITIES_2023_24:.2f}")

    st.markdown("#### Contribution économique (CVMA, 2023-24 — Canada)")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Production totale (M$ CAD)", f"{CAN_OUTPUT_MCAD:,.1f}".replace(",", " "))
    e2.metric("PIB total (M$ CAD)", f"{CAN_GDP_MCAD:,.1f}".replace(",", " "))
    e3.metric("Emplois (ETP/FTE)", f"{CAN_EMPLOYMENT_FTE:,}".replace(",", " "))
    e4.metric("Recettes fiscales totales (M$ CAD)", f"{(CAN_TAX_FED_MCAD + CAN_TAX_PROV_MCAD + CAN_TAX_MUNI_MCAD):,.1f}".replace(",", " "))

    st.caption(
        "Note méthodologique (CVMA) : l’accréditation en Ontario a changé en 2023, ce qui limite certaines comparaisons historiques. "
        "Les valeurs 2023-24 sont utilisées ici comme instantané."
    )

    st.markdown("#### Répartition provinciale (CVMA, 2023-24)")
    left, right = st.columns(2)

    with left:
        fig = px.bar(
            df_ca.sort_values("Vétérinaires actifs (2023-24)", ascending=False),
            x="Juridiction",
            y="Vétérinaires actifs (2023-24)",
            title="Vétérinaires actifs par juridiction (2023-24)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            df_ca.sort_values("Établissements accrédités (2023-24)", ascending=False),
            x="Juridiction",
            y="Établissements accrédités (2023-24)",
            title="Établissements accrédités par juridiction (2023-24)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Intensité par établissement (indicateur dérivé)")
    fig = px.bar(
        df_ca.sort_values("Ratio (vétos / établissement) — indicateur dérivé", ascending=False),
        x="Juridiction",
        y="Ratio (vétos / établissement) — indicateur dérivé",
        title="Ratio vétérinaires actifs / établissements accrédités (proxy de concentration)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df_ca.sort_values("Vétérinaires actifs (2023-24)", ascending=False),
        use_container_width=True
    )

# -----------------------------
# Québec (OMVQ)
# -----------------------------
with tab_qc:
    st.subheader("Québec — Indicateurs (OMVQ, au 26 septembre 2024)")

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Médecins vétérinaires membres (total)", f"{QC_OMVQ_MEMBERS_TOTAL:,}".replace(",", " "))
    q2.metric("Statut actif (n)", f"{QC_OMVQ_ACTIVE_STATUS_N:,}".replace(",", " "))
    q3.metric("Femmes (n)", f"{QC_OMVQ_FEMALE_N:,}".replace(",", " "))
    q4.metric("Hommes (n)", f"{QC_OMVQ_MALE_N:,}".replace(",", " "))

    st.markdown("#### Pratique principale (OMVQ)")
    left, right = st.columns([2, 1])

    with left:
        fig = px.bar(
            qc_practice_main.sort_values("Effectif", ascending=False),
            x="Pratique principale",
            y="Effectif",
            title="Répartition des pratiques principales (effectifs)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("**Points saillants (officiels)**")
        st.markdown(
            f"""
- Animaux de compagnie : **60%** (**n={qc_practice_main.loc[qc_practice_main['Pratique principale']=='Animaux de compagnie','Effectif'].iloc[0]}**)
- Grands animaux : **11%** (**n={qc_practice_main.loc[qc_practice_main['Pratique principale']=='Grands animaux','Effectif'].iloc[0]}**)
- Santé publique : **6%** (**n={qc_practice_main.loc[qc_practice_main['Pratique principale']=='Santé publique','Effectif'].iloc[0]}**)
"""
        )

    st.dataframe(
        qc_practice_main.sort_values("Effectif", ascending=False),
        use_container_width=True
    )

    st.markdown("#### Répartition régionale — pratique animaux de compagnie (OMVQ, constats)")
    st.markdown(
        f"""
Selon le document OMVQ, la concentration la plus élevée de médecins vétérinaires dont la pratique principale est
**animaux de compagnie** se situe en :
- **Montérégie : 24% (n={QC_COMPANION_MONTÉRÉGIE_N})**
- **Montréal : 21% (n={QC_COMPANION_MONTRÉAL_N})**

Certaines régions éloignées sont signalées comme plus touchées par un manque de médecins vétérinaires
dans ce domaine, notamment :
- Abitibi-Témiscamingue : 1% (n={QC_COMPANION_ABITIBI_N})
- Gaspésie–Îles-de-la-Madeleine : 1% (n={QC_COMPANION_GASPÉSIE_N})
- Côte-Nord : 1% (n={QC_COMPANION_CÔTE_NORD_N})
- Nord-du-Québec : <1% (n={QC_COMPANION_NORD_DU_QC_N})
"""
    )

    st.info(
        "Important : OMVQ mesure les **membres** au Québec (au 26 septembre 2024). "
        "CVMA mesure les **vétérinaires actifs** par juridiction (année 2023-24). "
        "Ces définitions ne sont pas strictement équivalentes, mais elles sont complémentaires."
    )

# -----------------------------
# Scénarios (estimation)
# -----------------------------
with tab_scen:
    st.subheader("Scénarios (estimation) — organisation des établissements")
    st.markdown(
        """
Les sources CVMA/OMVQ utilisées ci-dessus **ne publient pas** une répartition standardisée
du type **« pratique solo » vs « clinique multi-vétérinaires »** au niveau agrégé.

Cette section propose un **outil d’exploration** basé sur un **indicateur dérivé** :
**ratio vétérinaires actifs / établissements accrédités (CVMA, 2023-24)**.

Les résultats affichés ici sont des **estimations conditionnelles** à des hypothèses,
à utiliser pour des scénarios de discussion (et non comme constat).
"""
    )

    juris = st.selectbox("Juridiction (CVMA, 2023-24)", df_ca["Juridiction"].tolist(), index=df_ca["Juridiction"].tolist().index("Québec (QC)"))
    row = df_ca[df_ca["Juridiction"] == juris].iloc[0]
    vets = float(row["Vétérinaires actifs (2023-24)"])
    facs = float(row["Établissements accrédités (2023-24)"])
    ratio = float(row["Ratio (vétos / établissement) — indicateur dérivé"])

    a1, a2, a3 = st.columns(3)
    a1.metric("Vétérinaires actifs (officiel)", f"{int(vets):,}".replace(",", " "))
    a2.metric("Établissements accrédités (officiel)", f"{int(facs):,}".replace(",", " "))
    a3.metric("Ratio (indicateur dérivé)", f"{ratio:.2f}")

    st.markdown("##### Hypothèses de scénario")
    solo_share = st.slider("Part hypothétique d’établissements à vétérinaire unique (%)", min_value=0, max_value=80, value=20, step=5)
    solo_facilities = facs * (solo_share / 100.0)
    multi_facilities = facs - solo_facilities

    # Hypothèse explicite : 1 vétérinaire actif par établissement "solo"
    solo_vets_est = solo_facilities * 1.0
    multi_vets_est = max(vets - solo_vets_est, 0)

    s1, s2, s3 = st.columns(3)
    s1.metric("Établissements 'solo' (estim.)", f"{solo_facilities:.0f}")
    s2.metric("Vétérinaires 'solo' (estim.)", f"{solo_vets_est:.0f}")
    s3.metric("Vétérinaires en structure multi (estim.)", f"{multi_vets_est:.0f}")

    st.caption(
        "Transparence : ce module n’infère pas une réalité observée. Il applique des hypothèses paramétrables "
        "à des agrégats officiels (CVMA)."
    )

# -----------------------------
# Sources (liens)
# -----------------------------
with tab_sources:
    st.subheader("Sources (liens officiels)")

    st.markdown(
        """
**1) CVMA — Economic Impact 2024 Update (rapport PDF, 2023-24)**  
- Document complet (PDF) : https://www.canadianveterinarians.net/media/jo4hqvwc/cvma_final-report-en.pdf  
Ce rapport contient notamment :
- 15 278 vétérinaires actifs et 4 328 établissements accrédités (2023-24)
- répartition par province (figures)
- impacts économiques (tables : production/PIB/emplois/recettes fiscales)

**2) CVMA — Economic Impact Study 2024 Update (page de synthèse)**  
- https://www.canadianveterinarians.net/about-cvma/latest-news/economic-impact-study-2024-update/

**3) OMVQ — Portrait démographique de la profession vétérinaire au Québec (au 26 septembre 2024)**  
- Document complet (PDF) : https://www.omvq.qc.ca/DATA/TEXTEDOC/2024---Portrait-de-la-profession-veterinaire---Document.pdf  
Ce document contient notamment :
- 2 804 membres au Québec
- répartition par pratique principale (effectifs)
- constats régionaux (ex. animaux de compagnie)
"""
    )

    st.markdown("---")
    st.markdown("### Méthode (résumé)")
    st.markdown(
        """
- Les chiffres “Officiel” sont copiés **tels quels** des documents CVMA/OMVQ.
- Les “Indicateurs dérivés” sont des **ratios** calculés directement à partir des agrégats officiels.
- Les “Scénarios” sont des **estimations** basées sur hypothèses explicites (paramétrables).
"""
    )
