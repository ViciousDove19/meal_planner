import streamlit as st
from openai import OpenAI

st.title("Mealplanner")
st.caption("Plan your weekly meals in an efficient manner.")

#utility functions
def generate_dynamic_prompt(template, **variables):
    """
    Generate a prompt by replacing placeholders with custom variables.
    
    Args:
        template (str): Prompt template with {variable} placeholders
        **variables: Keyword arguments to replace placeholders
    
    Returns:
        str: Fully populated prompt
    """
    try:
        return template.format(**variables)
    except KeyError as e:
        raise ValueError(f"Missing variable in template: {e}")


#take following intake requirements:
#calories
#protein
#protein sources

st.title("Input Processing Demo")

# User input sections
st.header("Enter Your Variables")

# Numeric input
calories_input = st.number_input("Enter calorie goal")
protein_input = st.number_input("Enter protein goal")
diet_type_input = st.text_input("Enter your diet type")
#protein_sources = st.text_input("Enter protein sources")



#function to generate the menu card and grocery list
#openai based prompt

meal_planner_template = """
    Come up with a weekly meal plan for a person in Bangalore.
    The person needs to complete {calories_requirement} calories every day.
    The person needs to consume {protein_requirement} grams of protein every day.
    The person's diet is {diet_type}.
    Return a menu for the entire week.
    """

generated_prompt = generate_dynamic_prompt(
            meal_planner_template,
            calories_requirement=calories_input,
            protein_requirement=protein_input,
            diet_type=diet_type_input
        )


client = OpenAI(
            # Assumes OPENAI_API_KEY is set in environment variables
            api_key='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'
        )
        
        # Make API call
response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": "You are a helpful nutrionist"},
                {"role": "user", "content": generated_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Extract and return the response text
result = (response.choices[0].message.content.strip())

#diplay grocery list and menu card
# Button to trigger processing
if st.button("Process Input"):
    # Validate inputs
    st.success(result)


