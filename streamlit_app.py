import pandas
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError

streamlit.header("🍌🥭 ADAICHIE'S NEW APP🥝🍇")
streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

#import pandas
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(my_fruit_list)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#import streamlit
#create the repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized
#New section to display fruityvice api response

streamlit.header("The fruit load list contains:")
#snowflake-related function
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from fruit_load_list")
            return my_cur.fetchall()           

#Allow the end user to add a fruit to the list   
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list VALUES (%s)", (new_fruit,))
        return "Thanks for adding " + new_fruit

#Add a button to load the fruit
if streamlit.button('Get Fruit List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)
            
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

streamlit.stop()
