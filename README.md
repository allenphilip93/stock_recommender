# stock_recommender
Recommend equity stocks from NSE

# Installation

```bash
docker compose up --build
```

# Services

## TimescaleDB

**URL** `http://localhost:5432`
**Database** `stocks`
**Username** `admin`
**Password** `password`

## Airflow

**URL** `http://localhost:8080`
**Username** `admin`
**Password** `password`

## DB Admin

**URL** `http://localhost:9001`
**Username** `your@email.com`
**Password** `password`

## Grafana

**URL** `http://localhost:9000`
**Username** `admin`
**Password** `password`

# Initialization

Once the services are up and running. Open DB Admin, configure the TimescaleDB datasource as shown below:
![image](https://user-images.githubusercontent.com/20537002/222343322-a2e170be-b307-4c0a-86ba-62629d986874.png)

After the datasource connection is established, open the query tool:
![image](https://user-images.githubusercontent.com/20537002/222343723-88c26d31-cd4c-40c5-8672-4b83be8a44a6.png)

Copy paste the query from `init.sql` into the editor and run the query:
![image](https://user-images.githubusercontent.com/20537002/222343860-4aedd1cc-c6ac-4aa5-8604-0d0ae0077f78.png)

Next setup the datasource (PostgreSQL) on Grafana:
![image](https://user-images.githubusercontent.com/20537002/222344022-ef63870f-6467-4f73-a8c1-18a5093c14e3.png)

Load the data into your database by opening the Airflow UI and enable/trigger the `data_collector_dag` DAG
![image](https://user-images.githubusercontent.com/20537002/222344239-c8be3b99-fd80-4535-b9a4-e7589b2579df.png)

Lastly import the grafana dashboard by copying the contents from `stocks_dashboard.json` and paste into "Import via panel json" field:
![image](https://user-images.githubusercontent.com/20537002/222344450-bbb9e8b7-4d92-44a5-b040-206d10737a8e.png)

