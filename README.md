# Statboard
Statboard is a simple web application using django that lets you track custom statistics
of your choice. It is designed to be a simple and easy to use tool for tracking number
based statistics. (eg, 500 miles driven, 10000 words written, etc.)<br>

Originally, this is a program I designed for myself in use of my personal life, but I
decided to make it public for anyone who may find it useful.

## Features
- Add custom statistics
- View statistics over a span of a week
- Can add or subtract from a statistic at any time by entering a new entry for that date
- View the conditions of existence for a statistic (see below)

## Installation
This installation assumes you have python3.12 installed already
1. Clone the repository
2. Create a virtual environment using `python3.12 -m venv venv`
3. Activate the virtual environment using `source venv/bin/activate` or `venv\Scripts\activate` on windows
4. Install the required packages using `pip install -r requirements.txt`
5. execute "python webui/manage.py migrate"
6. execute "python app.py -O"
7. Open a browser and navigate to `http://127.0.0.1:8000/` to view the application

## Roadmap
- Add password protection (to the site, not meant to be used by multiple users)
- Add a way to reset the statistics for a given day
- Fully implement the "Statistic view" page to view a specific statistic, and its
status in the "conditions of existence" table

## Conditions of existence
The conditions of existence are the various states that a statistic can be in.
They are:
- **Power**: The statistic is consistently at the top of the range
- **Affluence**: The statistic is widely above the average value
- **Normal**: The statistic is slightly up from the average value
- **Emergency**: The statistic is slightly down, or a steady line compared to the average value<br>
You'll find a statistic in 'emergency' will ALWAYS drop to 'danger' if it goes unhandled.
- **Danger**: The statistic is widely below the average value
- **Non-existence**: The statistic exists, but is so low that its flat-lined.

Each of these conditions of existence will have a pre-defined handling method
as provided by the writer L. Ron Hubbard in his book on the topic of Ethics.