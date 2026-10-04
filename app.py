import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="TNBC Regulatory State Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# VISUAL STYLE
# ==================================================

st.markdown(
    """
    <style>

    /* Wider sidebar */
    section[data-testid="stSidebar"] {
        width: 330px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 330px !important;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h1 {
        font-size: 30px !important;
        margin-bottom: 24px !important;
    }

    /* Navigation label */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        font-size: 17px !important;
        font-weight: 600 !important;
    }

    /* Navigation options */
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        font-size: 18px !important;
        padding: 10px 4px !important;
        min-height: 48px !important;
        cursor: pointer !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 500 !important;
    }

    /* Main page width */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128, 128, 128, 0.25);
        padding: 18px;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    cell_data = pd.read_csv(
        "app_data/cell_data.csv",
        index_col=0
    )

    regulon_activity = pd.read_csv(
        "app_data/regulon_activity.csv",
        index_col=0
    )

    regulon_summary = pd.read_csv(
        "app_data/regulon_summary.csv",
        index_col=0
    )

    program_loadings = pd.read_csv(
        "app_data/program_loadings.csv",
        index_col=0
    )

    program_regulons = pd.read_csv(
        "app_data/program_regulons.csv"
    )

    program_enrichment = pd.read_csv(
        "app_data/program_enrichment.csv"
    )

    tf_annotations = pd.read_csv(
        "app_data/tf_annotations.csv",
        index_col=0
    )

    return (
        cell_data,
        regulon_activity,
        regulon_summary,
        program_loadings,
        program_regulons,
        program_enrichment,
        tf_annotations
    )


(
    cell_data,
    regulon_activity,
    regulon_summary,
    program_loadings,
    program_regulons,
    program_enrichment,
    tf_annotations
) = load_data()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("TNBC Explorer")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Regulon Explorer",
        "Regulatory Components",
        "Methods & About"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Single-cell regulatory network analysis "
    "of MDA-MB-231 TNBC cells."
)


# ==================================================
# OVERVIEW
# ==================================================

if page == "Overview":

    st.title("TNBC Regulatory State Explorer")

    st.subheader(
        "Mapping transcription-factor regulatory heterogeneity "
        "at single-cell resolution"
    )

    st.write(
        "An interactive framework for exploring transcription-factor "
        "regulatory activity and recurring regulatory patterns in "
        "MDA-MB-231 triple-negative breast cancer cells."
    )

    st.divider()

    # ----------------------------------------------
    # PROJECT AT A GLANCE
    # ----------------------------------------------

    st.subheader("Project at a glance")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Single cells",
        f"{len(cell_data):,}"
    )

    col2.metric(
        "TF regulons",
        f"{regulon_activity.shape[1]}"
    )

    col3.metric(
        "Regulatory components",
        "8"
    )

    st.divider()

    # ----------------------------------------------
    # WHAT THE TOOL DOES
    # ----------------------------------------------

    st.subheader("What this tool does")

    st.write(
        "The explorer moves beyond gene-expression visualization "
        "by representing each cell through inferred transcription-factor "
        "regulon activity. Individual regulons and broader recurring "
        "regulatory components can then be explored across the same "
        "single-cell population."
    )

    st.info(
        "In this dataset, the regulatory-space representation shows "
        "additional branching and localized structure within a largely "
        "continuous expression-space population. These patterns provide "
        "hypotheses about regulatory heterogeneity rather than evidence "
        "for discrete cell types."
    )

    st.divider()

    # ----------------------------------------------
    # EXPRESSION VS REGULATORY
    # ----------------------------------------------

    st.header("Expression vs Regulatory Landscape")

    st.write(
        "Switch between two representations of the same 24,073 cells."
    )

    view = st.radio(
        "Representation",
        [
            "Gene Expression",
            "Regulatory Activity"
        ],
        horizontal=True
    )

    if view == "Gene Expression":

        x = "expr_umap1"
        y = "expr_umap2"

        title = "Gene Expression Landscape"

        x_label = "Expression UMAP 1"
        y_label = "Expression UMAP 2"

    else:

        x = "reg_umap1"
        y = "reg_umap2"

        title = "Regulatory Landscape"

        x_label = "Regulatory UMAP 1"
        y_label = "Regulatory UMAP 2"

    fig_landscape = px.scatter(
        cell_data,
        x=x,
        y=y,
        opacity=0.55,
        render_mode="webgl",
        labels={
            x: x_label,
            y: y_label
        },
        title=title
    )

    fig_landscape.update_traces(
        marker={"size": 3}
    )

    fig_landscape.update_layout(
        height=650
    )

    st.plotly_chart(
        fig_landscape,
        use_container_width=True
    )

    st.caption(
        "Both views contain exactly the same cells. "
        "The geometry changes because the embeddings are constructed "
        "from different feature spaces: gene expression versus "
        "regulon activity. UMAP geometry should not be interpreted "
        "as literal biological distance."
    )


# ==================================================
# REGULON EXPLORER
# ==================================================

elif page == "Regulon Explorer":

    st.title("Regulon Explorer")

    st.write(
        "Select any of the 225 inferred transcription-factor regulons "
        "to explore its activity across the regulatory landscape."
    )

    selected_regulon = st.selectbox(
        "Select a regulon",
        regulon_activity.columns.tolist()
    )

    selected_tf = selected_regulon.replace(
        "(+)",
        ""
    )

    # ----------------------------------------------
    # TF INFORMATION
    # ----------------------------------------------

    if selected_tf in tf_annotations.index:

        annotation = tf_annotations.loc[selected_tf]

        st.subheader(
            f"{selected_tf} — {annotation['full_name']}"
        )

        with st.expander(
            "Known biological function",
            expanded=False
        ):

            st.write(
                annotation["function"]
            )

            st.caption(
                "External gene annotation provided for biological "
                "context. This description is not derived from "
                "the present dataset."
            )

    # ----------------------------------------------
    # REGULATORY UMAP
    # ----------------------------------------------

    plot_data = cell_data[
        [
            "reg_umap1",
            "reg_umap2"
        ]
    ].copy()

    plot_data["activity"] = regulon_activity.loc[
        plot_data.index,
        selected_regulon
    ]

    fig_regulon = px.scatter(
        plot_data,
        x="reg_umap1",
        y="reg_umap2",
        color="activity",
        color_continuous_scale="Viridis",
        title=f"Regulatory activity — {selected_regulon}",
        labels={
            "reg_umap1": "Regulatory UMAP 1",
            "reg_umap2": "Regulatory UMAP 2",
            "activity": "AUCell activity"
        },
        opacity=0.65,
        render_mode="webgl"
    )

    fig_regulon.update_traces(
        marker={"size": 3}
    )

    fig_regulon.update_layout(
        height=650,
        coloraxis_colorbar=dict(
            title="AUCell<br>activity"
        )
    )

    st.plotly_chart(
        fig_regulon,
        use_container_width=True
    )

    # ----------------------------------------------
    # STATISTICS
    # ----------------------------------------------

    stats = regulon_summary.loc[
        selected_regulon
    ]

    prevalence = stats[
        "pct_nonzero"
    ]

    st.subheader("In this dataset")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Prevalence",
        f"{prevalence:.2f}%"
    )

    col2.metric(
        "Mean activity",
        f"{stats['mean']:.4f}"
    )

    col3.metric(
        "Variability",
        f"{stats['std']:.4f}"
    )

    col4.metric(
        "95th percentile",
        f"{stats['q95']:.4f}"
    )

    # ----------------------------------------------
    # ACTIVITY PATTERN
    # ----------------------------------------------

    if prevalence <= 1:

        pattern = (
            "Very rare / highly localized activity"
        )

    elif prevalence <= 5:

        pattern = "Rare activity"

    elif prevalence <= 20:

        pattern = (
            "Activity detected in a minority of cells"
        )

    elif prevalence < 80:

        pattern = (
            "Activity distributed across a substantial "
            "fraction of cells"
        )

    else:

        pattern = "Broadly detected activity"

    st.info(
        f"**Activity pattern:** {pattern} "
        f"({prevalence:.2f}% of cells)."
    )

    st.caption(
        "Prevalence is the percentage of cells with non-zero "
        "AUCell activity. It describes how widely a regulon is "
        "detected, not the strength of its activity, and does not "
        "by itself define a biological cell state."
    )


# ==================================================
# REGULATORY COMPONENTS
# ==================================================

elif page == "Regulatory Components":

    st.title("Regulatory Components")

    st.write(
        "Explore recurring patterns of regulon activity identified "
        "using non-negative matrix factorization (NMF)."
    )

    component_options = [
        f"Program_{i}"
        for i in range(1, 9)
    ]

    selected_program = st.selectbox(
        "Select a regulatory component",
        component_options,
        format_func=lambda x: (
            f"Regulatory Component "
            f"{x.split('_')[1]}"
        )
    )

    component_number = (
        selected_program.split("_")[1]
    )

    # ----------------------------------------------
    # COMPONENT UMAP
    # ----------------------------------------------

    component_plot = cell_data[
        [
            "reg_umap1",
            "reg_umap2",
            selected_program
        ]
    ].copy()

    fig_component = px.scatter(
        component_plot,
        x="reg_umap1",
        y="reg_umap2",
        color=selected_program,
        color_continuous_scale="Viridis",
        title=(
            f"Regulatory Component "
            f"{component_number}"
        ),
        labels={
            "reg_umap1": "Regulatory UMAP 1",
            "reg_umap2": "Regulatory UMAP 2",
            selected_program: "Component activity"
        },
        opacity=0.65,
        render_mode="webgl"
    )

    fig_component.update_traces(
        marker={"size": 3}
    )

    fig_component.update_layout(
        height=650,
        coloraxis_colorbar=dict(
            title="Component<br>activity"
        )
    )

    st.plotly_chart(
        fig_component,
        use_container_width=True
    )

    # ----------------------------------------------
    # TOP REGULONS
    # ----------------------------------------------

    st.subheader("What defines this component?")

    st.write(
        "Top transcription-factor regulons contributing "
        "to this NMF regulatory component."
    )

    top_regulons = (
        program_loadings[selected_program]
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_regulons.columns = [
        "Regulon",
        "NMF loading"
    ]

    top_regulons[
        "NMF loading"
    ] = (
        top_regulons[
            "NMF loading"
        ].round(4)
    )

    st.dataframe(
        top_regulons,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Higher NMF loading indicates a stronger contribution "
        "of the regulon to this component. Loadings describe "
        "component composition and do not represent regulon "
        "activity in individual cells."
    )

    # ----------------------------------------------
    # ENRICHMENT
    # ----------------------------------------------

    st.subheader("Functional enrichment")

    enrichment = program_enrichment[
        program_enrichment["program"]
        == selected_program
    ].copy()

    generic_terms = [
        "transcription",
        "RNA metabolic",
        "RNA biosynthetic",
        "gene expression",
        "nucleobase-containing",
        "biosynthetic process",
        "metabolic process"
    ]

    specific_enrichment = enrichment[
        ~enrichment["name"].str.contains(
            "|".join(generic_terms),
            case=False,
            regex=True,
            na=False
        )
    ].copy()

    if specific_enrichment.empty:

        st.info(
            "No specific functional enrichment was identified "
            "for this component after excluding broad "
            "transcription/regulation terms. No pathway-level "
            "biological label was therefore assigned."
        )

    else:

        enrichment_display = (
            specific_enrichment[
                [
                    "source",
                    "name",
                    "p_value",
                    "intersection_size"
                ]
            ]
            .head(10)
            .copy()
        )

        enrichment_display.columns = [
            "Source",
            "Pathway / biological process",
            "Corrected p-value",
            "Target overlap"
        ]

        st.dataframe(
            enrichment_display,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "NMF components represent recurring patterns of regulon "
        "activity. They are continuous and potentially overlapping "
        "regulatory axes, not discrete cell types. Functional "
        "enrichment is based on targets of the top-loading regulons "
        "and is used for interpretation rather than as direct "
        "evidence of pathway activity."
    )


# ==================================================
# METHODS & ABOUT
# ==================================================

elif page == "Methods & About":

    st.title("Methods & About")

    st.header("Analysis workflow")

    st.markdown(
        """
### 1. Single-cell RNA-seq

MDA-MB-231 triple-negative breast cancer cells were processed
and quality controlled, resulting in **24,073 cells** used for
downstream analysis.

### 2. Gene regulatory network inference

**GRNBoost2** was used to infer associations between
transcription factors and potential target genes.

### 3. Motif-supported regulons

**cisTarget** motif enrichment was used to refine the inferred
network into motif-supported transcription-factor regulons.

### 4. Single-cell regulon activity

**AUCell** was used to estimate regulon activity in individual
cells. The resulting regulatory representation contains
**225 regulons across 24,073 cells**.

### 5. Regulatory landscape

PCA and UMAP were applied to the regulon-activity representation
to visualize regulatory heterogeneity.

### 6. Regulatory components

**Non-negative matrix factorization (NMF)** was applied to the
AUCell matrix. **Eight components** were retained as a compact
exploratory representation of recurring regulatory patterns.

### 7. Functional interpretation

Targets associated with top-loading regulons were evaluated
using functional enrichment against **GO Biological Process,
Reactome and WikiPathways**.
"""
    )

    st.divider()

    st.header("How to interpret the results")

    st.markdown(
        """
- **Regulon activity** represents inferred AUCell enrichment,
  not direct transcription-factor protein activity.

- **Regulon prevalence** is the fraction of cells with non-zero
  AUCell activity. It is not a measure of activity strength.

- **Regulatory components** are continuous and potentially
  overlapping NMF axes rather than discrete cell types.

- **Functional enrichment** provides biological context for
  targets associated with top-loading regulons. It does not
  demonstrate direct pathway activation.

- **UMAP** is a nonlinear visualization. Global geometry and
  distances should not be interpreted as literal biological
  distances.
"""
    )

    st.divider()

    st.header("Purpose")

    st.write(
        "TNBC Regulatory State Explorer is an exploratory and "
        "hypothesis-generation research tool for investigating "
        "transcriptional regulatory heterogeneity in a "
        "single-cell TNBC model."
    )

    st.warning(
        "This application is a research tool and is not intended "
        "for clinical or diagnostic use."
    )