# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

#===============
# Coption=st.selectbox(
#     'How would you like to be contacted ?',
#     ['Email', 'Home Phone', 'Mobile Phone']
# )   

# st.write(f"You selected: {Coption} ")
cnx= st.connect("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
name=st.text_input("Enter the Name for the Order")
ingredients_list= st.multiselect('Choose Up to 5 Ingredients', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients= ''
    
    for ing in ingredients_list:
        if ingredients == '':
            ingredients+= ing
        else:
            ingredients= ingredients +", " + ing
    
    st.write(ingredients)
 
    insert_T= st.button('Submit Order')
    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
            values ('""" + ingredients + """','"""+ name +"""')"""

    #st.write(my_insert_stmt)

    if insert_T:
        
        session.sql(my_insert_stmt).collect()
        st.success(f'Smoothie Ordered, {name}')

#===================

