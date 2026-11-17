import math
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ==========================================
# إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="DRVT Video Call Explorer",
    page_icon="📹",
    layout="wide"
)

# ==========================================
# الثوابت الفيزيائية (DRVT Constants)
# ==========================================
V_EQ = 286.398            # nm³
A0 = 0.529                # Angstrom
LAMBDA_REF = 91.127       # nm
LAMBDA_COMPTON = 0.002426 # nm

# ==========================================
# الدوال الحسابية والتصنيف
# ==========================================
def drvt(lambda_nm):
    r_nm = math.sqrt(V_EQ / (math.pi * lambda_nm))
    a_eff = math.pi * r_nm**2
    energy = 13.606 * r_nm**2
    xi = (r_nm * 10) / A0
    return r_nm, a_eff, energy, xi

def classify(xi):
    if xi > 1.05:
        return "🟢 Extended Resonance (رنين ممتد)"
    elif xi < 0.95:
        return "🔴 Localized Resonance (رنين متموضع)"
    else:
        return "🟡 Transition Horizon (أفق انتقالي)"

# ==========================================
# القائمة الجانبية للتحكم
# ==========================================
st.sidebar.header("⚙️ Control Panel | لوحة التحكم")

systems = {
    "Green Image Photon (532 nm)": 532.0,
    "Silicon Camera Sensor (550 nm)": 550.0,
    "Display Pixel (630 nm)": 630.0,
    "GaAs Photodetector (870 nm)": 870.0,
    "Optical Fiber Telecom (1550 nm)": 1550.0,
    "Custom Wavelength (طول موجي مخصص)": None
}

selected = st.sidebar.selectbox(
    "Select System Stage | اختر مرحلة النظام:",
    list(systems.keys())
)

if systems[selected] is None:
    lambda_nm = st.sidebar.slider(
        "Adjust Wavelength λ (nm) | حدد الطول الموجي:",
        min_value=100.0,
        max_value=35000.0,
        value=1000.0,
        step=50.0
    )
else:
    lambda_nm = systems[selected]

# ==========================================
# العنوان والمقدمة
# ==========================================
st.title("📹 DRVT Video Call Explorer")

st.markdown("""
### How does an image travel through a video call?
**Dynamic Resonant Volume Theory (DRVT)**  
By: **Dr. Khalid Abdel Fattah M. Osman**, Merowe University of Technology, Sudan

The image propagates through different resonant states:  
**Camera → Silicon → Processor → Optical Fiber → GaAs Detector → Display**
""")

# ==========================================
# حساب وعرض المؤشرات الحالية (5 أعمدة)
# ==========================================
r_nm, area, energy, xi = drvt(lambda_nm)

st.header("Current Resonant State | الحالة الرنينية الحالية")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("λ (nm)", f"{lambda_nm:.1f}")
c2.metric("r_res (nm)", f"{r_nm:.4f}")
c3.metric("A_eff (nm²)", f"{area:.4f}")
c4.metric("Energy E (eV)", f"{energy:.4f}")
c5.metric("ξ (Index)", f"{xi:.2f}")

st.info(f"**Classification:** {classify(xi)}")

# ==========================================
# خريطة الرنين التفاعلية (DRVT Resonance Map)
# ==========================================
st.header("DRVT Resonance Map")

y_upper = max(10.0, xi + 2.0)

fig = go.Figure()

fig.add_hrect(y0=1.05, y1=y_upper, fillcolor="green", opacity=0.15, line_width=0)
fig.add_hrect(y0=0.95, y1=1.05, fillcolor="yellow", opacity=0.25, line_width=0)
fig.add_hrect(y0=0, y1=0.95, fillcolor="red", opacity=0.15, line_width=0)

fig.add_trace(
    go.Scatter(
        x=[lambda_nm],
        y=[xi],
        mode="markers+text",
        text=[f"Current (ξ={xi:.2f})"],
        textposition="top center",
        marker=dict(size=18, color="darkblue")
    )
)

fig.add_hline(y=1, line_dash="dash", annotation_text="Bohr Horizon ξ = 1")

fig.update_layout(
    title="Current DRVT Position",
    xaxis_title="Wavelength λ (nm)",
    yaxis_title="Localization Index ξ",
    yaxis_range=[0, y_upper],
    height=480
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# مقارنة شاملة لجميع المراحل (جدول + تحميل)
# ==========================================
st.header("System Stages Comparison | مقارنة مراحل النظام")

comparison_data = []
for stage_name, wl in systems.items():
    if wl is not None:
        r, a, e, x_val = drvt(wl)
        comparison_data.append({
            "Stage": stage_name,
            "λ (nm)": wl,
            "r_res (nm)": round(r, 4),
            "A_eff (nm²)": round(a, 4),
            "Energy (eV)": round(e, 4),
            "ξ": round(x_val, 2),
            "State": classify(x_val)
        })

df_stages = pd.DataFrame(comparison_data)
st.dataframe(df_stages, use_container_width=True)

csv = df_stages.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Comparison Data (CSV)",
    data=csv,
    file_name="drvt_video_call_stages.csv",
    mime="text/csv"
)

# ==========================================
# مسار المكالمة المرئية (Video Call Journey)
# ==========================================
st.header("Image Journey Through a Video Call")

systems_path = ["Camera", "Silicon", "Processor", "Fiber", "GaAs", "Display"]
xi_path = [0.96, 0.96, 1.00, 4.58, 0.72, 0.95]
colors = ["orange", "orange", "gold", "green", "red", "orange"]

fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=systems_path,
        y=xi_path,
        mode="lines+markers+text",
        text=[f"{x:.2f}" for x in xi_path],
        textposition="top center",
        marker=dict(size=14, color=colors, line=dict(width=2, color="black")),
        line=dict(width=4)
    )
)

fig2.add_hline(y=1, line_dash="dash", annotation_text="Bohr Horizon")
fig2.update_layout(
    title="DRVT Interpretation of a Video Call",
    xaxis_title="System Stage",
    yaxis_title="ξ",
    height=450
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# الحدود المرجعية والتعريفات
# ==========================================
st.header("Fundamental DRVT Boundaries & Definitions")

col_chart, col_def = st.columns([1.2, 1])

with col_chart:
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=["Compton Boundary", "Reference Resonance", "Bohr Horizon"],
            y=[LAMBDA_COMPTON, LAMBDA_REF, 32550],
            mode="lines+markers+text",
            text=["λC", "λR", "λB"],
            textposition="top center",
            marker=dict(size=14)
        )
    )
    fig3.update_layout(
        title="DRVT Wavelength Boundaries",
        yaxis_type="log",
        yaxis_title="Wavelength (nm)",
        height=420
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_def:
    st.markdown(r"""
    #### Core Quantities
    * $V_{eq} = 286.398\;\text{nm}^3$ : Resonant Equilibrium Volume
    * $r_{res} = \sqrt{\frac{V_{eq}}{\pi \lambda}}$ : Resonant-State Radius
    * $A_{eff} = \pi r_{res}^2$ : Effective Resonant Area
    * $E = 13.606\,r_{res}^2$ : Resonant Energy Relation
    * $\xi = \frac{r_{res}}{a_0}$ : Localization Index ($a_0 = 0.529\;\text{\AA}$)
    """)
