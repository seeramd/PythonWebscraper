# PythonWebscraper

A webscraper that parses the National Weather Service Website for temperature data in New York, NY. The data is saved to a csv, and also inserted in to a PostgresSQL database

Uses OOP to create a "data run" instance. The instance will collect data every user defined interval. The interval between scrapes is input by the user on execution. The collection run can be interrupted or stopped at any time in a tkinter window using <space> to interrupt and print the current plot, and <Esc> to stop collection. After stopping, the csv file is generated and the data is string formatted into an INSERT query for the SQL database.
