"""
AI Ransomware Defense Dashboard
Real-time threat visualization using Streamlit
"""
import os
import sys
import time
import json
import threading
import subprocess
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import deque

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    ALERT_THRESHOLD, WARNING_THRESHOLD, SAFE_THRESHOLD,
    BEHAVIORAL_LOG_PATH, TEST_FILES_DIR, SCORE_HISTORY_LENGTH
)
from monitor.monitor import BehaviorMonitor, FeatureExtractor

# Cache the model to avoid reloading on every refresh
@st.cache_resource
def get_threat_scorer():
    """Load and cache the threat scorer with model."""
    from antivirus.guardian_daemon import ThreatScorer
    return ThreatScorer()

@st.cache_resource
def get_guardian_daemon():
    """Start and cache the guardian daemon with active protection."""
    from antivirus.guardian_daemon import GuardianDaemon
    daemon = GuardianDaemon(active_protection=True)
    daemon.start()
    return daemon

# Page configuration
st.set_page_config(
    page_title="AI Ransomware Defense System",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visuals
st.markdown("""
<style>
    .threat-safe { color: #28a745; font-size: 2rem; font-weight: bold; }
    .threat-elevated { color: #ffc107; font-size: 2rem; font-weight: bold; }
    .threat-warning { color: #fd7e14; font-size: 2rem; font-weight: bold; }
    .threat-critical { color: #dc3545; font-size: 2rem; font-weight: bold; }
    .big-metric { font-size: 4rem; font-weight: bold; text-align: center; }
    .stAlert { margin-top: 1rem; }
    div[data-testid="stMetricValue"] { font-size: 2.5rem; }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'score_history' not in st.session_state:
        st.session_state.score_history = deque(maxlen=SCORE_HISTORY_LENGTH)
    if 'threats_detected' not in st.session_state:
        st.session_state.threats_detected = 0
    if 'monitoring_active' not in st.session_state:
        st.session_state.monitoring_active = True
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()


def get_threat_color(score):
    """Get color based on threat score."""
    if score >= ALERT_THRESHOLD:
        return "#dc3545"  # Red
    elif score >= WARNING_THRESHOLD:
        return "#fd7e14"  # Orange
    elif score >= SAFE_THRESHOLD:
        return "#ffc107"  # Yellow
    else:
        return "#28a745"  # Green


def get_threat_level(score):
    """Get threat level label."""
    if score >= ALERT_THRESHOLD:
        return "CRITICAL"
    elif score >= WARNING_THRESHOLD:
        return "WARNING"
    elif score >= SAFE_THRESHOLD:
        return "ELEVATED"
    else:
        return "SAFE"


def create_gauge_chart(score):
    """Create a gauge chart for threat visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Threat Level", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': get_threat_color(score)},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, SAFE_THRESHOLD * 100], 'color': 'rgba(40, 167, 69, 0.3)'},
                {'range': [SAFE_THRESHOLD * 100, WARNING_THRESHOLD * 100], 'color': 'rgba(255, 193, 7, 0.3)'},
                {'range': [WARNING_THRESHOLD * 100, ALERT_THRESHOLD * 100], 'color': 'rgba(253, 126, 20, 0.3)'},
                {'range': [ALERT_THRESHOLD * 100, 100], 'color': 'rgba(220, 53, 69, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': ALERT_THRESHOLD * 100
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"}
    )
    
    return fig


def create_history_chart(history_data):
    """Create a line chart for score history."""
    if not history_data:
        return None
    
    df = pd.DataFrame(history_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = go.Figure()
    
    # Add the score line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['score'] * 100,
        mode='lines+markers',
        name='Threat Score',
        line=dict(color='#00d4ff', width=2),
        marker=dict(size=4)
    ))
    
    # Add threshold lines
    fig.add_hline(y=ALERT_THRESHOLD * 100, line_dash="dash", 
                  line_color="red", annotation_text="Critical")
    fig.add_hline(y=WARNING_THRESHOLD * 100, line_dash="dash", 
                  line_color="orange", annotation_text="Warning")
    fig.add_hline(y=SAFE_THRESHOLD * 100, line_dash="dash", 
                  line_color="yellow", annotation_text="Elevated")
    
    fig.update_layout(
        title="Threat Score History",
        xaxis_title="Time",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"}
    )
    
    return fig


def get_current_analysis():
    """Get current threat analysis from behavioral logs."""
    monitor = BehaviorMonitor()
    extractor = FeatureExtractor()
    scorer = get_threat_scorer()  # Use cached scorer
    
    # Get recent operations
    operations = monitor.get_recent_operations(50)
    
    if not operations:
        return {
            "score": 0.0,
            "level": "SAFE",
            "features": {},
            "contributors": [],
            "operations_count": 0
        }
    
    # Get score and analysis
    result = scorer.get_score(operations)
    result["operations_count"] = len(operations)
    
    return result


def render_sidebar():
    """Render the sidebar."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/security-checked--v1.png", width=80)
        st.title("Control Panel")
        
        st.markdown("---")
        
        # Protection Status
        daemon = get_guardian_daemon()
        st.markdown("**Active Protection:** ENABLED")
        st.markdown(f"**Processes Killed:** {len(daemon.terminated_processes)}")
        
        # File Recovery Stats
        if daemon.recovery_results:
            st.markdown(f"**Files Recovered:** {daemon.recovery_results.get('recovered', 0)}")
        
        st.markdown("---")
        
        # Status
        status = "Active" if st.session_state.monitoring_active else "Paused"
        st.markdown(f"**Monitoring Status:** {status}")
        
        # Toggle monitoring
        if st.button("Toggle Monitoring"):
            st.session_state.monitoring_active = not st.session_state.monitoring_active
        
        st.markdown("---")
        
        # Thresholds display
        st.subheader("Detection Thresholds")
        st.write(f"Critical: {ALERT_THRESHOLD * 100:.0f}%")
        st.write(f"Warning: {WARNING_THRESHOLD * 100:.0f}%")
        st.write(f"Elevated: {SAFE_THRESHOLD * 100:.0f}%")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("Quick Actions")
        
        if st.button("Clear Log"):
            monitor = BehaviorMonitor()
            monitor.clear_log()
            st.session_state.score_history.clear()
            st.success("Log cleared!")
        
        if st.button("Reset History"):
            st.session_state.score_history.clear()
            st.session_state.threats_detected = 0
            st.success("History reset!")
        
        st.markdown("---")
        
        # File paths
        st.subheader("Paths")
        st.text(f"Log: {BEHAVIORAL_LOG_PATH}")
        st.text(f"Test Files: {TEST_FILES_DIR}")


def render_main_dashboard():
    """Render the main dashboard."""
    # Header
    st.title("AI Ransomware Defense System")
    st.markdown("*Real-time behavioral analysis powered by Deep Learning*")
    
    # Get current analysis
    analysis = get_current_analysis()
    current_score = analysis["score"]
    threat_level = analysis["level"]
    
    # Update history
    st.session_state.score_history.append({
        "timestamp": datetime.now().isoformat(),
        "score": current_score,
        "level": threat_level
    })
    
    # Check for threat detection
    if current_score >= ALERT_THRESHOLD:
        st.session_state.threats_detected += 1
    
    # Main metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Get daemon for protection stats
    daemon = get_guardian_daemon()
    
    with col1:
        color = get_threat_color(current_score)
        st.metric(
            label="Threat Score",
            value=f"{current_score * 100:.1f}%",
            delta=f"{(current_score - 0.5) * 100:.1f}%" if current_score != 0 else None
        )
    
    with col2:
        st.metric(
            label="Threat Level",
            value=threat_level
        )
    
    with col3:
        st.metric(
            label="Operations",
            value=analysis["operations_count"]
        )
    
    with col4:
        st.metric(
            label="Killed",
            value=len(daemon.terminated_processes)
        )
    
    with col5:
        recovered = daemon.recovery_results.get('recovered', 0) if daemon.recovery_results else 0
        st.metric(
            label="Recovered",
            value=recovered
        )
    
    # Alert banner
    if current_score >= ALERT_THRESHOLD:
        if daemon.terminated_processes:
            # Check if files were recovered
            recovered = 0
            if daemon.recovery_results:
                recovered = daemon.recovery_results.get('recovered', 0)
            
            if recovered > 0:
                st.success(f"""
                **RANSOMWARE NEUTRALIZED & FILES RECOVERED!**
                
                The AI detected ransomware behavior, terminated {len(daemon.terminated_processes)} malicious process(es),
                and successfully recovered {recovered} encrypted file(s)!
                
                Your files have been restored!
                """)
            else:
                st.error(f"""
                **RANSOMWARE NEUTRALIZED!**
                
                The AI detected ransomware behavior and automatically terminated {len(daemon.terminated_processes)} malicious process(es).
                Attempting file recovery...
                """)
        else:
            st.error("""
            **RANSOMWARE ACTIVITY DETECTED!**
            
            The system has detected behavioral patterns consistent with ransomware.
            Active protection is attempting to terminate the malicious process.
            """)
    elif current_score >= WARNING_THRESHOLD:
        st.warning("""
        **Suspicious Activity Detected**
        
        Elevated threat indicators have been identified. Monitor closely.
        """)
    elif current_score >= SAFE_THRESHOLD:
        st.info("**Elevated monitoring** - Some unusual activity detected.")
    else:
        st.success("**System Secure** - No threats detected.")
    
    st.markdown("---")
    
    # Charts row
    chart_col1, chart_col2 = st.columns([1, 2])
    
    with chart_col1:
        st.subheader("Current Threat Level")
        gauge_fig = create_gauge_chart(current_score)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with chart_col2:
        st.subheader("Threat Score Timeline")
        history_data = list(st.session_state.score_history)
        if history_data:
            history_fig = create_history_chart(history_data)
            if history_fig:
                st.plotly_chart(history_fig, use_container_width=True)
        else:
            st.info("Collecting data...")
    
    st.markdown("---")
    
    # Feature analysis
    st.subheader("Behavioral Analysis")
    
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("**Feature Breakdown**")
        features = analysis.get("features", {})
        
        if features:
            feature_data = {
                "Crypto API Calls": features.get("crypto_api_count", 0),
                "File Writes": features.get("file_write_count", 0),
                "File Reads": features.get("file_read_count", 0),
                "File Deletes": features.get("file_delete_count", 0),
                "Extension Changes": features.get("extension_changes", 0),
            }
            
            df = pd.DataFrame({
                "Feature": list(feature_data.keys()),
                "Count": list(feature_data.values())
            })
            
            fig = px.bar(df, x="Feature", y="Count", 
                        color="Count",
                        color_continuous_scale=["green", "yellow", "red"])
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with feat_col2:
        st.markdown("**Top Contributing Factors**")
        contributors = analysis.get("contributors", [])
        
        if contributors:
            for i, (name, value, explanation) in enumerate(contributors, 1):
                severity = "red" if i == 1 else "orange" if i == 2 else "yellow"
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0; border-left: 4px solid {severity}; 
                            background-color: rgba(255,255,255,0.1);">
                    <strong>{explanation}</strong><br>
                    <small>{name}: {value}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant threat indicators detected.")
        
        # Additional metrics
        st.markdown("**Additional Metrics**")
        add_metrics = {
            "Write/Read Ratio": f"{features.get('write_read_ratio', 0):.2f}",
            "Average Entropy": f"{features.get('avg_entropy', 0):.2f}",
            "Ops/Second": f"{features.get('operations_per_second', 0):.1f}",
            "Unique Files": str(features.get("unique_files", 0))
        }
        
        metrics_df = pd.DataFrame({
            "Metric": list(add_metrics.keys()),
            "Value": list(add_metrics.values())
        })
        st.dataframe(metrics_df, hide_index=True, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Refresh rate: {st.session_state.get('refresh_rate', 2)}s*"
    )


def main():
    """Main dashboard entry point."""
    initialize_session_state()
    render_sidebar()
    render_main_dashboard()
    
    # Auto-refresh
    if st.session_state.monitoring_active:
        time.sleep(0.5)
        st.rerun()


if __name__ == "__main__":
    main()
