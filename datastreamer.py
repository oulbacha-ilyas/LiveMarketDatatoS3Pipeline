
# Flask and web-related imports
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify

# Data manipulation and analysis
import pandas as pd
import numpy as np
from io import BytesIO, StringIO
import scipy.stats as stats

# Data visualization
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from IPython.display import display

# Time-related imports
from datetime import datetime, timedelta
import pytz
import time
from time import sleep

# Financial data and trading
import yfinance as yf
from yflive import QuoteStreamer
import ta
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.accounts import AccountDetails



# Database
import sqlite3

# Multithreading
import threading
import queue
import logging
from multiprocessing import Process, Event

# Utilities
import hashlib
import os
import json

# Cloud services
import boto3

# Application-specific
from flask import current_app

class ConsolidationAgent:
    def __init__(self,market):

        ##bucket setup:
        self.AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
        self.AWS_SECRET_ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
        self.BUCKET_NAME = 'BUCKET_NAME'
        self.s3_client = boto3.resource(
                            's3',
                            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY
                        )
        ##market and quotes
        self.market=market
        self.quotes_list={"crypto":["BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "LTC-USD"],
                           "forex":["EURUSD=X", "GBPUSD=X", "NZDUSD=X", "AUDUSD=X", "DX-Y.NYB"]}
        self.market_quotes = self.quotes_list[self.market]
        self.data = []

        ##df setup
        columns=['DATETIME','change','changePercent','circulatingSupply',
                 'currency','dayHigh','dayLow','dayVolume','exchange','fromCurrency'
                 ,'identifier','lastSize','marketCap','marketState','openPrice',
                 'price','priceHint','quoteType','time','volAllCurrencies','vol_24hr']
        self.df_1mls=pd.DataFrame(columns=columns)
        self.all_pair_df_max=pd.DataFrame(columns=columns)

    def return_df(self,timeframe):
        if timeframe=='1mls':
            return self.df_1mls
    def dfs_current_state(self):
        market=self.market
        df_1mls_len=len(self.df_1mls)
        message=f'Market:{market} ,1mls df:{df_1mls_len}'

        return message



    def reset_df(self,timeframe):
             self.save_to_bucket(timeframe)

             if timeframe=='1mls':
                    self.df_1mls=self.df_1mls.tail(0)

             message=f"{timeframe} df has been reset successfully to 0 rows"
             return message


    def lambda_handler(self,quote):
            desired_timezone = 'Europe/Paris'
            current_time = datetime.now() #(pytz.timezone(desired_timezone))
            change = str(quote.change)
            changePercent = str(quote.changePercent)
            circulatingSupply = str(quote.circulatingSupply)
            currency = str(quote.currency)
            dayHigh = str(quote.dayHigh )
            dayLow = str(quote.dayLow )
            dayVolume = str(quote.dayVolume)
            exchange = str(quote.exchange )
            fromCurrency = str(quote.fromCurrency )
            identifier = str(quote.identifier )
            lastSize = str(quote.lastSize )
            marketCap = str(quote.marketCap )
            marketState = str(quote.marketState )
            openPrice = str(quote.openPrice )
            price = str(quote.price )
            priceHint = str(quote.priceHint )
            quoteType = str(quote.quoteType )
            time = str(quote.time )
            volAllCurrencies = str(quote.volAllCurrencies )
            vol_24hr = str(quote.vol_24hr )

            item = {
            'DATETIME' : str(current_time),
            'change' : str(quote.change ),
            'changePercent' : str(quote.changePercent ),
            'circulatingSupply' : str(quote.circulatingSupply ),
            'currency' : str(quote.currency ),
            'dayHigh' : str(quote.dayHigh ),
            'dayLow' : str(quote.dayLow ),
            'dayVolume' : str(quote.dayVolume ),
            'exchange' : str(quote.exchange ),
            'fromCurrency' : str(quote.fromCurrency ),
            'identifier' : str(quote.identifier ),
            'lastSize' : str(quote.lastSize ),
            'marketCap' : str(quote.marketCap ),
            'marketState' : str(quote.marketState ),
            'openPrice' : str(quote.openPrice ),
            'price' : str(quote.price ),
            'priceHint' : str(quote.priceHint ),
            'quoteType' : str(quote.quoteType ),
            'time' : str(quote.time ),
            'volAllCurrencies' : str(quote.volAllCurrencies ),
            'vol_24hr' : str(quote.vol_24hr)
            }

            new_quote=pd.DataFrame(item,index=[0])
            self.df_1mls=pd.concat([self.df_1mls,new_quote],ignore_index=True)
            self.df_1mls=self.df_1mls.drop_duplicates()

            periodic_tasks_logger.info("Quote added to df")


    def save_to_bucket(self,timeframe):

                ##timesetup:
                now = datetime.now()
                desired_timezone = 'Europe/Paris'
                current_time = datetime.now(pytz.timezone(desired_timezone))
                today_date = now.strftime("%Y-%m-%d")
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")
                ##df setup
                filename=f'{self.market}_{timeframe}_{today_date}_{current_hour}_{current_minute}.csv'
                df=getattr(self,f'df_{timeframe}')
                save_treshold=getattr(self,f'save_treshold_{timeframe}')
                #df=df.tail(save_treshold)

                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)

                ##bucket setup

                response=self.s3_client.Object(self.BUCKET_NAME, filename).put(Body=csv_buffer.getvalue())
                saving_status=response['ResponseMetadata']['HTTPStatusCode']
                message=''
                if saving_status==200:
                   message=f"{self.market} {timeframe} data saved successfully at : {current_time}"
                else:
                   message="File not saved"
                periodic_tasks_logger.info(f"{timeframe} data saved to bucket;{saving_status}")
                return message
    def reinitialize(self,market):
        # Reinitialize all attributes to their initial state
        self.__init__(market)  # This is one way, but not always recommended

        return f"Reinitialized consolidation to {market} market"



consolidation=ConsolidationAgent('forex')







####strategy####################################################################




class StreamingAgent:
    def __init__(self):
        self.quote_streamer = None
        self.quote_queue = queue.Queue()
        self.quote_ready=False
        #self.last_execution_time = time.time()
        self.last_execution_time = datetime.now()
        self.threads = {}
        self.lock = threading.Lock()
        self.monitor_thread = None
        self.is_running = threading.Event()
        self.periodic_tasks_is_running = threading.Event()
        self.is_running.set()
        self.periodic_tasks_is_running.set()
    def start_thread(self, name, target, args=(), daemon=True):

        with self.lock:
            if name in self.threads and self.threads[name].is_alive():
                threads_monitoring_logger.info(f"Thread {name} is already running")

            else :
                thread = threading.Thread(target=target, args=args, daemon=daemon)
                self.threads[name] = thread
                thread.start()
                threads_monitoring_logger.info(f"Thread {name} started")
        threads_monitoring_logger.info("Lock released")


    def stop_thread(self, name):
        with self.lock:
            if name in self.threads:
                self.is_running.clear()  # Use this event to signal threads to stop
                self.periodic_tasks_is_running.clear()
                #self.threads[name].join()
                threads_monitoring_logger.info(f"Thread {name} stopped")
                del self.threads[name]
    def stop_all_threads(self):
        self.is_running.clear()
        self.periodic_tasks_is_running.clear()
        with self.lock:
            for name, thread in list(self.threads.items()):
                thread.join()
                threads_monitoring_logger.info(f"Thread {name} stopped")
            self.threads.clear()

        return "Data pulling and consolidation stopped"


    def start_streaming(self):
        market_quotes = getattr(consolidation, 'market_quotes')
        threads_monitoring_logger.info(f'Quotes beeing streamed :{market_quotes}')

        if self.is_running.is_set():
                if self.quote_streamer is None:
                    try:
                        self.quote_streamer = QuoteStreamer(
                            subscribe=market_quotes,
                            on_connect=self.your_on_connect_callback,
                            on_quote=self.your_on_quote_callback,
                            on_error=self.your_on_error_callback,
                            on_close=self.your_on_close_callback
                        )
                        self.quote_streamer.start()
                    except Exception as e:
                        threads_monitoring_logger.info(f"Error creating or starting QuoteStreamer: {e}")
                else :
                  threads_monitoring_logger.info("Pull data event set and quotestreamer exist")
                  self.quote_streamer.start()

        else:
             print('Pull data event is not set')

    def your_on_connect_callback(self, quote_streamer):
        #print("Connected to Yahoo! Finance websocket")
        threads_monitoring_logger.info("Connected to Yahoo! Finance websocket")

    def your_on_quote_callback(self, quote_streamer, quote):
        if self.is_running.is_set():
            with self.lock:
                # Put the quote into the queue for processing

                self.quote_queue.put(quote)
                self.quote_ready=True
                #consolidation.lambda_handler(quote)
                #print("Quote added to queue")
                pulling_data_logger.info("Quote added to queue")

    def process_queue(self):
            try:
                # Get the next quote from the queue, blocks if empty

                with self.lock:
                    quote = self.quote_queue.get()
                    consolidation.lambda_handler(quote)
                    df1s_name = '1mls'
                    df_1mls = consolidation.return_df(df1s_name)

                    pulling_data_logger.info(f'df1s length: {len(df_1mls)}' )
                    current_time = datetime.now()
                    pulling_data_logger.info('Adding quotes finished at')


            except Exception as e:
                #print(f"Error in processing queue: {e}")
                periodic_tasks_logger.info(f"Error in processing queue: {e}")
            finally:
                # Indicate that a formerly enqueued task is complete
                self.quote_queue.task_done()

    def your_on_error_callback(self, quote_streamer, error):
        threads_monitoring_logger.info(f"Error encountered: {error}")

        self.is_running.set()
        self.periodic_tasks_is_running.set()
        self.start_streaming()
    def your_on_close_callback(self, quote_streamer):
        threads_monitoring_logger.info("Connection to Yahoo! Finance websocket closed")
        self.is_running.set()
        self.periodic_tasks_is_running.set()
        self.start_streaming()


    def periodic_tasks(self):
        while True:
                if not self.periodic_tasks_is_running.is_set():
                    threads_monitoring_logger.info("Periodic tasks stopping as the event is cleared.")
                    break
                current_time = datetime.now()
                current_execution_time = time.time()
                if not self.periodic_tasks_is_running.is_set():

                    threads_monitoring_logger.info("Periodic tasks stopped")

                    break

                if self.quote_ready ==True:
                                self.process_queue()
                                self.quote_ready=False
                if current_time.minute != self.last_execution_time.minute:
                        with self.lock:
                            periodic_tasks_logger.info("Consolidation started")
                            consolidation.consolidate_1mls_to_tf('1min')
                            self.last_execution_time = datetime.now()
                            c_time_lapse_sec=self.last_execution_time.second-current_time.second
                            c_time_lapse_min=self.last_execution_time.minute-current_time.minute
                            periodic_tasks_logger.info("Consolidation finished")
                            periodic_tasks_logger.info(f"Consolidation spent time : {c_time_lapse_min} minutes and {c_time_lapse_sec} seconds")
                            current_time_signal=datetime.now()

                            last_signals_calculaion_time= datetime.now()
                            c_time_lapse_sec=last_signals_calculaion_time.second-current_time_signal.second
                            c_time_lapse_min=last_signals_calculaion_time.minute-current_time_signal.minute
                            periodic_tasks_logger.info(f"Calculating signal spent time : {c_time_lapse_min} minutes and {c_time_lapse_sec} seconds")

                if current_time.minute % 30 == 0:
                    with self.lock:
                        df_1min=consolidation.return_df('1min')
                        df_1mls=consolidation.return_df('1mls')
                        if  df_1mls is not None  and not df_1mls.empty:
                            if len(df_1mls)>=2000:

                                consolidation.reset_df('1mls')
                                periodic_tasks_logger.info("1mls data reset")
                        if  df_1min is not None  and not df_1min.empty:
                            if len(df_1min)>=10000:
                                consolidation.reset_df('1min')
                                periodic_tasks_logger.info("1min data reset")


        periodic_tasks_logger.info("Cannot execute periodic tasks because pull data event is not set")
    def reinitialize(self):
        # Reinitialize all attributes to their initial state
        self.__init__()  # This is one way, but not always recommended
        print("Reinitialized StreamingAgent")



streaming_agent = StreamingAgent()


class MonitoringAgent():
    def __init__(self):
        self.monitoring_is_running = threading.Event()
        self.lock = threading.Lock()  # Initialize lock

    def monitor_threads(self):

        while self.monitoring_is_running.is_set():
            threads = getattr(streaming_agent, 'threads')
            with self.lock:
                for name, thread in list(threads.items()):
                    if not thread.is_alive():
                        monitoring_logger.info(f"Thread {name} is not alive, restarting...")

                        # Restart the thread based on its name
                        if name == "pulling_data":
                            streaming_agent.start_thread(name, streaming_agent.start_streaming)
                        elif name == "periodic_tasks":
                            streaming_agent.start_thread(name, streaming_agent.periodic_tasks)

                        monitoring_logger.info(f"restarted {name} thread")

            threads_monitoring_logger.info("Monitoring is running")
            time.sleep(30)  # Monitor every 30 seconds

    def start_monitoring(self):
        self.monitoring_is_running.set()
        self.monitor_thread = threading.Thread(target=self.monitor_threads, daemon=True)
        self.monitor_thread.start()
        monitoring_logger.info("Monitoring thread started")

    def stop_monitoring(self):
        self.monitoring_is_running.clear()
        monitoring_logger.info("Monitoring thread stopped")

# Initialize MonitoringAgent
monitoring = MonitoringAgent()
###flask app####################################################################
app = Flask(__name__, static_folder='static_streamer')
# Configure logging for the Flask app
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [Flask] %(levelname)s: %(message)s')
flask_logger = logging.getLogger(__name__)

# Configure logging for the pulling_data thread
pulling_data_logger = logging.getLogger('pulling_data')
pulling_data_logger.setLevel(logging.DEBUG)
pulling_data_logger.propagate = False
pulling_data_formatter = logging.Formatter('%(asctime)s [pulling_data] %(levelname)s: %(message)s')
pulling_data_handler = logging.StreamHandler()
pulling_data_handler.setFormatter(pulling_data_formatter)
pulling_data_logger.addHandler(pulling_data_handler)

# Configure logging for the periodic_tasks thread
periodic_tasks_logger = logging.getLogger('periodic_tasks')
periodic_tasks_logger.setLevel(logging.DEBUG)
periodic_tasks_logger.propagate = False
periodic_tasks_formatter = logging.Formatter('%(asctime)s [periodic_tasks] %(levelname)s: %(message)s')
periodic_tasks_handler = logging.StreamHandler()
periodic_tasks_handler.setFormatter(periodic_tasks_formatter)
periodic_tasks_logger.addHandler(periodic_tasks_handler)

# Configure logging for threads monitoring
threads_monitoring_logger = logging.getLogger('periodic_tasks')
threads_monitoring_logger.setLevel(logging.DEBUG)
threads_monitoring_logger.propagate = False
threads_monitoring_formatter = logging.Formatter('%(asctime)s [threads_monitoring] %(levelname)s: %(message)s')
threads_monitoring_handler = logging.StreamHandler()
threads_monitoring_handler.setFormatter(threads_monitoring_formatter)
threads_monitoring_logger.addHandler(threads_monitoring_handler)

# Configure logging for threads monitoring
monitoring_logger = logging.getLogger('monitor_thread')
monitoring_logger.setLevel(logging.DEBUG)
monitoring_logger.propagate = False
monitoring_formatter = logging.Formatter('%(asctime)s [monitoring] %(levelname)s: %(message)s')
monitoring_handler = logging.StreamHandler()
monitoring_handler.setFormatter(monitoring_formatter)
monitoring_logger.addHandler(monitoring_handler)


@app.route('/start_streaming', methods=['POST'])
def start_streaming():
    # Create an instance of StreamingAgent
    flask_logger.info("Received request to start streaming")
    streaming_agent.reinitialize()
    #streaming_agent.start_streaming_threading()
    streaming_agent.start_thread("pulling_data",streaming_agent.start_streaming)
    threads_monitoring_logger.info("Pulling data thread started")
    streaming_agent.start_thread("periodic_tasks",streaming_agent.periodic_tasks)
    threads_monitoring_logger.info("Periodic tasks thread started")
    monitoring.start_monitoring()
    return jsonify({'message':'Streaming launched' })

@app.route('/stop_streaming', methods=['POST'])
def stop_streaming():
    # Your logic here
    flask_logger.info("Received request to stop streaming")
    monitoring.stop_monitoring()
    return jsonify({'message': streaming_agent.stop_all_threads()})

@app.route('/save_to_bucket', methods=['POST'])
def save_to_bucket():
    flask_logger.info("Received request to save to bucket")
    timeframe = request.json.get('timeframe')
    return jsonify({'message': consolidation.save_to_bucket(timeframe)})

@app.route('/reset_df', methods=['POST'])
def reset_df():
    # Your logic here
    flask_logger.info("Received request to reset df")
    timeframe = request.json.get('timeframe')
    return jsonify({'message': consolidation.reset_df(timeframe)})



@app.route('/dfs_current_state', methods=['POST'])
def dfs_current_state():
    # Your logic here
    flask_logger.info("Received request to current state")
    return jsonify({'message': consolidation.dfs_current_state()})

@app.route('/')
def index():
    return send_from_directory('static_streamer', 'index.html')





if __name__ == "__main__":
    # Start the monitoring process
    monitor_process = Process(target=monitoring.start_monitoring)
    monitor_process.start()

    # Start the Flask app in a separate process if needed
    app_process = Process(target=app.run, kwargs={"debug": True})
    app_process.start()

    # Optionally, you can join the processes if you want the main script to wait for them
    monitor_process.join()
    app_process.join()
