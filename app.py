# ==========================================================
# Project Name: AquaPrompt
# Description: A beginner-friendly Streamlit web app that calculates
#              the estimated water footprint of AI prompts and optimizes
#              them by removing conversational filler words.
# ==========================================================

# Step 1: Import the Streamlit library so we can create a web interface
import streamlit as st

# Step 2: Configure page title and browser tab icon
st.set_page_config(page_title="AquaPrompt", page_icon="💧")

# Step 3: Display the app header and introduction
st.title("💧 AquaPrompt")
st.subheader("Measure and Reduce the Water Footprint of Your AI Prompts")
st.write(
    "Data centers consume large amounts of freshwater for cooling when running AI models. "
    "AquaPrompt helps you estimate how much water your prompt uses and simplifies it to save resources!"
)

# Step 4: Create a text box where the user can paste or type their prompt
user_prompt = st.text_area(
    label="Paste your AI prompt below:",
    placeholder="e.g., Can you please kindly summarize this article for me, um, as soon as possible?",
    height=150
)

# Step 5: Check if the user entered any text
if len(user_prompt.strip()) > 0:

    # ---------------------------------------------------------
    # PART A: TOKEN & WATER FOOTPRINT CALCULATION
    # ---------------------------------------------------------

    # 1. Count the number of characters in the user's prompt
    character_count = len(user_prompt)

    # 2. Estimate tokens: Industry standard rule of thumb is ~4 characters per token
    estimated_tokens = round(character_count / 4)

    # 3. Water usage metric: Roughly 0.002 mL of cooling water per token
    # (Based on average AI data-center cooling consumption metrics)
    water_multiplier = 0.002
    estimated_water_ml = estimated_tokens * water_multiplier

    # 4. Display the metrics side-by-side using columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Character Count", value=character_count)

    with col2:
        st.metric(label="Estimated Tokens", value=estimated_tokens)

    with col3:
        # Display the water footprint formatted to 4 decimal places
        st.metric(label="Estimated Water Used", value=f"{estimated_water_ml:.4f} mL")

    st.write("---")

    # ---------------------------------------------------------
    # PART B: PROMPT OPTIMIZATION (FILLER WORD REMOVER)
    # ---------------------------------------------------------

    st.subheader("🛠️ Prompt Optimizer")
    st.write("Click the button below to remove filler words and make your prompt eco-friendly.")

    # A button that triggers the text-cleaning code when clicked
    if st.button("Clean & Optimize Prompt"):

        # Start with a copy of the original prompt text
        cleaned_prompt = user_prompt

        # A list of common conversational filler words and phrases to remove
        filler_words = [
            "can you please",
            "could you please",
            "would you kindly",
            "can you",
            "could you",
            "please",
            "kindly",
            "um",
            "uh",
        ]

        # Loop through each filler phrase and remove it using .replace()
        for word in filler_words:
            # Replace lowercase version
            cleaned_prompt = cleaned_prompt.replace(word.lower(), "")
            # Replace capitalized version
            cleaned_prompt = cleaned_prompt.replace(word.capitalize(), "")
            # Replace uppercase version
            cleaned_prompt = cleaned_prompt.replace(word.upper(), "")

        # Clean up any leftover double spaces and trim edges
        cleaned_prompt = cleaned_prompt.replace("  ", " ").strip()

        # Recalculate metrics for the newly cleaned prompt
        cleaned_characters = len(cleaned_prompt)
        cleaned_tokens = round(cleaned_characters / 4)
        cleaned_water_ml = cleaned_tokens * water_multiplier

        # Calculate exact savings
        tokens_saved = estimated_tokens - cleaned_tokens
        water_saved_ml = estimated_water_ml - cleaned_water_ml

        # Show the result to the user
        st.success("Prompt successfully optimized!")
        st.write("**Optimized Prompt:**")
        st.text_area(label="Cleaned version:", value=cleaned_prompt, height=100)

        # Show side-by-side comparison metrics showing savings
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(
                label="New Water Footprint",
                value=f"{cleaned_water_ml:.4f} mL",
                delta=f"-{water_saved_ml:.4f} mL Saved",
                delta_color="inverse"
            )
        with res_col2:
            st.metric(
                label="New Token Count",
                value=cleaned_tokens,
                delta=f"-{tokens_saved} Tokens",
                delta_color="inverse"
            )

else:
    # Helpful message shown when the text box is empty
    st.info("👆 Please paste or type a prompt above to see its estimated water footprint.")