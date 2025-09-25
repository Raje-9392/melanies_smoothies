# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write(
  """Choose the fruit you want in your custom Smoothie
  """)
cnx = st.connection("snowflake")
session=cnx.session()


#import streamlit as st

#title = st.text_input('Movie title', 'Life of Brian')
#st.write('The current movie title is', title)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)




#option = st.selectbox( 'What is your favorite fruit?',('Banana', 'Strawberries', 'Peaches')
#)

#st.write('Your favorite fruit is:', option)
from snowflake.snowpark.functions import col

#session = get_active_session()
st.write("Session initialized:", session)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect( 'chose up to 5 imgredients:',my_dataframe)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
   # st.write(ingredients_string)    
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
   # st.write(my_insert_stmt)
    #st.stop()

    #st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()


#st.cache_data.clear()
















    
