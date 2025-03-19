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
#st.dataframe(pd_df)
name=st.text_input("Enter the Name for the Order")
ingredients_list= st.multiselect('Choose Up to 5 Ingredients', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients= ''
    for ing in ingredients_list:
        if ingredients == '':
            ingredients+= ing
        else:
            ingredients= ingredients +", " + ing
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +ing)
    s_o= pd_df.loc[pd_df['FRUIT_NAME'] == ing,'SEARCH_ON'.iloc[0]]
    st.write(f'Search Value for {ing} is {s_o}.')
    st.subheader(ing + 'Nutriton Information')
    
    sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients)
 
    insert_T= st.button('Submit Order')
    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
            values ('""" + ingredients + """','"""+ name +"""')"""

    #st.write(my_insert_stmt)

    if insert_T:
        
        session.sql(my_insert_stmt).collect()
        st.success(f'Smoothie Ordered, {name}')

#===================

