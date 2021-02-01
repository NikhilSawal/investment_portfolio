# Investment Portfolio

### 1. Overview

This is an end-to-end project that covers several aspects of a machine learning project life-cycle. This project is my attempt to learn various technologies required for Data Science/Machine Learning and grow as a full stack Machine Learning Engineer. Through this project I have tried to cover 4 aspects of DS/ML project:

1. Data collection/extraction (web scraping)
2. Data storage
3. Continuous integration
4. Visualization, model building & evaluation

### 2. Problem Statement

Forecasting strategies have become more important given the uncertain times we live in.
- Can a rich storage of data help us predict important aspects of the stock market?
- Can we use news data to model the impact of certain keywords that come up in news headlines on stock prices across different industries?

### 3. Motivation

The idea for this project, struck me when we were hit by the pandemic in early 2020. I used to work for a gift cards selling company i.e [Raise Marketplace.](https://www.raise.com/) that acquired gift cards from over 3000 brands and sold them on its platform. The business was impacted because of the pandemic since a huge chunk of the companies revenue came from the travels & hotels industry.

- What if we had access to external data like news headlines? Could we have modeled the impact of the pandemic on several industries through their stock prices and made informed decisions about our acquisition strategies?

- Can we start storing information like news data and model the impact of a few key words to different industries, so that if a similar situation were to happen in the future, we can have a backup?

### 4. Current Stage of Project

I currently have 3 scripts that scrape three different sets of data from **yahoo finance**. I have **cronjobs** set to schedule the scrape. The data is then stored to 3 **.jl** files which is then piped to a Postgres Database. I also have a slackbot that sends notification to my slack channel for error handling.

> Current technologies: Python, Scrapy, Slack (for notifications), Cronjob

> Future technologies: Docker, Jenkins, Plotly, (Tensorflow/Keras/PyTorch)
