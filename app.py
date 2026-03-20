import streamlit as st
from agents import build_graph, StoryState

st.set_page_config(
    page_title="Story Teller — Multi-Agent",
    page_icon="📖",
    layout="wide",
)

st.markdown("""
<style>
    .stApp { background-color: #f5edd8; }
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-orch   { background: #c8852a22; color: #c8852a; border: 1px solid #c8852a55; }
    .badge-writer { background: #b84c2b22; color: #b84c2b; border: 1px solid #b84c2b55; }
    .badge-imgen  { background: #4a7c5922; color: #4a7c59; border: 1px solid #4a7c5955; }
</style>
""", unsafe_allow_html=True)

st.title("📖 Story Teller")
st.caption("Multi-Agent System · LangGraph + Ollama")

st.markdown("---")

with st.sidebar:
    st.markdown("### Agent Pipeline")
    st.markdown("""
```
       START
         │
    ┌────▼────┐
    │  ORCH   │  ← crafts directive
    └────┬────┘
         │
    ┌────▼────┐
    │  STORY  │  ← writes story
    │ WRITER  │
    └────┬────┘
         │
    ┌────▼────┐
    │  IMAGE  │  ← distills prompt
    │  PROMPT │     + generates image
    └────┬────┘
         │
       END
```
    """)
    st.markdown("---")
    st.markdown("**Models used**")
    st.markdown("- LLM: `llama3.2` (Ollama)")
    st.markdown("- Image: `pollinations.ai` (free)")

# ── MAIN INPUT ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    seed = st.text_area(
        "Story Seed",
        placeholder="e.g. A lonely lighthouse keeper discovers an ancient map hidden in a bottle...",
        height=100,
    )

with col2:
    genre = st.selectbox(
        "Genre",
        ["Fantasy", "Sci-Fi", "Horror", "Mystery", "Romance", "Adventure"],
    )
    run = st.button("▶ Run Pipeline", type="primary", use_container_width=True)

if run:
    if not seed.strip():
        seed = "A mysterious traveler arrives at a forgotten village at dusk"

    app = build_graph()

    initial_state: StoryState = {
        "user_seed":      seed,
        "genre":          genre,
        "orch_directive": "",
        "story":          "",
        "image_prompt":   "",
        "image_url":      "",
        "log":            [],
    }

    st.markdown("---")
    st.markdown("### Pipeline Output")

    # Step containers
    orch_placeholder   = st.empty()
    writer_placeholder = st.empty()
    image_placeholder  = st.empty()

    with st.status("Running multi-agent pipeline...", expanded=True) as status:

        final_state = None
        for event in app.stream(initial_state):
            node_name = list(event.keys())[0]
            node_state = event[node_name]

            if node_name == "orchestrator":
                st.write("✅ Orchestrator: directive crafted")
                with orch_placeholder.container():
                    st.markdown(
                        '<span class="agent-badge badge-orch">⬡ Orchestrator</span>',
                        unsafe_allow_html=True,
                    )
                    st.info(node_state.get("orch_directive", ""))

            elif node_name == "story_writer":
                st.write("✅ Story Writer: story written")
                with writer_placeholder.container():
                    st.markdown(
                        '<span class="agent-badge badge-writer">✍ Story Writer</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div style="font-family:Georgia,serif;font-size:1.05rem;'
                        f'line-height:1.85;padding:1rem;background:#f5edd8;'
                        f'border-left:3px solid #b84c2b;border-radius:4px">'
                        f'{node_state.get("story","").replace(chr(10),"<br>")}</div>',
                        unsafe_allow_html=True,
                    )

            elif node_name == "image_prompt":
                st.write("✅ Image Prompt: visual prompt distilled")

            elif node_name == "image_generator":
                st.write("✅ Image Generator: image generated")
                with image_placeholder.container():
                    st.markdown(
                        '<span class="agent-badge badge-imgen">◈ Image Generator</span>',
                        unsafe_allow_html=True,
                    )
                    img_url = node_state.get("image_url", "")
                    if img_url:
                        st.image(img_url, caption=node_state.get("image_prompt", ""))
                    st.caption(f"**Prompt:** {node_state.get('image_prompt', '')}")

                final_state = node_state

        status.update(label="Pipeline complete ✓", state="complete", expanded=False)

    if final_state and final_state.get("log"):
        with st.expander("📝 Pipeline Log"):
            for entry in final_state["log"]:
                st.text(entry)
