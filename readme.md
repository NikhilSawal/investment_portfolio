# Investment Portfolio

## 1. Overview

This is an end-to-end implementation that tries to cover several aspects of a machine learning project life-cycle. This project is my attempt to learn various technologies required for Data Science/Machine Learning and grow as a full stack Machine Learning Engineer. Through this project I have tried to cover 4 aspects of DS/ML project:

1. Data collection/extraction (web scraping)  **----> ```[COMPLETE]```**
2. Data storage                               **----> ```[COMPLETE]```**
3. Continuous integration                     **----> ```[IN-PROGRESS]```**
4. EDA, Visualization, model building & evaluation **----> ```[IN-PROGRESS]```**

## 2. Problem Statement

Coming up with innovative techniques to predict the market accurately, has become increasingly important given the uncertain times we live in. Through this project I want to emphasize on two broad categories of Machine Learning problems to test the following hypothesis:
- **Time series forecasting:** Can a rich storage of data help us predict important aspects of the stock market?
- **Natural language processing:** Can we use news data to model the impact of certain keywords on the trends of stocks belonging to different sector/industries?

## 3. Motivation

The idea for this project, struck me when we were hit by the pandemic in early 2020. I used to work for a gift cards selling company i.e [Raise Marketplace.](https://www.raise.com/) that acquired gift cards from over 3000 brands and sold them on its marketplace. The business was heavily impacted because of the pandemic, since a huge chunk of the companies revenue came from the travels & hotels industry.

- What if we had access to external data like news headlines? Could we have modeled the impact of the pandemic on several industries through their stock prices and made informed decisions about our acquisition strategies?

- Can we start storing information like news data and model the impact of a few key words to different industries, so that if a similar situation were to happen in the future, we can have a backup?

## 4. Current Stage of Project

- Three python scripts are currently operational that scrape different sets of data from **yahoo finance**.
- A  **cronjobs** is set to schedule these scrape & load the transformed data into Postgres.
- The data from the scrape is first stored to 3 **.jl via: stock_prices.jl, index.jl, company_profile.jl** files which are subsequently piped to a Postgres Database.
- A Slackbot then sends job notifications to my slack channel for handling errors.

> Current technologies: Python, Scrapy, Slack (for notifications), Cronjob, PostgreSQL, GIT

> Future technologies: Docker, Jenkins, Plotly/Flask, (Tensorflow/Keras/PyTorch)

*Figure 1* shows detailed representation of the project architecture.
1. **WEB SCRAPING:**  
The orange boxes are Scrapy spiders written in Python that go on Yahoo Finance !! scrape three sets of information related to stock prices and store them in separate files (json lines). All scrapes are currently scheduled using ```cron``` and the frequency is every hour on business days from 8:00 am - 4:00 pm (CST)

2. **Transform:**  
Some amount of data cleaning is performed like using regex to send clean numbers. The 3 green boxes are 3 separate files that store the scraped data in json lines format. All information related to data collected is shown in ```Figure 2```

| ![Project Architecture](misc_files/Picture1.png) |
|:--:|
| *Figure 1: Project Architecture* |

3. **Load:**  
A postgres database is created using the python package ```psycopg2``` that provides a pythonic interface perform SQL operations like ```CREATING database/tables, ALTERING information, INSERT/UPSERT operations```. The credentials needed to establish connections are stored as environment variables in ```~/.bash_profile``` script.

4. **Virtual Environment:**  
All the operations until the load stage are packaged into a virtual environment that uses ```Python --version 3.8.7```. The green dashed line in ```Figure 1``` represents the virtual environment. A ```requirements.txt``` is also generated that store the versions of dependancies used for the application.

| <img src="misc_files/investment_db.png" alt="drawing" width="1000"/> |
|:--:|
| *Figure 2: Database tables & Columns* |

| <img src="misc_files/pg_admin_sample_data.png" alt="drawing" width="1000"/> |
|:--:|
| *Figure 3: Stock price data in PostgreSQL* |

5. **Slack:**  
A ```helper_functions.py``` script sends job completion notifications to a slack channel of the following format. *More improvements to come in future.* ```Figure 4```shows sample slack notifications

| ![](misc_files/slack.png) |
|:--:|
| *Figure 4: Slack Notifications* |

## 5. Exploratory Data Analysis (EDA)

Moving averages are a commonly used techniques to smooth a noisy time-series data. With the investment use case, it can be used both as a signaling technique and for forecasting. In this section I will be focusing more on the how we can use moving averages to signal buy/sell decisions for a stock. The 3 techniques we will be discussing are:  
1. Simple Moving Average
2. Exponential Moving Average
3. Weighted Moving Average

Fig. 5 compares how each of the above techniques respond to price change in Uber stock price. Each of the moving averages is calculated using a 9 and 12 period timeframe, which means that each instance of the moving averages is computed as a function of the previous 9 or 12 stock prices. The reason why we use two different timeframes (9 and 12) to compute moving averages is because the cross-overs between the two is considered as a signal to buy/sell stocks.

Right of the bat we can see that the simple moving average is a more smooth curve as compared to the other two but is less responsive to price changes. This behavior stems from the fact that the simple moving average treats all previous stock prices equally where as the other two compensate by putting weights on them.

We use the following two rules to make these decisions:
- **Sell the stocks when the short-term ma (here after ma is used for moving average) or 9-period ma crosses over the long-term ma or 12-period ma in a downward direction.** The reason why we do this is because 9-period ma crossing over 12-period ma signifies that the drop in the prices in the most recent times (9 days) is significantly higher than that in the past 12 days.

- **Buy when the short-term ma or 9-period ma crosses over the long-term ma or 12-period ma in a upward direction.** The reason why we do this is because 9-period ma crossing over 12-period ma in upward direction, signifies that the lift in the prices in the most recent times (9 days) is significantly higher than that in the past 12 days.

The relative positions of the red dashed line in Fig. 5 shows how the weighted and exponential ma techniques are more quicker to identify signal as compared to the simple moving average.

| <img src="eda_plots/moving_avg.png" alt="drawing" width="1000"/> |
|:--:|
| *Figure 5: Moving Averages* |

## 6. Resources
- Web Scraping: [https://docs.scrapy.org/en/latest/intro/overview.html](https://docs.scrapy.org/en/latest/intro/overview.html)  
- Virtual Environment: [Corey Schafer: https://www.youtube.com/watch?v=Kg1Yvry_Ydk](https://www.youtube.com/watch?v=Kg1Yvry_Ydk)  
- Cronjob: [Corey Schafer: https://www.youtube.com/watch?v=QZJ1drMQz1A&t=418s](https://www.youtube.com/watch?v=QZJ1drMQz1A&t=418s) ,  
[Indian Pythonista: https://www.youtube.com/watch?v=Q2CNZGEH59Q&t=870s](https://www.youtube.com/watch?v=Q2CNZGEH59Q&t=870s)  
- Environment variables: [Corey Schafer: https://www.youtube.com/watch?v=5iWhQWVXosU&t=164s](https://www.youtube.com/watch?v=5iWhQWVXosU&t=164s)
- Slack bot: [Tech and Beyond with Moss: https://www.youtube.com/watch?v=lEQ68HhpO4g](https://www.youtube.com/watch?v=lEQ68HhpO4g) ,  
[Abhishek Thakur: https://www.youtube.com/watch?v=jDqjSd42024&t=379s](https://www.youtube.com/watch?v=jDqjSd42024&t=379s)
- Postgres: [Dataquest: https://www.dataquest.io/blog/loading-data-into-postgres/](https://www.dataquest.io/blog/loading-data-into-postgres/) ,  
[PostgreSQL Tutorial: https://www.postgresqltutorial.com/postgresql-python/connect/](https://www.postgresqltutorial.com/postgresql-python/connect/)
- Docker: [TechWorld with Nana: https://www.youtube.com/watch?v=3c-iBn73dDE&t=8377s](https://www.youtube.com/watch?v=3c-iBn73dDE&t=8377s)
