# Import python packages
import streamlit as st
import requests
import pandas as pd
streamlit run streamlit_app.py
smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/all")

#from snowflake.snowpark import Session
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write(
  """Choose the fruit you want in your custom Smoothie
  """)
cnx = st.connection("snowflake")
session=cnx.session()

#import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df = st.dataframe(
    #data=smoothiefroot_response.json(),
    #use_container_width=True
#)

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)                                                                                         
#st.stop()
                                                                                            
ingredients_list=st.multiselect('chose up to 5 imgredients:',my_dataframe,max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition information')
        fruitvice= requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen+search_on)
        fv_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
       # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        #sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
   #st.write(ingredients_string)    

ingredients_string = "Apples,Lime,Ximenia "   
name_on_order = "Kevin "

ingredients_string = "Dragon Fruit, Guava,Figs, Jackfruit and Blueberries  "   
name_on_order = " Divya "

ingredients_string = " Vanilla Fruit,Nectarine  "   
name_on_order = "Xi  "
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
         values('""" + ingredients_string + """','"""+name_on_order+ """')"""
   # st.write(my_insert_stmt)
    #st.stop()


    #st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()


#st.cache_data.clear()











    
