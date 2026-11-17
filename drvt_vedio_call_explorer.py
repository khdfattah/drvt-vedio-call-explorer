import math
import streamlit as st
import plotly.graph_objects as go

# ==========================================
# DRVT VIDEO CALL EXPLORER
# ==========================================

st.set_page_config(
    page_title="DRVT Video Call Explorer",
    page_icon="📹",
    layout="wide"
)

# ==========================================
# Constants
# ==========================================

V_EQ = 286.398          # nm³
A0 = 0.529             # Angstrom
LAMBDA_REF = 91.127    # nm
LAMBDA_COMPTON = 0.002426  # nm

# ==========================================
# Functions
# ==========================================

def drvt(lambda_nm):

    r_nm = math.sqrt(
        V_EQ / (math.pi * lambda_nm)
    )

    a_eff = math.pi * r_nm**2

    energy = 13.606 * r_nm**2

    xi = (r_nm * 10) / A0

    return r_nm, a_eff, energy, xi


def classify(xi):

    if xi > 1.05:
        return "🟢 Extended Resonance"

    elif xi < 0.95:
        return "🔴 Localized Resonance"

    else:
        return "🟡 Transition Horizon"


# ==========================================
# Header
# ==========================================

st.title("📹 DRVT Video Call Explorer")

st.markdown("""
### How does an image travel through a video call?

Dynamic Resonant Volume Theory (DRVT)

The image propagates through different resonant states:

**Camera → Silicon → Processor → Optical Fiber → GaAs Detector → Display**
""")

# ==========================================
# Stage Selection
# ==========================================

systems = {
    "Green Image Photon": 532.0,
    "Silicon Camera Sensor": 550.0,
    "Optical Fiber (Telecom)": 1550.0,
    "GaAs Photodetector": 870.0,
    "Display Pixel": 630.0,
}

selected = st.selectbox(
    "Select System Stage",
    list(systems.keys())
)

lambda_nm = systems[selected]

r_nm, area, energy, xi = drvt(lambda_nm)

# ==========================================
# Metrics
# ==========================================

st.header("Current Resonant State")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "λ (nm)",
    f"{lambda_nm:.1f}"
)

c2.metric(
    "r_res (nm)",
    f"{r_nm:.4f}"
)

c3.metric(
    "A_eff (nm²)",
    f"{area:.4f}"
)

c4.metric(
    "ξ",
    f"{xi:.2f}"
)

st.info(classify(xi))

# ==========================================
# DRVT Resonance Map
# ==========================================

st.header("DRVT Resonance Map")

fig = go.Figure()

fig.add_hrect(
    y0=1.05,
    y1=6,
    fillcolor="green",
    opacity=0.15,
    line_width=0
)

fig.add_hrect(
    y0=0.95,
    y1=1.05,
    fillcolor="yellow",
    opacity=0.20,
    line_width=0
)

fig.add_hrect(
    y0=0,
    y1=0.95,
    fillcolor="red",
    opacity=0.15,
    line_width=0
)

fig.add_trace(
    go.Scatter(
        x=[lambda_nm],
        y=[xi],
        mode="markers+text",
        text=["Current State"],
        textposition="top center",
        marker=dict(
            size=18,
            color="darkblue"
        )
    )
)

fig.add_hline(
    y=1,
    line_dash="dash",
    annotation_text="Bohr Horizon ξ = 1"
)

fig.update_layout(
    title="Current DRVT Position",
    xaxis_title="Wavelength λ (nm)",
    yaxis_title="Localization Index ξ",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Video Call Journey
# ==========================================

st.header("Image Journey Through a Video Call")

systems_path = [
    "Camera",
    "Silicon",
    "Processor",
    "Fiber",
    "GaAs",
    "Display"
]

xi_path = [
    0.96,
    0.96,
    1.00,
    4.58,
    0.72,
    0.95
]

colors = [
    "orange",
    "orange",
    "gold",
    "green",
    "red",
    "orange"
]

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=systems_path,
        y=xi_path,
        mode="lines+markers+text",
        text=[f"{x:.2f}" for x in xi_path],
        textposition="top center",
        marker=dict(
            size=14,
            color=colors,
            line=dict(
                width=2,
                color="black"
            )
        ),
        line=dict(width=4)
    )
)

fig2.add_hline(
    y=1,
    line_dash="dash",
    annotation_text="Bohr Horizon"
)

fig2.update_layout(
    title="DRVT Interpretation of a Video Call",
    xaxis_title="System Stage",
    yaxis_title="ξ",
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================
# DRVT Reference Boundaries
# ==========================================

st.header("Fundamental DRVT Boundaries")

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=[
            "Compton Boundary",
            "Reference Resonance",
            "Bohr Horizon"
        ],
        y=[
            LAMBDA_COMPTON,
            LAMBDA_REF,
            32550
        ],
        mode="lines+markers+text",
        text=[
            "λC",
            "λR",
            "λB"
        ],
        textposition="top center",
        marker=dict(size=14)
    )
)

fig3.update_layout(
    title="DRVT Wavelength Boundaries",
    yaxis_type="log",
    yaxis_title="Wavelength (nm)",
    height=450
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# Definitions
# ==========================================

st.header("Symbols and Definitions")

st.markdown(r"""
### Core Quantities

$$
V_{eq}=286.398\;nm^3
$$

Resonant Equilibrium Volume

---

$$
r_{res}
$$

Resonant-State Radius

---

$$
A_{eff}
=
\pi r_{res}^{2}
$$

Effective Resonant Area

---

$$
E
=
13.606\,r_{res}^{2}
$$

Resonant Energy Relation

---

$$
\xi
=
\frac{r_{res}}{a_0}
$$

Localization Index

---

$$
a_0
=
0.529\,\AA
$$

Bohr Resonance Horizon
""")

# ==========================================
# Educational Summary
# ==========================================

st.header("Educational Interpretation")

st.markdown("""
### Extended Resonance (ξ > 1)

Photonic transport dominates.

Typical example:
- Optical Fiber

---

### Transition Horizon (ξ ≈ 1)

Balanced photonic–electronic behaviour.

Typical example:
- Silicon Camera Sensor

---

### Localized Resonance (ξ < 1)

Energy becomes localized and detection becomes efficient.

Typical example:
- GaAs Photodetector
""")
