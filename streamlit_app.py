# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get Snowflake session
session = get_active_session()

# Load the fruit list
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Multi-select fruit list
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# If user picked ingredients
if ingredients_list:

    # Build ingredients string
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    # Fix INSERT statement (2 columns!)
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Button
    submit_clicked = st.button("Submit Order")

    # If button clicked → insert + show message
    if submit_clicked:
        #session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
