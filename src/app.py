import plotly.graph_objects as go
import streamlit as st

# Local libraries
from config import create_model
from session import TopologicSession, SessionContext
from tools import list_session_items, get_object_info, clear_session
from tools import create_vertex, create_cube, create_edge, create_wire, create_face, create_rectangle, create_circle, create_prism, create_cylinder

# AI
from langchain.agents import create_agent

# Topologic
from topologicpy.Cluster import Cluster
from topologicpy.Plotly import Plotly

# 1. Page Config & Dark/Coral Theme CSS
st.set_page_config(layout="wide", page_title="Topologic Vibe")

st.markdown("""
    <style>
        .block-container { padding-bottom: 0px; }
        
        /* Layout alignment for the chat input row */
        [data-testid="stHorizontalBlock"] {
            align-items: end;
        }

        /* Button Styling: White border/text for Dark background vibe */
        .stButton > button {
            border-radius: 4px !important;
            height: 44px !important;
            width: 100% !important;
            border: 2px solid #FF7043 !important; /* Coral Accent */
            background-color: transparent !important;
            color: #FF7043 !important;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #FF7043 !important;
            color: #ffffff !important;
        }

        .stButton > button:disabled {
            border-color: #444444 !important;
            color: #666666 !important;
        }

        /* Custom styling for the "Empty Canvas" message in dark mode */
        .dark-info-box {
            padding: 1rem;
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 5px solid #FF7043;
            color: #E0E0E0;
            border-radius: 4px;
            margin-bottom: 1rem;
            font-family: sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Define the Modal (Dialog)
@st.dialog("Session Objects")
def show_inventory(session):
    if not session.items:
        st.write("No objects found.")
    else:
        items_data = [
            {"Name": name, "Type": type(obj).__name__} 
            for name, obj in session.items.items()
        ]
        st.table(items_data)

# 3. Agent & Session Setup
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(
        model=create_model(),
        tools=[
            clear_session,
            create_cube,
            create_vertex,
            create_wire,
            create_face,
            create_rectangle,
            create_circle,
            create_prism,
            create_cylinder,
            
            create_edge,
            list_session_items,
            get_object_info
        ],
        context_schema=SessionContext,
        system_prompt="You are a topologicpy library assistant."
    )

if "topologic_session" not in st.session_state:
    st.session_state.topologic_session = TopologicSession()

session = st.session_state.topologic_session
session_context = SessionContext(session=session)

# 4. Layout
col_chat, col_viz = st.columns([1, 2], gap="large")

with col_chat:
    # Control row for chat actions
    ctrl_col1, ctrl_col2 = st.columns([1, 0.25])
    with ctrl_col1:
        st.markdown("### TopologicVibe")
    with ctrl_col2:
        if st.button(label="", icon=":material/delete_outline:", help="Clear chat history", use_container_width=True):
            session.messages = []
            st.session_state.messages = []
            st.rerun()
    chat_container = st.container(height=650)

    if "messages" not in st.session_state:
        st.session_state.messages = session.get_messages()

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # INPUT SECTION: 
    has_objects = len(session.items) > 0
    
    input_row = st.container()
    with input_row:
        chat_col, btn_col = st.columns([8, 1.2])
        
        with chat_col:
            prompt = st.chat_input("What do you want to build?")
            
        with btn_col:
            if st.button(label="", 
                         icon=":material/view_in_ar:",
                         help="Show Session Objects", 
                         disabled=not has_objects,
                         use_container_width=True):
                show_inventory(session)

    if prompt:
        # Save user message to session and UI
        session.add_message("user", prompt)
        st.session_state.messages = session.get_messages()
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Send the full session history to the agent stream
        messages_for_agent = session.get_messages()

        # Track the last assistant text received so we can save it once streaming completes
        last_assistant_text = ""

        for chunk in st.session_state.agent.stream(
            {"messages": messages_for_agent},
            context=session_context,
            stream_mode="updates",
        ):
            for step, data in chunk.items():
                content = data['messages'][-1].content_blocks
                if step == "model":
                    # extract text or tool_call placeholder
                    piece = content[0]["text"] if content[0]["type"] != "tool_call" else f"Using '{content[0]['name']}' tool ..."
                    last_assistant_text = piece
                    with chat_container:
                        with st.chat_message("assistant"):
                            st.markdown(piece)

        # After streaming completes, persist assistant response into the session
        if last_assistant_text:
            session.add_message("assistant", last_assistant_text)
            st.session_state.messages = session.get_messages()

        st.rerun()

# VIZ SECTION
with col_viz:
    objs = [obj for name, obj in session.items.items()]
    
    if not objs:
        st.markdown('<div class="dark-info-box"><b>Canvas Status:</b> The canvas is empty.</div>', unsafe_allow_html=True)
    
    if objs:
        scene = Cluster.ByTopologies(objs)
        data = Plotly.DataByTopology(scene)
        fig = go.Figure(data=data)
        
        for trace in fig.data:
            # 1. FACE TRANSPARENCY
            if trace.type in ['mesh3d', 'surface']:
                trace.opacity = 0.1  # Set transparency (0.0 to 1.0)
                trace.flatshading = True # Better architectural look
            
            # 2. EDGES
            if hasattr(trace, 'line'):
                trace.line.width = 3
                trace.line.color = '#F5F5F4'
                trace.opacity = 0.8  # Ensure edges are fully opaque
            
            # 3. VERTEXES
            if hasattr(trace, 'marker'):
                trace.marker.size = 7
                trace.marker.color = '#FF7043'
        
        fig.update_layout(
            height=750, 
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            scene=dict(
                xaxis=dict(showgrid=True, gridcolor='#333333', zerolinecolor='#444444'),
                yaxis=dict(showgrid=True, gridcolor='#333333', zerolinecolor='#444444'),
                zaxis=dict(showgrid=True, gridcolor='#333333', zerolinecolor='#444444'),
                bgcolor='#0E1117',
                aspectmode='data'
            )
        )
        
        st.plotly_chart(fig, width='stretch', theme=None)