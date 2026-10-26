import streamlit as st

from rag import (
    load_vector_store,
    retrieve_authorized_context,
    generate_answer,
)

from privacy_scanner import (
    scan_for_pii,
    calculate_risk,
)

from access_control import get_allowed_departments
from audit_logger import log_interaction


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="PrivateRAG",
    page_icon="🔐",
    layout="wide",
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🔐 PrivateRAG")

st.subheader(
    "Privacy-Aware Enterprise AI"
)

st.caption(
    "Secure internal knowledge assistant for "
    "NordWerk Solutions GmbH"
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("Employee Access")

    role = st.selectbox(
        "Select your role",
        [
            "General",
            "IT",
            "HR",
            "Finance",
        ],
    )

    role = role.lower()

    allowed_departments = get_allowed_departments(role)

    st.write("**Authorised knowledge domains:**")

    for department in allowed_departments:
        st.write(f"✓ {department.upper()}")

    st.divider()

    st.write("### Security Architecture")

    st.write("🔐 Local Llama 3.2")
    st.write("🛡️ Role-Based Access Control")
    st.write("🔎 PII Detection")
    st.write("📚 Grounded RAG")
    st.write("💾 Local Vector Database")
    st.write("📝 Privacy-Safe Audit Logging")

    st.divider()

    st.caption(
        "Demo environment using synthetic company data."
    )


# ---------------------------------------------------------
# MAIN QUESTION AREA
# ---------------------------------------------------------

st.write("### Ask PrivateRAG")

st.write(
    "Ask a question about authorised NordWerk "
    "company information."
)

question = st.text_area(
    "Employee question",
    placeholder=(
        "Example: Can I send customer personal "
        "information to a public AI tool?"
    ),
    height=120,
)


# ---------------------------------------------------------
# PROCESS QUESTION
# ---------------------------------------------------------

if st.button(
    "Ask PrivateRAG",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analysing privacy and searching "
            "authorised company knowledge..."
        ):

            # ---------------------------------------------
            # PRIVACY SCAN
            # ---------------------------------------------

            pii_entities = scan_for_pii(
                question
            )

            privacy_risk = calculate_risk(
                pii_entities
            )

            # ---------------------------------------------
            # LOAD VECTOR STORE
            # ---------------------------------------------

            vector_store = load_vector_store()

            # ---------------------------------------------
            # AUTHORISED RETRIEVAL
            # ---------------------------------------------

            documents = retrieve_authorized_context(
                vector_store,
                question,
                role,
            )

            # ---------------------------------------------
            # LOCAL LLM GENERATION
            # ---------------------------------------------

            answer = generate_answer(
                question,
                documents,
            )

            # ---------------------------------------------
            # PRIVACY-SAFE AUDIT LOG
            # ---------------------------------------------

            log_interaction(
                role=role,
                privacy_risk=privacy_risk,
                pii_entities=pii_entities,
                documents=documents,
            )

        st.divider()


        # -------------------------------------------------
        # PRIVACY ASSESSMENT
        # -------------------------------------------------

        st.write(
            "### 🛡️ Privacy Assessment"
        )

        if privacy_risk == "HIGH":

            st.error(
                "🔴 Personal Data Detected • HIGH"
            )

        elif privacy_risk == "MEDIUM":

            st.warning(
                "🟠 Personal Data Detected • MEDIUM"
            )

        else:

            st.success(
                "🟢 No Significant Personal Data "
                "Detected • LOW"
            )

        if pii_entities:

            detected_types = sorted(
                {
                    entity["type"]
                    for entity in pii_entities
                }
            )

            st.write(
                "**Detected sensitive data types:**"
            )

            for entity_type in detected_types:

                st.write(
                    f"• {entity_type}"
                )

            st.caption(
                "Detected values are not displayed "
                "to reduce unnecessary exposure of "
                "personal information."
            )

        else:

            st.write(
                "No supported PII types detected "
                "in the question."
            )


        # -------------------------------------------------
        # ANSWER
        # -------------------------------------------------

        st.write(
            "### 💬 Answer"
        )

        st.info(
            answer
        )


        # -------------------------------------------------
        # AUTHORISED SOURCES
        # -------------------------------------------------

        st.write(
            "### 📚 Authorised Sources"
        )

        if documents:

            sources = set()

            for document in documents:

                sources.add(
                    (
                        document.metadata["source"],
                        document.metadata["department"],
                    )
                )

            for source, department in sorted(
                sources
            ):

                st.write(
                    f"📄 **{source}** "
                    f"— {department.upper()}"
                )

        else:

            st.write(
                "No authorised company source "
                "was retrieved."
            )


        # -------------------------------------------------
        # ACCESS INFORMATION
        # -------------------------------------------------

        with st.expander(
            "🔐 Why can I access these sources?"
        ):

            st.write(
                f"Your current role is "
                f"**{role.upper()}**."
            )

            st.write(
                "PrivateRAG filters the vector "
                "database before information is "
                "provided to the language model."
            )

            st.write(
                "**Your authorised domains:**"
            )

            for department in allowed_departments:

                st.write(
                    f"✓ {department.upper()}"
                )

            st.write(
                "Documents outside these domains "
                "are excluded from retrieval."
            )


        # -------------------------------------------------
        # AUDIT INFORMATION
        # -------------------------------------------------

        with st.expander(
            "📝 Privacy-Safe Audit Information"
        ):

            st.write(
                "This interaction has been recorded "
                "for security and auditing purposes."
            )

            st.write(
                "The audit log stores:"
            )

            st.write("✓ Employee role")
            st.write("✓ Privacy risk level")
            st.write("✓ Detected PII categories")
            st.write("✓ Number of retrieved sources")

            st.write(
                "**PrivateRAG does not store the "
                "question or detected PII values "
                "in the audit log.**"
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "PrivateRAG • Privacy-aware enterprise AI prototype • "
    "Synthetic demonstration data only"
)