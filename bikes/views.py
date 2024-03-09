import asyncio
import math
from django.shortcuts import render
import requests, time
import datetime
import pandas as pd
from greykite.framework.templates.autogen.forecast_config import ForecastConfig, MetadataParam, ModelComponentsParam
from greykite.framework.templates.forecaster import Forecaster
from asgiref.sync import sync_to_async
from .models import Bikes


def get_data():
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/records"
    params = {
        "where": "id_compteur='100057445-103057445'",
        "limit": 100,
        "order_by": "date DESC"
    }

    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = [{'date': item['date'], 'sum_counts': item['sum_counts']} for item in r.json()['results']]
    else:
        raise Exception(f"Failed to fetch data from the API. Status code: {r.status_code}")
    time.sleep(1)
    if data:
        return data
    else:
        return "Waiting..."


def runMLModel(data):
    forecast_config = ForecastConfig(
        model_template = "SILVERKITE",
        forecast_horizon = 25,
        coverage = 0.85,
        metadata_param = MetadataParam(
            time_col = "DateTime",
            value_col = "sum_counts",
            freq = "H",
            train_end_date=datetime.datetime.today() + datetime.timedelta(days=3)
        )
    )
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df["date"], utc=True, errors='coerce')
    df['date'] = df['date'].values
    df.sort_values(by='date', inplace=True)
    df["DateTime"] = df["date"]
    df.set_index('date', inplace=True)

    forecaster = Forecaster()
    silverkite = forecaster.run_forecast_config(
        df = df,
        config = forecast_config
    )

    forecast_data_json  = silverkite.forecast.df.to_dict()

    last_24_entries = {}
    for forecast_key in forecast_data_json:
        if forecast_key == "DateTime":
            for y in forecast_data_json[forecast_key]:
                forecast_data_json[forecast_key][y] = forecast_data_json[forecast_key][y].strftime("%Y-%m-%d %X")
            forecast_value = dict(list(forecast_data_json[forecast_key].items())[-100:])
        else :
            forecast_value = dict(list(forecast_data_json[forecast_key].items())[-100:])
        for index_key in forecast_value:
            if index_key in last_24_entries:
                last_24_entries[index_key][forecast_key] = forecast_value[index_key]
            else:
                last_24_entries[index_key] = {forecast_key: forecast_value[index_key]}

    result = list(last_24_entries.values())
    return result

@sync_to_async
def saveResultsToDB(result):
    for data in result:
        actual_data = None
        if not (math.isnan(data['actual'])):
            actual_data = data["actual"]
        result_to_save = Bikes(
            actual=actual_data,
            forecast=data["forecast"],
            upper=data["forecast_upper"],
            lower=data["forecast_lower"],
            date_time=data["DateTime"]
        )
        result_to_save.save()


@sync_to_async
def check_is_entry_today(today):
    todays_data = Bikes.objects.filter(date_time=today)
    return todays_data.exists() and todays_data[0].actual != None

@sync_to_async
def get_treated_data():
    bikes_queryset = Bikes.objects.all()
    data = []
    for bikes_data in bikes_queryset:
        actual_data = None
        if bikes_data.actual != None:
            actual_data = float(bikes_data.actual)
        data.append({
            "actual":actual_data,
            "forecast":float(bikes_data.forecast),
            "forecast_upper":float(bikes_data.upper),
            "forecast_lower":float(bikes_data.lower),
            "DateTime":bikes_data.date_time
        })


    return data

async def bikes(request):
    context = {}
    data = get_data()
    today = datetime.datetime.fromisoformat(data[0]['date']).strftime("%Y-%m-%d %H:%M:%S")
    is_entry_today = await check_is_entry_today(today)
    if not is_entry_today:
        if data != "Waiting...":
            context["forecast"] = runMLModel(data)[-72:]
            await saveResultsToDB(context["forecast"])
    else:
        treated_data = await get_treated_data()
        context["forecast"] = treated_data[-72:]
    return render(request, 'bikes/bikes.html', context)
