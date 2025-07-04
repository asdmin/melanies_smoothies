# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw: {st.__version__}")

name = st.text_input("Name")
st.write("Given Name:", name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Chose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

ingredients_string = ' '.join(ingredients_list)

insert_statement = "insert into SMOOTHIES.PUBLIC.ORDERS (name_on_order, ingredients) values ('" + name + "', '" + ingredients_string + "')"

submit = st.button('Submit Order');

if submit:
    session.sql(insert_statement).collect()
    st.success('ordered, dear ' +name)

