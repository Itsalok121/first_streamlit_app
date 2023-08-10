import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avancado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)


#streamlit.text(fruityvice_response.json())
streamlit.header('Fruityvice Fruit Advice!')
def get_fruitvice_date(this_fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information')
    else:
        streamlit.dataframe(get_fruitvice_date(fruit_choice))

except URLError as e:
    streamlit.error()




# write your own comment - what does this do?


streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * From pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
my_fruit_add = streamlit.text_input('What fruit would you like to add?')
streamlit.write('thanks for adding ', my_fruit_add)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')");