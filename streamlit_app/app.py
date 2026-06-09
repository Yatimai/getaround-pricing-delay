import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Getaround Analysis",
    page_icon=None,
    layout="wide"
)

st.markdown("""
    <style>
    .recommendation-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel('data/get_around_delay_analysis.xlsx')
    return df

def prepare_consecutive_data(df):
    consecutive = df[df['previous_ended_rental_id'].notna()].copy()
    consecutive['previous_delay'] = consecutive['previous_ended_rental_id'].map(
        df.set_index('rental_id')['delay_at_checkout_in_minutes']
    )
    consecutive_with_delay = consecutive[consecutive['previous_delay'].notna()].copy()
    consecutive_with_delay['is_problematic'] = (
        consecutive_with_delay['previous_delay'] >
        consecutive_with_delay['time_delta_with_previous_rental_in_minutes']
    )
    return consecutive, consecutive_with_delay

def calculate_threshold_impact(consecutive, consecutive_with_delay, threshold, scope='all'):
    if scope == 'mobile':
        consecutive_filtered = consecutive[consecutive['checkin_type'] == 'mobile']
        with_delay_filtered = consecutive_with_delay[consecutive_with_delay['checkin_type'] == 'mobile']
    elif scope == 'connect':
        consecutive_filtered = consecutive[consecutive['checkin_type'] == 'connect']
        with_delay_filtered = consecutive_with_delay[consecutive_with_delay['checkin_type'] == 'connect']
    else:
        consecutive_filtered = consecutive
        with_delay_filtered = consecutive_with_delay

    blocked = consecutive_filtered[consecutive_filtered['time_delta_with_previous_rental_in_minutes'] < threshold]

    temp = with_delay_filtered.copy()
    temp['would_solve'] = (
        (temp['previous_delay'] > temp['time_delta_with_previous_rental_in_minutes']) &
        (threshold > temp['time_delta_with_previous_rental_in_minutes'])
    )
    solved = temp['would_solve'].sum()
    total_problems = with_delay_filtered['is_problematic'].sum()

    return {
        'blocked_rentals': len(blocked),
        'blocked_pct': len(blocked) / len(consecutive_filtered) * 100 if len(consecutive_filtered) > 0 else 0,
        'problems_solved': solved,
        'problems_solved_pct': solved / total_problems * 100 if total_problems > 0 else 0,
        'total_problems': total_problems
    }

try:
    df = load_data()
    consecutive, consecutive_with_delay = prepare_consecutive_data(df)
    data_loaded = True
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Missing file: data/get_around_delay_analysis.xlsx")
    st.stop()

st.title("Getaround - Delay Analysis")
st.markdown("---")
st.markdown("""
### Objective
Determine the **optimal minimum threshold** between two rentals to reduce problems caused by delays.
""")
st.markdown("---")

st.sidebar.header("Settings")
threshold = st.sidebar.slider("Minimum delay (minutes)", 0, 720, 60, 15)
scope = st.sidebar.radio("Apply to:", ["All", "Mobile", "Connect"])
scope_map = {"All": "all", "Mobile": "mobile", "Connect": "connect"}
scope_value = scope_map[scope]

impact = calculate_threshold_impact(consecutive, consecutive_with_delay, threshold, scope_value)
st.sidebar.markdown("---")
st.sidebar.metric("Blocked rentals", f"{impact['blocked_rentals']}", f"{impact['blocked_pct']:.1f}%")
st.sidebar.metric("Problems solved", f"{impact['problems_solved']}", f"{impact['problems_solved_pct']:.1f}%")

st.header("1. Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total rentals", f"{len(df):,}")
col2.metric("Cars", f"{df['car_id'].nunique():,}")
col3.metric("Ended", f"{(df['state']=='ended').sum():,}")
col4.metric("Canceled", f"{(df['state']=='canceled').sum():,}")
st.markdown("---")

st.header("2. Delay analysis")
delays = df['delay_at_checkout_in_minutes'].dropna()
late_count = (delays > 0).sum()
on_time_count = (delays <= 0).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Late", f"{late_count:,}", f"{late_count/len(delays)*100:.1f}%")
col2.metric("On time", f"{on_time_count:,}", f"{on_time_count/len(delays)*100:.1f}%")
col3.metric("Average delay", f"{delays[delays>0].mean():.0f} min")

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    delays_filt = delays[(delays>-500) & (delays<2000)]
    fig.add_trace(go.Histogram(x=delays_filt, nbinsx=50))
    fig.add_vline(x=0, line_dash="dash", line_color="red")
    fig.update_layout(title="Delay distribution", xaxis_title="Minutes", height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(data=[go.Pie(labels=['Late', 'On time'], values=[late_count, on_time_count], hole=0.4)])
    fig.update_layout(title="Proportion", height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.header("3. Mobile vs Connect comparison")
st.markdown("""
**Mobile**: the driver meets the owner and signs on a smartphone.
**Connect**: the driver opens the car with their smartphone (no meeting).
""")

col1, col2 = st.columns(2)

# Stats Mobile
mobile_delays = df[df['checkin_type'] == 'mobile']['delay_at_checkout_in_minutes'].dropna()
mobile_late = (mobile_delays > 0).sum()
mobile_pct = mobile_late / len(mobile_delays) * 100

# Stats Connect
connect_delays = df[df['checkin_type'] == 'connect']['delay_at_checkout_in_minutes'].dropna()
connect_late = (connect_delays > 0).sum()
connect_pct = connect_late / len(connect_delays) * 100

with col1:
    st.subheader("Mobile")
    st.metric("Rentals", f"{len(df[df['checkin_type']=='mobile']):,}", "79.8%")
    st.metric("Late", f"{mobile_late:,}", f"{mobile_pct:.1f}%")
    st.metric("Average delay", f"{mobile_delays[mobile_delays>0].mean():.0f} min")

with col2:
    st.subheader("Connect")
    st.metric("Rentals", f"{len(df[df['checkin_type']=='connect']):,}", "20.2%")
    st.metric("Late", f"{connect_late:,}", f"{connect_pct:.1f}%")
    st.metric("Average delay", f"{connect_delays[connect_delays>0].mean():.0f} min")

# Comparison chart
fig = go.Figure(data=[
    go.Bar(name='Mobile', x=['% Late', 'Avg delay (min)'], y=[mobile_pct, mobile_delays[mobile_delays>0].mean()], marker_color='#ff6b6b'),
    go.Bar(name='Connect', x=['% Late', 'Avg delay (min)'], y=[connect_pct, connect_delays[connect_delays>0].mean()], marker_color='#4dabf7')
])
fig.update_layout(barmode='group', title="Mobile vs Connect comparison", height=400)
st.plotly_chart(fig, use_container_width=True)

# Problematic cases by type
mobile_prob = consecutive_with_delay[consecutive_with_delay['checkin_type'] == 'mobile']
connect_prob = consecutive_with_delay[consecutive_with_delay['checkin_type'] == 'connect']
st.markdown(f"""
**Problematic cases:**
- **Mobile**: {mobile_prob['is_problematic'].sum()} / {len(mobile_prob)} ({mobile_prob['is_problematic'].sum()/len(mobile_prob)*100:.1f}%)
- **Connect**: {connect_prob['is_problematic'].sum()} / {len(connect_prob)} ({connect_prob['is_problematic'].sum()/len(connect_prob)*100:.1f}%)
""")

st.markdown("---")

st.header("4. Consecutive rentals")
col1, col2, col3 = st.columns(3)
col1.metric("Consecutive", f"{len(consecutive):,}", f"{len(consecutive)/len(df)*100:.1f}%")
col2.metric("Average gap", f"{consecutive['time_delta_with_previous_rental_in_minutes'].mean():.0f} min")
col3.metric("Median gap", f"{consecutive['time_delta_with_previous_rental_in_minutes'].median():.0f} min")

fig = go.Figure()
time_deltas = consecutive['time_delta_with_previous_rental_in_minutes'].dropna()
fig.add_trace(go.Histogram(x=time_deltas, nbinsx=30))
fig.update_layout(title="Gaps between rentals", xaxis_title="Minutes", height=400)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.header("5. Problematic cases")
total_prob = consecutive_with_delay['is_problematic'].sum()
col1, col2 = st.columns(2)
col1.metric("Problematic cases", f"{total_prob}", f"{total_prob/len(consecutive_with_delay)*100:.1f}%")
col2.metric("Analyzed", f"{len(consecutive_with_delay):,}")
st.markdown("---")

st.header("6. Threshold simulation")
thresholds = [0, 30, 60, 90, 120, 180, 240, 300, 360, 480, 720]
results = []
for t in thresholds:
    imp = calculate_threshold_impact(consecutive, consecutive_with_delay, t, scope_value)
    results.append({'Threshold': t, '% Blocked': imp['blocked_pct'], '% Solved': imp['problems_solved_pct']})

results_df = pd.DataFrame(results)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=results_df['Threshold'], y=results_df['% Blocked'], name="% Blocked", line=dict(color='red', width=3)), secondary_y=False)
fig.add_trace(go.Scatter(x=results_df['Threshold'], y=results_df['% Solved'], name="% Solved", line=dict(color='green', width=3)), secondary_y=True)
fig.add_vline(x=threshold, line_dash="dash", line_color="blue")
fig.update_layout(title="Trade-off", height=500)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(results_df, use_container_width=True)
st.markdown("---")

st.header("7. Recommendations")
st.markdown("""
<div class="recommendation-box">
<h3>RECOMMENDATION</h3>
<p><strong>Threshold: 60 minutes | Scope: All cars</strong></p>
<ul>
<li>67% of problems solved</li>
<li>22% of rentals blocked (limited impact)</li>
<li>~1.9% estimated revenue loss</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("*Getaround Analysis*")
