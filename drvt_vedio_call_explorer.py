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

def classify(xi, lang="EN"):
    if xi > 1.05:
        return "🟢 رنين ممتد (Extended Resonance)" if lang == "AR" else "🟢 Extended Resonance"
    elif xi < 0.95:
        return "🔴 رنين متموضع (Localized Resonance)" if lang == "AR" else "🔴 Localized Resonance"
    else:
        return "🟡 أفق انتقالي (Transition Horizon)" if lang == "AR" else "🟡 Transition Horizon"

# ==========================================
# القائمة الجانبية للتحكم واختيار اللغة
# ==========================================
st.sidebar.header("⚙️ Control Panel | لوحة التحكم")

lang_choice = st.sidebar.radio(
    "Language | اللغة:",
    ["English", "العربية"],
    horizontal=True
)
lang = "AR" if lang_choice == "العربية" else "EN"

systems = {
    "Green Image Photon (532 nm)": 532.0,
    "Silicon Camera Sensor (550 nm)": 550.0,
    "Display Pixel (630 nm)": 630.0,
    "GaAs Photodetector (870 nm)": 870.0,
    "Optical Fiber Telecom (1550 nm)": 1550.0,
    "Custom Wavelength (طول موجي مخصص)": None
}

st.sidebar.subheader("1️⃣ المرحلة الأساسية (Primary Stage)")
selected_1 = st.sidebar.selectbox(
    "Select Primary Stage:" if lang == "EN" else "اختر المرحلة الأولى:",
    list(systems.keys()),
    index=0
)

if systems[selected_1] is None:
    lambda_1 = st.sidebar.slider(
        "Primary λ (nm):" if lang == "EN" else "الطول الموجي الأول (nm):",
        min_value=100.0, max_value=35000.0, value=1000.0, step=50.0
    )
    name_1 = f"Custom ({lambda_1} nm)"
else:
    lambda_1 = systems[selected_1]
    name_1 = selected_1.split(" (")[0]

# خيار المقارنة مع مرحلة ثانية
compare_mode = st.sidebar.checkbox(
    "Enable Side-by-Side Comparison" if lang == "EN" else "تفعيل مقارنة مرحلتين جنباً إلى جنب",
    value=True
)

if compare_mode:
    st.sidebar.subheader("2️⃣ مرحلة المقارنة (Comparison Stage)")
    selected_2 = st.sidebar.selectbox(
        "Select Second Stage:" if lang == "EN" else "اختر المرحلة الثانية للمقارنة:",
        list(systems.keys()),
        index=4 # Optical Fiber كافتراضي للمقارنة
    )
    if systems[selected_2] is None:
        lambda_2 = st.sidebar.slider(
            "Comparison λ (nm):" if lang == "EN" else "الطول الموجي الثاني (nm):",
            min_value=100.0, max_value=35000.0, value=2500.0, step=50.0
        )
        name_2 = f"Custom 2 ({lambda_2} nm)"
    else:
        lambda_2 = systems[selected_2]
        name_2 = selected_2.split(" (")[0]

# ==========================================
# العنوان والمقدمة
# ==========================================
st.title("📹 DRVT Video Call Explorer")

if lang == "AR":
    st.markdown("""
    ### كيف تنتقل الصورة عبر مكالمة الفيديو؟
    **نظرية الحجم الرنيني الديناميكي (DRVT)**  
    إعداد: **د. خالد عبد الفتاح م. عثمان**، جامعة مروي التكنولوجية، السودان
    
    تنتقل الإشارة الضوئية والإلكترونية للصورة عبر حالات رنينية متتابعة:  
    **الكاميرا ← السيليكون ← المعالج ← الألياف الضوئية ← الكاشف  ← الشاشة**
    """)
else:
    st.markdown("""
    ### How does an image travel through a video call?
    **Dynamic Resonant Volume Theory (DRVT)**  
    By: **Dr. Khalid Abdel Fattah M. Osman**, Merowe University of Technology, Sudan

    The image propagates through different resonant states:  
    **Camera → Silicon → Processor → Optical Fiber → GaAs Detector → Display**
    """)

# ==========================================
# حساب وعرض المؤشرات (مع المقارنة إن وجدت)
# ==========================================
r1, a1, e1, xi1 = drvt(lambda_1)

if not compare_mode:
    st.header("الحالة الرنينية الحالية" if lang == "AR" else "Current Resonant State")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("λ (nm)", f"{lambda_1:.1f}")
    c2.metric("r_res (nm)", f"{r1:.4f}")
    c3.metric("A_eff (nm²)", f"{a1:.4f}")
    c4.metric("Energy E (eV)", f"{e1:.4f}")
    c5.metric("ξ (Index)", f"{xi1:.2f}")
    st.info(f"**التصنيف:** {classify(xi1, lang)}" if lang == "AR" else f"**Classification:** {classify(xi1, lang)}")
else:
    r2, a2, e2, xi2 = drvt(lambda_2)
    st.header("مقارنة الحالات الرنينية جنباً إلى جنب" if lang == "AR" else "Side-by-Side Resonant State Comparison")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader(f"🔵 {name_1}")
        m1, m2, m3 = st.columns(3)
        m1.metric("λ (nm)", f"{lambda_1:.1f}")
        m2.metric("ξ (Index)", f"{xi1:.2f}")
        m3.metric("Energy (eV)", f"{e1:.4f}")
        st.caption(f"r_res = {r1:.4f} nm | A_eff = {a1:.4f} nm²")
        st.info(classify(xi1, lang))
        
    with col_b:
        st.subheader(f"🟣 {name_2}")
        m4, m5, m6 = st.columns(3)
        m4.metric("λ (nm)", f"{lambda_2:.1f}", delta=f"{lambda_2 - lambda_1:+.1f} nm")
        m5.metric("ξ (Index)", f"{xi2:.2f}", delta=f"{xi2 - xi1:+.2f}")
        m6.metric("Energy (eV)", f"{e2:.4f}", delta=f"{e2 - e1:+.4f} eV")
        st.caption(f"r_res = {r2:.4f} nm | A_eff = {a2:.4f} nm²")
        st.info(classify(xi2, lang))

# ==========================================
# خريطة الرنين التفاعلية مع المنحنى المتصل
# ==========================================
st.header("خريطة الرنين التفاعلية (DRVT Resonance Map)" if lang == "AR" else "DRVT Resonance Map")

max_xi = max(xi1, xi2) if compare_mode else xi1
y_upper = max(10.0, max_xi + 2.0)

max_l = max(lambda_1, lambda_2) if compare_mode else lambda_1
min_l = min(lambda_1, lambda_2) if compare_mode else lambda_1
x_max = max(1800.0, max_l * 1.15)
x_min = min(400.0, min_l * 0.85)

step = (x_max - x_min) / 150
lambda_curve = [x_min + i * step for i in range(151)]
xi_curve = [drvt(l)[3] for l in lambda_curve]

fig = go.Figure()

fig.add_hrect(y0=1.05, y1=y_upper, fillcolor="green", opacity=0.15, line_width=0)
fig.add_hrect(y0=0.95, y1=1.05, fillcolor="yellow", opacity=0.25, line_width=0)
fig.add_hrect(y0=0, y1=0.95, fillcolor="red", opacity=0.15, line_width=0)

# المنحنى المتصل
fig.add_trace(
    go.Scatter(
        x=lambda_curve,
        y=xi_curve,
        mode="lines",
        name="DRVT Curve ξ(λ)",
        line=dict(color="royalblue", width=2, dash="dot")
    )
)

# النقطة الأولى
fig.add_trace(
    go.Scatter(
        x=[lambda_1],
        y=[xi1],
        mode="markers+text",
        name=name_1,
        text=[f"{name_1} (ξ={xi1:.2f})"],
        textposition="top right",
        marker=dict(size=16, color="darkblue", line=dict(width=2, color="white"))
    )
)

# النقطة الثانية عند تفعيل المقارنة
if compare_mode:
    fig.add_trace(
        go.Scatter(
            x=[lambda_2],
            y=[xi2],
            mode="markers+text",
            name=name_2,
            text=[f"{name_2} (ξ={xi2:.2f})"],
            textposition="bottom left",
            marker=dict(size=16, color="purple", symbol="diamond", line=dict(width=2, color="white"))
        )
    )

fig.add_hline(y=1, line_dash="dash", annotation_text="Bohr Horizon ξ = 1")

fig.update_layout(
    title="موقع المراحل المختارة على المنحنى النظري" if lang == "AR" else "Selected Stages on Theoretical DRVT Curve",
    xaxis_title="Wavelength λ (nm)",
    yaxis_title="Localization Index ξ",
    xaxis_range=[x_min, x_max],
    yaxis_range=[0, y_upper],
    height=480
)

st.plotly_chart(fig, use_container_width=True)

if lang == "AR":
    st.caption("💡 **تفسير الرسم:** يوضح الخط المنقط العلاقة العكسية بين الطول الموجي ومعامل التموضع (ξ). كلما زاد الطول الموجي، اقترب النظام من أفق بور (ξ = 1) حيث يبدأ الانتقال من الانتشار الفوتوني الممتد إلى التموضع الإلكتروني.")
else:
    st.caption("💡 **Chart Interpretation:** The dotted curve illustrates the inverse relationship between wavelength and localization index (ξ). Longer wavelengths approach the Bohr Horizon (ξ = 1), marking the transition toward localized electronic behavior.")

# ==========================================
# مقارنة شاملة لجميع المراحل (جدول + تحميل)
# ==========================================
st.header("جدول مقارنة جميع مراحل النظام" if lang == "AR" else "System Stages Comparison Table")

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
            "State": classify(x_val, lang)
        })

df_stages = pd.DataFrame(comparison_data)
st.dataframe(df_stages, use_container_width=True)

csv = df_stages.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 تحميل بيانات المقارنة (CSV)" if lang == "AR" else "📥 Download Comparison Data (CSV)",
    data=csv,
    file_name="drvt_video_call_stages.csv",
    mime="text/csv"
)

# ==========================================
# مسار المكالمة المرئية (Video Call Journey)
# ==========================================
st.header("رحلة الصورة عبر مكالمة الفيديو" if lang == "AR" else "Image Journey Through a Video Call")

systems_path = ["Camera", "Silicon", "Processor", "Fiber", "GaAs", "Display"]
xi_path = [0.96, 0.96, 1.00, 4.58, 0.72, 0.95]
colors = ["orange", "orange", "gold", "green", "red", "orange"]

