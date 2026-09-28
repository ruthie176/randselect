import random
import time

import streamlit as st

from randselect.selector import available_items, random_selection

st.session_state.setdefault("roster", [])
st.session_state.setdefault("questions", [])
st.session_state.setdefault("used_names", set())
st.session_state.setdefault("used_questions", set())
st.session_state.setdefault("last_pick", None)

st.title("Random Selector")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Roster")
    with st.form("add_name_form", clear_on_submit=True):
        new_name = st.text_input("Name")
        if st.form_submit_button("Add") and new_name.strip():
            st.session_state.roster.append(new_name.strip())

    if st.session_state.roster:
        st.markdown("\n".join(f"- {name}" for name in st.session_state.roster))
    else:
        st.caption("No names added yet.")

with col2:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        new_question = st.text_input("Question")
        if st.form_submit_button("Add") and new_question.strip():
            st.session_state.questions.append(new_question.strip())

    if st.session_state.questions:
        st.markdown("\n".join(f"- {q}" for q in st.session_state.questions))
    else:
        st.caption("No questions added yet.")

st.divider()

no_repeats = st.checkbox("No repeats this session")

messages = []
if not st.session_state.roster or not st.session_state.questions:
    messages.append("Add at least one name and one question before drawing.")
elif no_repeats:
    if not available_items(st.session_state.roster, st.session_state.used_names):
        messages.append("All names are selected!")
    if not available_items(st.session_state.questions, st.session_state.used_questions):
        messages.append("All questions are selected!")

for message in messages:
    st.info(message)

placeholder = st.empty()

if st.button("Draw", disabled=bool(messages)):
    end_time = time.time() + 3
    while time.time() < end_time:
        flash_name, flash_question = random_selection(
            st.session_state.roster, st.session_state.questions, rng=random
        )
        placeholder.markdown(f"### {flash_name} — {flash_question}")
        time.sleep(0.1)

    used_names = st.session_state.used_names if no_repeats else None
    used_questions = st.session_state.used_questions if no_repeats else None
    chosen_name, chosen_question = random_selection(
        st.session_state.roster,
        st.session_state.questions,
        rng=random,
        used_names=used_names,
        used_questions=used_questions,
    )

    if no_repeats:
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)

    st.session_state.last_pick = (chosen_name, chosen_question)
    st.rerun()

if st.session_state.last_pick:
    chosen_name, chosen_question = st.session_state.last_pick
    placeholder.markdown(f"## 🎉 {chosen_name} — {chosen_question}")
