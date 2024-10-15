import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import time

# kerala bus
lists_K=[]
df_K=pd.read_csv("kerala_bus_details.csv")
for i,r in df_K.iterrows():
    lists_K.append(r["Route_Name"])

#Andhra bus
lists_A=[]
df_A=pd.read_csv("ap_bus_details.csv")
for i,r in df_A.iterrows():
    lists_A.append(r["Route_Name"])

#Telungana bus
lists_T=[]
df_T=pd.read_csv("telegana_bus_details.csv")
for i,r in df_T.iterrows():
    lists_T.append(r["Route_Name"])

#kadamba bus
lists_G=[]
df_G=pd.read_csv("kadamba_bus_details.csv")
for i,r in df_G.iterrows():
    lists_G.append(r["Route_Name"])

#Rajastan bus
lists_R=[]
df_R=pd.read_csv("rajasthan_bus_details.csv")
for i,r in df_R.iterrows():
    lists_R.append(r["Route_Name"])


# chandigarh
lists_C=[]
df_C=pd.read_csv("chandigarh_bus_details.csv")
for i,r in df_C.iterrows():
    lists_C.append(r["Route_Name"])

# Himachal bus
lists_H=[]
df_H=pd.read_csv("himachal_bus_details.csv")
for i,r in df_H.iterrows():
    lists_H.append(r["Route_Name"])

#Assam bus
lists_AS=[]
df_AS=pd.read_csv("assam_bus_details.csv")
for i,r in df_AS.iterrows():
    lists_AS.append(r["Route_Name"])

#jammu bus
lists_J=[]
df_J=pd.read_csv("jk_bus_details.csv")
for i,r in df_J.iterrows():
    lists_J.append(r["Route_Name"])

#West bengal bus
lists_WB=[]
df_WB=pd.read_csv("wb_bus_details.csv")
for i,r in df_WB.iterrows():
    lists_WB.append(r["Route_Name"])

#setting up streamlit page
slt.set_page_config(layout="wide")

web=option_menu(menu_title="🚌OnlineBus",
                options=["Home","📍States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )
# Home page setting
if web=="Home":
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:]  Transportation")
    slt.subheader(":blue[Objective:] ")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    slt.subheader(":blue[Overview:]") 
    slt.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data...")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.subheader(":blue[Skill-take:]")
    slt.markdown("Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    slt.subheader(":blue[Developed-by:] nagabharathi")

# States and Routes page setting
if web == "📍States and Routes":
    S = slt.selectbox("Lists of States", ["Kerala", "Andhra Pradesh", "Telegana", "kadamba", "Rajastan", 
                                          "Chandigarh", "Himachal", "Assam", "Jammu", "West Bengal"])
    
    col1,col2=slt.columns(2)
    with col1:
        select_type = slt.radio("Choose Bus_Type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_Price = slt.radio("Choose Price range", ("50-1000", "1000-2000", "2000 and above"))
    TIME=slt.time_input("select the time")

    # Kerala bus fare filtering
    if S == "Kerala":
        K = slt.selectbox("List of routes",lists_K)

        def type_and_Price_K(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{K}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_K(select_type, select_Price)
        slt.dataframe(df_result)

    # Andhra Pradesh bus fare filtering
    if S=="Andhra Pradesh":
        A=slt.selectbox("list of routes",lists_A)

        def type_and_Price_A(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{A}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_A(select_type, select_Price)
        slt.dataframe(df_result)
          

    # Telugana bus fare filtering
    if S=="Telegana":
        T=slt.selectbox("list of routes",lists_T)

        def type_and_Price_T(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{T}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_T(select_type, select_Price)
        slt.dataframe(df_result)

    # kadamba bus fare filtering
    if S=="kadamba":
        G=slt.selectbox("list of routes",lists_G)

        def type_and_Price_G(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{G}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_G(select_type, select_Price)
        slt.dataframe(df_result)

    # Rajastan bus fare filtering
    if S=="Rajastan":
        R=slt.selectbox("list of routes",lists_R)

        def type_and_Price_R(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{R}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_R(select_type, select_Price)
        slt.dataframe(df_result)
          

    # chandigarh bus fare filtering       
    if S=="Chandigarh":
        C=slt.selectbox("list of routes",lists_C)

        def type_and_Price_C(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{C}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_C(select_type, select_Price)
        slt.dataframe(df_result)
    
    # Himachal bus fare filtering
    if S=="Himachal":
        H=slt.selectbox("list of routes",lists_H)

        def type_and_Price_H(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{H}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_H(select_type, select_Price)
        slt.dataframe(df_result)


    # Assam bus fare filtering
    if S=="Assam":
        AS=slt.selectbox("list of routes",lists_AS)

        def type_and_Price_AS(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{AS}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_AS(select_type, select_Price)
        slt.dataframe(df_result)

    # jammu bus fare filtering
    if S=="Jammu":
        J=slt.selectbox("list of routes",lists_J)

        def type_and_Price_J(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{J}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_J(select_type, select_Price)
        slt.dataframe(df_result)

    # West Bengal bus fare filtering
    if S=="West Bengal":
        WB=slt.selectbox("list of routes",lists_WB)

        def type_and_Price_WB(Bus_Type, Price_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="naga", database="RED_BUS_DETAILS")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if Price_range == "50-1000":
                Price_min, Price_max = 50, 1000
            elif Price_range == "1000-2000":
                Price_min, Price_max = 1000, 2000
            else:
                Price_min, Price_max = 2000, 100000  

            # Define bus type condition
            if Bus_Type == "sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%Sleeper%'"
            elif Bus_Type == "semi-sleeper":
                Bus_Type_condition = "Bus_Type LIKE '%A/c Semi Sleeper %'"
            else:
                Bus_Type_condition = "Bus_Type NOT LIKE '%Sleeper%' AND Bus_Type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM busdetails 
                WHERE Price BETWEEN {Price_min} AND {Price_max}
                AND Route_Name = "{WB}"
                AND {Bus_Type_condition} AND Departing_Time>='{TIME}'
                ORDER BY Price and Departing_Time  DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Route_Name","Route_Link","Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time",
                "Star_Rating","Price","Seat_Availability"
            ])
            return df

        df_result = type_and_Price_WB(select_type, select_Price)
        slt.dataframe(df_result)


