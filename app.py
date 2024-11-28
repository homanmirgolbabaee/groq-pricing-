import streamlit as st
import pandas as pd

# Updated LLM pricing data with corrected values
llm_pricing = {
    "Llama 3.2 1B (Preview) 8k": {
        "speed": 3100,
        "input_price": 0.04,  # 25M tokens per $1
        "output_price": 0.04   # 25M tokens per $1
    },
    "Llama 3.2 3B (Preview) 8k": {
        "speed": 1600,
        "input_price": 0.06,  # 17M tokens per $1
        "output_price": 0.06   # 17M tokens per $1
    },
    "Llama 3.1 70B Versatile 128k": {
        "speed": 250,
        "input_price": 0.59,  # 1.69M tokens per $1
        "output_price": 0.79   # 1.27M tokens per $1
    },
    "Llama 3.1 8B Instant 128k": {
        "speed": 750,
        "input_price": 0.05,  # 20M tokens per $1
        "output_price": 0.08   # 12.5M tokens per $1
    },
    "Llama 3 70B 8k": {
        "speed": 330,
        "input_price": 0.59,  # 1.69M tokens per $1
        "output_price": 0.79   # 1.27M tokens per $1
    },
    "Llama 3 8B 8k": {
        "speed": 1250,
        "input_price": 0.05,  # 20M tokens per $1
        "output_price": 0.08   # 12.5M tokens per $1
    },
    "Mixtral 8x7B Instruct 32k": {
        "speed": 575,
        "input_price": 0.24,  # 4.17M tokens per $1
        "output_price": 0.24   # 4.17M tokens per $1
    },
    "Gemma 7B 8k Instruct": {
        "speed": 950,
        "input_price": 0.07,  # 14.29M tokens per $1
        "output_price": 0.07   # 14.29M tokens per $1
    },
    "Gemma 2 9B 8k": {
        "speed": 500,
        "input_price": 0.20,  # 5M tokens per $1
        "output_price": 0.20   # 5M tokens per $1
    },
    "Llama 3 Groq 70B Tool Use Preview 8k": {
        "speed": 335,
        "input_price": 0.89,  # 1.12M tokens per $1
        "output_price": 0.89   # 1.12M tokens per $1
    },
    "Llama 3 Groq 8B Tool Use Preview 8k": {
        "speed": 1250,
        "input_price": 0.19,  # 5.26M tokens per $1
        "output_price": 0.19   # 5.26M tokens per $1
    },
    "Llama Guard 3 8B 8k": {
        "speed": 765,
        "input_price": 0.20,  # 5M tokens per $1
        "output_price": 0.20   # 5M tokens per $1
    }
}

def calculate_llm_cost(model, input_tokens, output_tokens):
    input_cost = (input_tokens / 1_000_000) * llm_pricing[model]["input_price"]
    output_cost = (output_tokens / 1_000_000) * llm_pricing[model]["output_price"]
    return input_cost + output_cost

st.title("LLM Pricing Calculator")

st.header("Model Selection and Usage")
llm_model = st.selectbox("Select LLM Model", list(llm_pricing.keys()))

# Add tokens per dollar information
selected_model = llm_pricing[llm_model]
st.write(f"Input tokens per $1: {1_000_000/selected_model['input_price']:,.2f}")
st.write(f"Output tokens per $1: {1_000_000/selected_model['output_price']:,.2f}")
st.write(f"Speed: {selected_model['speed']} tokens/second")

input_tokens = st.number_input("Input Tokens", min_value=0, value=1000000, step=100000)
output_tokens = st.number_input("Output Tokens", min_value=0, value=100000, step=10000)

llm_cost = calculate_llm_cost(llm_model, input_tokens, output_tokens)
st.write(f"Estimated LLM Cost: ${llm_cost:.4f}")

st.header("Pricing Analysis")
usage_frequency = st.selectbox("Usage Frequency", ["Per Request", "Hourly", "Daily", "Weekly", "Monthly"])
num_requests = st.number_input("Number of Requests", min_value=1, value=1, step=1)

if usage_frequency != "Per Request":
    total_cost = llm_cost * num_requests
    st.write(f"Total {usage_frequency} Cost: ${total_cost:.2f}")

    if usage_frequency == "Hourly":
        daily_cost = total_cost * 24
        monthly_cost = daily_cost * 30
    elif usage_frequency == "Daily":
        monthly_cost = total_cost * 30
    elif usage_frequency == "Weekly":
        monthly_cost = total_cost * 4
    else:  # Monthly
        monthly_cost = total_cost

    st.write(f"Estimated Monthly Cost: ${monthly_cost:.2f}")

    markup = st.slider("Markup Percentage", min_value=0, max_value=200, value=30)
    suggested_price = monthly_cost * (1 + markup/100)
    st.write(f"Suggested Monthly Price (with {markup}% markup): ${suggested_price:.2f}")

st.header("Model Comparison")
comparison_df = pd.DataFrame(llm_pricing).T
comparison_df = comparison_df.reset_index().rename(columns={"index": "Model"})
comparison_df["Input Price (per 1M tokens)"] = comparison_df["input_price"].apply(lambda x: f"${x:.2f}")
comparison_df["Output Price (per 1M tokens)"] = comparison_df["output_price"].apply(lambda x: f"${x:.2f}")
comparison_df["Speed (tokens/sec)"] = comparison_df["speed"]
comparison_df["Tokens per $1 (Input)"] = comparison_df["input_price"].apply(lambda x: f"{1_000_000/x:,.0f}")
comparison_df["Tokens per $1 (Output)"] = comparison_df["output_price"].apply(lambda x: f"{1_000_000/x:,.0f}")
comparison_df = comparison_df[["Model", "Speed (tokens/sec)", "Input Price (per 1M tokens)", "Output Price (per 1M tokens)", "Tokens per $1 (Input)", "Tokens per $1 (Output)"]]
st.dataframe(comparison_df)

st.header("Notes")
st.write("- All prices and calculations are based on per million tokens")
st.write("- Speeds are theoretical maximums and may vary based on actual usage")
st.write("- Consider other costs such as infrastructure, development, and support for pricing")