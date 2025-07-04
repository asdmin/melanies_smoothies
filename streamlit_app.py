# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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

ingredients_string = ' '.join(ingredients_list)

if ingredients_list:
	for fruit_chosen in ingredients_list:
		st.subheader(fruit_chosen + ' Nutrition information')
		smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
		st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


insert_statement = "insert into SMOOTHIES.PUBLIC.ORDERS (name_on_order, ingredients) values ('" + name + "', '" + ingredients_string + "')"

submit = st.button('Submit Order');

if submit:
    session.sql(insert_statement).collect()
    st.success('ordered, dear ' +name)

