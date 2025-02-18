# 🚌 Dublin Bus App

**The Dublin Bus App has been built in an attempt to use real time data using the API's provided by the [National Transport Authority](https://developer.nationaltransport.ie/). Using this app you can see the incoming buses for a selected stop and the buses that currently operate a route based on a direction.**

---

## 🧬 **Project Structure**
```bash
DublinBusApp
├── assets/         
│   ├── data/
│   │   ├── Routes.txt
│   │   ├── StopMapLocation.txt
│   │   ├── StopTimesPerTrip.txt
│   │   └── Towards.csv
│   ├── dataCleaning/
│   │   ├── 00_EndpointExploration.ipynb
│   │   ├── 01_DataCleaning.ipynb
│   │   ├── 02_Flow_01_⌚_StopTimes.ipynb
│   │   ├── 03_Flow_02_📍_BusLocator.ipynb
│   │   ├── routes.txt
│   │   ├── stop_times.txt
│   │   ├── stops.txt
│   │   └── trips.txt
│   ├── gifs/
│   │   ├── BusLocator.gif
│   │   └── StopTimes.gif
│   └── images/ 
│       ├── bus.png
│       ├── dublin_bus_favicon.png
│       ├── dublin_bus_logo.png
│       ├── pin_blue.png
│       ├── pin_green.png
│       ├── pin_red.png
│       └── tfi_logo.png
├── streamlit_app/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── BLutils.py
│   │   ├── DataPrep.py
│   │   ├── STutils.py
│   │   └── Styles.py
│   ├── pages/               
│   │   ├── 01_⌚_StopTimes.py
│   │   └── 02_📍_BusLocator.py
│   └── 00_🚌_Info.py     
├── LICENSE                 
├── README.md               
└── requirements.txt        
```

---

## 🎯 **Road Map**

  

Plan to develop the app:

  

- **Understand the data provided by the APIs**

- **Explore the static data provided by the NTA to complement data shown in the APIs**

- **Design the logic for `StopTimes` and `BusLocator` pages**

---
  

## 🏗️ **Deployment**

  

1. **Understand the data provided by the APIs**:

- First, sign up for the [National Transport Authority (NTA)](https://developer.nationaltransport.ie/) to access their APIs. Use the following link to sign up: [Sign up here](https://developer.nationaltransport.ie/signup).

- Next, understand and visualise the data provided by the following endpoints:

- [GTFSR Endpoint](https://api.nationaltransport.ie/gtfsr/v2/gtfsr?format=json)

- [Vehicles Endpoint](https://api.nationaltransport.ie/gtfsr/v2/Vehicles?format=json)

- To assist with exploring these endpoints, I have created a Jupyter Notebook (JN): [00_EndpointExploration.ipynb](https://github.com/josericodata/DublinBusApp/blob/main/assets/dataCleaning/00_EndpointExploration.ipynb). Replace `os.environ.get("API_KEY")` with the variable `YOUR_API_KEY`, and you're ready to proceed.

  

2. **Exploring and Preparing NTA Dublin Bus Static Data**:

- Please head over to the following link: [GTFS Dublin Bus Data](https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip). This will download the file `GTFS_Dublin_Bus.zip`. After downloading, extract the files.

- We will need the following files from the extracted data:

1. `routes.txt`

2. `stops.txt`

3. `stop_times.txt`

4. `trips.txt`

- These files will be used to generate the following new files:

1. `Routes.txt`

2. `StopMapLocation.txt`

3. `StopTimesPerTrip.txt`

4. `Towards.txt`

- To visualise this step, I have created a JN: [01_DataCleaning.ipynb](https://github.com/josericodata/DublinBusApp/blob/main/assets/dataCleaning/01_DataCleaning.ipynb).

- **The files mentioned above were used in the early stages of this project. However, since the NTA updates `GTFS_Dublin_Bus.zip` almost every week, maintaining the app required frequent updates. To simplify this process, I created [DataPrep.py](https://github.com/josericodata/DublinBusApp/blob/main/streamlit_app/modules/DataPrep.py). With this script, every time the app runs, it fetches fresh data from [GTFS Dublin Bus Data](https://www.transportforireland.ie/transitData/Data/GTFS_Dublin_Bus.zip). I am keeping the old `.txt` files in case they help someone better understand this complex process.**

3. **What is GTFS?**

- Summarising point 1 and 2 the **General Transit Feed Specification (GTFS)** is a standardised format for public transportation data, allowing transit agencies to share schedules, routes, and real-time updates. It consists of structured text files (CSV format) that define agencies, stops, routes, trips, and schedules.

**GTFS Data Types:**

- **GTFS Realtime**: Delivers live updates on vehicle positions, delays, and service alerts. `GTFSR` and `Vehicles` endpoints.
- **GTFS Static**: Provides fixed schedules, routes, and stop locations. `GTFS_Dublin_Bus.zip`.

- For more details, visit the official GTFS website: [GTFS.org](https://gtfs.org/)


4. **Logic Design for `StopTimes` and `BusLocator` Pages**:

- After understanding the data provided by the endpoints and the static files, it is time to develop the logic for the pages.

- **`StopTimes` Page**:

- The user will first select a `route`, then be prompted to choose a `direction`, and finally select a `stop` to display the buses that are due to arrive.

- For a clear understanding of this flow, refer to the JN: [02_Flow_01_⌚_StopTimes.ipynb](https://github.com/josericodata/DublinBusApp/blob/main/assets/dataCleaning/02_Flow_01_⌚_StopTimes.ipynb).

- **`BusLocator` Page**:

- This page will show the operating buses for the selected `route` and `direction`.

- For more details on this logic, refer to the JN: [03_Flow_02_📍_BusLocator.ipynb](https://github.com/josericodata/DublinBusApp/blob/main/assets/dataCleaning/03_Flow_02_📍_BusLocator.ipynb).

---

5. **Streamlit App Creation**:

- After completing the steps above, the final app can be found at: [streamlit_app](https://github.com/josericodata/DublinBusApp/tree/main/streamlit_app).

  

## 🚀 **Getting Started**

  

### **Local Installation**

  

1. Clone the repository:

```bash

git clone https://github.com/user/DublinBusApp.git

```

**Hint:** Replace `user` with `josericodata` in the URL above. I am deliberately asking you to pause here so you can support my work. If you appreciate it, please consider giving the repository a star or forking it. Your support means a lot—thank you! 😊

  

2. Navigate to the project directory:

```bash

cd DublinBusApp

```

  

3. Create a virtual environment:

```bash

python3 -m venv venvDublinBus

```

  

4. Activate the virtual environment:

```bash

source venvDublinBus/bin/activate

```

  

5. Install requirements:

```bash

pip install -r requirements.txt

```

  

6. Navigate to the modules directory:

```bash

cd streamlit_app/modules

```

  

7. Please locate in `BLutils.py` and `STutils.py` the following line code:

```bash

YOUR_API_KEY = st.secrets["API_KEY"]

```

It is crutial to replace `st.secrets["API_KEY"]` with the actual API Key provided by the [National Transport Authority](https://developer.nationaltransport.ie/) after [signing up](https://developer.nationaltransport.ie/signup) to acces their APIs. Please use the following link to sign up: https://developer.nationaltransport.ie/signup

  
  

8. Go back one directory and run the app:

```bash

cd ..

```

  

Then run

  

```bash

streamlit run 00_🚌_Info.py

```

  

The app will be live at `http://localhost:8501`.

---

## 🎬 **Demo**
  
### Page 1: Stop Times
![Stop Times Demo](assets/gifs/StopTimes.gif)

### Page 2: Bus Locator
![Bus Locator Demo](assets/gifs/BusLocator.gif)

---

## 🔮 **Future Enhancements**

  

Planned improvements for the Dublin Bus App include:

  

- **Database Integration**: Implementing a relational database (e.g., PostgreSQL) to better manage and query data, enabling faster performance and enhanced data relationships between routes, stops, and trips.

- **Historical Data Storage**: Storing historical bus data to provide insights like delay trends, busiest stops, and more accurate arrival time predictions using machine learning.

- **Personalised Features**: Adding user-specific data storage, such as favorite routes or frequently accessed stops, for a more tailored experience.

- **Advanced Reporting and Analytics**: Generating detailed reports, such as route popularity or stop traffic trends, with visualisations like heatmaps or charts.

- **Enhanced Pages**: Introducing new pages and features, including route performance tracking, user feedback collection, and real-time bus location improvements.

- **Scalability**: Preparing the app for multi-user support by efficiently handling concurrent queries through the database.

--- 
  

## 🎓 **Motivation**

  

- The motivation behind developing this app is to gain hands-on experience in working with JSON-formatted data from real-time APIs. As a resident of Ireland, I found Dublin Bus data particularly convenient, as I am familiar with many of the routes, buses, and stops.

- Additionally, this project helps me stay up to date with my skills while serving as a valuable addition to my portfolio, showcasing my abilities in handling and processing data effectively.

--- 

## 🔧 **Environment Setup**

  

This app has been built and tested in the following environment:

  

- **Operating System**: Ubuntu 22.04.5 LTS (Jammy)

- **Python Version**: Python 3.10.12

---
  

## 🤝 **Open Pull Requests**

If you find any bug, feel free to contact me by opening a pull request on GitHub or via email at **maninastre@gmail.com**.

---

## ⚠️ **Disclaimer**

  

This app was developed for my portfolio and demonstration purposes only. The results are not guaranteed to be error-free and should not be used for critical decision-making.

<p align="center">
    <a href="https://www.dublinbus.ie/" target="_blank">
        <img src="/assets/images/dublin_bus_logo.png" alt="Dublin Bus Logo" width="200">
    </a><br>
    <a href="https://www.transportforireland.ie/" target="_blank">
        <img src="/assets/images/tfi_logo.png" alt="TFI Logo" width="200">
    </a>
</p>