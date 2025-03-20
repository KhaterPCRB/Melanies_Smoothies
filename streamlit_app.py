# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")


# st.write(f"You selected: {Coption} ")
cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
name=st.text_input("Enter the Name for the Order")
ingredients_list= st.multiselect('Choose Up to 5 Ingredients', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients_string= ''
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen + ' '
        search_on= pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen,'SEARCH_ON'].iloc[0]
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #==================================
    st.write(f'Search Value for {fruit_chosen} is {search_on}.')
    st.subheader(fruit_chosen + " " + 'Nutriton Information')
    
    st.write(ingredients_string)
     
    insert_T= st.button('Submit Order')
    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredient_string, name_on_order) 
            values ('"""+ ingredient_string +"""','"""+ name +"""')"""
    
    st.write(my_insert_stmt)

    if insert_T:
        
        session.sql(my_insert_stmt).collect()
        st.success(f'Smoothie Ordered, {name}')

#===================

