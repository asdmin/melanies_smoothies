# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw: {st.__version__}")

name = st.text_input("Name")
st.write("Given Name:", name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Chose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

ingredients_string = ' '.join(ingredients_list)

if ingredients_list:
	for fruit_chosen in ingredients_list:
		st.subheader(fruit_chosen + ' Nutrition information')
		search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
		st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
		smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
		st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


insert_statement = "insert into SMOOTHIES.PUBLIC.ORDERS (name_on_order, ingredients) values ('" + name + "', '" + ingredients_string + "')"

submit = st.button('Submit Order');

if submit:
    session.sql(insert_statement).collect()
    st.success('ordered, dear ' +name)

