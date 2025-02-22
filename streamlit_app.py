# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The nameon your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingedrients:",
    my_dataframe,
    max_selections =5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)


    ingredients_string = ''
    for ingredient in ingredients_list:
        ingredients_string+=ingredient + " "
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    # st.write(my_insert_stmt)
    # st.stop()
    time_to_submit = st.button("Submit Order")

    
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success(f'✅ Your Smoothie is ordered, {name_on_order}! ')

