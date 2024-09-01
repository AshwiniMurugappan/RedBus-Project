# RedBus-Project

## Redbus Data Scraping and Filtering with Streamlit Application

  The "Redbus Data Scraping and Filtering with Streamlit Application" is designed to streamline the process of gathering and analyzing bus travel data. 
By leveraging web scraping techniques and the interactive capabilities of Streamlit, this application offers a valuable tool for researchers, analysts, and travelers alike.

## Key features and benefits include:

### Efficient data collection: 
Automated scraping of Redbus data, eliminating the need for manual input and saving time.
### Customizable filtering: 
Users can refine their search based on various criteria, such as bus routes, cities, prices and more.
### Interactive visualization: 
Streamlit provides a user-friendly interface for exploring and visualizing the collected data, enabling easy identification of trends and patterns.
### Data-driven insights: 
The application can be used to generate valuable insights into bus travel patterns, pricing trends, and customer preferences.

## 1. Web Scraping with Selenium:

### Code Breakdown:

  **Imports**: Necessary libraries for web scraping (Selenium), waiting (WebDriverWait), handling exceptions (from selenium.common.exceptions), data manipulation (pandas), and user interaction (ActionChains).List of URLs for different state transport corporations on Redbus.
  **routedata**: Empty list to store scraped route data.
  **Looping through state URLs**: Iterates over each state bus URL. Navigates to the current state bus URL. Creates a WebDriverWait object for handling dynamic elements.
  **Function**: Defines a function to scrape routes from the current page. Uses WebDriverWait to wait for all elements with the class "route" to be present. Loops through each route element, Extracts route name, Extracts route link, and Appends data
  **Looping through page**s: Iterates from page 1 to 5 (inclusive) of the current state bus URL. Prints a message indicating which page is being scraped.
Calls route_page() to scrape routes from the current page.
  **Pagination handling**: Tries to find the pagination container using XPath. If found, it finds the next page button element based on its text content (page number). Uses ActionChains to move to the next page button and click it.
  **df creation**: Creates a pandas DataFrame from the scraped routedata list.
  
### Scraping Loop:

  **bus_details**: Empty list to store scraped bus details dictionaries. Iterates over items in routedata, Extracts route_link and route_name from the current item. Opens the route_link in the Chrome browser using driver.get(route_link).
  **Handling Government Buses**: Tries to find an element with the class button, If found, clicks the element and waits for 2 seconds.
  **Scrolling Down the Page**: Sets scrolling to True to initiate a loop for scrolling.
Loops until scrolling becomes False.
  **Scrape_bus_details Function**: This function extracts details about individual buses displayed on the page. Extracts various details like bus name, type, departure time, duration, reaching time, star rating (if available), price, and seat availability using XPaths within the current bus element. Appends the extracted details as a dictionary to the bus_details list.
  **Data Storage**: Closes the Chrome browser. Creates a pandas DataFrame data from the list of scraped bus details dictionaries bus_details.
Saves the DataFrame to a CSV file named RB_bus_details.csv using to_csv().

## 2. Data Processing and Storage:

**Clean and process scraped data**: 
  Handle missing values, inconsistencies, etc, and normalizing data.

**Store data in a database**: 
  Use MySQL to connect to database and insert data.

**Functions**: 
  Executes the SQL statement to retrieve all data from the "bus_details" table. Returns the fetched data as a list of tuples.
  -> Retrieves all columns and rows from the "bus_details" table. 
  -> Retrieves all columns and rows from the "routes" table.

**Purpose:**
  These functions are likely used to retrieve data from a database containing information about bus routes, their details, and their popularity. The data can then be used in a Streamlit application to provide users with information about bus routes, their details, and popular cities.


  
## 3. Project Setup:

**Import Statements:**
 Imported the Streamlit, Pandas, mysql.connector,Plotly Express,streamlit_option_menu library for creating web applications, and query.py module, which contains functions for interacting with the database.
 
**Page Configuration, Image and Title:**
 Sets the title of the Streamlit app to "RedBus App". Displayed an image at the top of the page.
 
**Database Interaction and Data Retrieval:**
 Calls function from the query.py module to retrieve data from the database. Created a pandas DataFrame from the retrieved data using the column names.

**Sidebar:**
 Displayed an image in the sidebar with the caption "Redbus Web App". Created a multiselect widget in the sidebar allowing users to select multiple bus route names.

**Data Filtering and Display:**
 Filters the DataFrame df based on the selected bus route names. Defined a function to display the home page content.
Created four columns to display the top 3 popular bus names, bus types, average price, and average star rating.
Defined a function to display a table of the filtered data. Created an expander which allows users to select columns to display the selected columns in a DataFrame.

**Sidebar Menu:**
 Created a sidebar container with options "Home", "Route Links", "Dashboard", and "Popular Cities". The selected option is stored in the menu variable.

**Conditional Execution:**
 Selected menu option executes the functions of displaying table, route links creates two charts using Plotly and retrieves data on popular cities, creates a line chart and a pie chart using Plotly, and displays them.



