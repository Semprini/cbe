#!/usr/bin/env python 
import os, sys, time, json
import requests
import logging
import traceback

import pika

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

RETRY_DELAY = 30000 # Warning: do not change this if MQ has the queue instantiated already.

TEST_NAME = 'test.queue_trigger_pattern'    
TEST_EXCHANGES = (('notify.retail.sale.Sale.updated',None),('notify.retail.sale.Sale.created',{'store':'Test Store 1'}))


class RequeableError( Exception ):
    pass
    
    
class FatalError( Exception ):
    pass

    
class QueueTriggerPattern():
    """
    Boiler plate of queue triggered microservices. Should be inherited and 'worker' function overriden.
    
    Provided exchanges is a list of tuples. Each tuple contains an exchange name and exchange args dictionary (or None)
    Args example: {'ham': 'good', 'x-match':'any'}
    """
   
    def __init__(self, microservice_name, exchanges, queue_host, queue_user, queue_pass):
        self.microservice_name = microservice_name
        self.exchanges = exchanges
        self.retry_ready_exchnage = 'microservice.' + microservice_name + '.retry_ready'
        self.retry_exchange = 'microservice.' + microservice_name + '.retry'
        self.queue_name = 'microservice.' + microservice_name
        self.retry_queue_name = 'microservice.' + microservice_name + ".retry"
    
        self.queue_host = queue_host
        self.queue_user = queue_user
        self.queue_pass = queue_pass
    
    
    def worker(self, message_json):
        """
        Function as a placeholder to be overriden which is called for each message received on the subscribed queues
        """
        print( "Should override worker and do something here" )
    
    
    def request(self, url, user, password, error_message):
        """
        A wrapper around the requests get function which will call CBE and load the json response.
        """
        if type(url) is dict:
            logging.info( "QueueTriggerPattern request called to get url but url is already dict. Assuming loaded json so returning input." )
            return url
        response = requests.get(url, auth=(user, password))
        if response.status_code >= 500 or response.status_code in (401,403):
            # Retryable errors which can be requeued
            logging.warning( "Retryable " + error_message + "{}".format(response.content) )
            raise RequeableError("Get {} returned: {}".format(url, response.status_code))
        elif response.status_code != 200:
            # Fatal errors which can't be retried
            logging.error( "Fatal " + error_message + "{}".format(response.content) )
            raise FatalError("Get {} returned: {}".format(url, response.status_code))
        return json.loads(response.text)
    
    
    def queue_callback(self, channel, method, properties, body):
        """
        Handler for messages received off subscribed queues. Handles Acks, failures and requeues.
        Calls the worker function which a microservice should implement
        """
        # Always ack before work has completed as we have assumed responsibility for message. Retry handled via new message passed to retry exchange
        try:
            channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
            logging.info( "ackd" )
        except:
            logging.error( "Message unable to be ackd. Do not process now: %s"%body )
            raise

        # Load the message as json and call worker function
        try:
            # Create a disctionary from message body
            message_json=json.loads(body.decode('utf-8'))
            self.worker(message_json)
        except RequeableError as err:
            logging.info( "requeued: %s"%channel.basic_publish( self.retry_exchange, '', body ) )
        except FatalError as err:
            logging.error( "Fatal error: %s"%body )
        except Exception as err:
            logging.critical( "Unhandled message: %s | %s"%(err,body) )
            traceback.print_exc()
        

    def queue_setup(self, connection, callback):
        """
        Subscribes to configured queues and creates exchanges & queues for retry
        """
    
        channel = connection.channel()
        channel.confirm_delivery()

        # Create a queue for our messages to be read from
        result = channel.queue_declare(exclusive=False, queue=self.queue_name, durable=True )
        if not result:
            logging.critical( 'Queue didnt declare properly!' )
            sys.exit(1)

        # Subscribe (bind) to object message exchanges
        for exchange, arguments in self.exchanges:
            channel.exchange_declare(exchange=exchange, exchange_type='headers')
            channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key = '', arguments=arguments)

        # Create a dead letter exhange where messages from retry queue will be put after TTL
        # Subscribe (bind) our main queue to it for redelivery
        channel.exchange_declare(exchange=self.retry_ready_exchnage, exchange_type='direct')
        channel.queue_bind(exchange=self.retry_ready_exchnage, queue=self.queue_name, routing_key = '',)
        
        # Create a retry exchange and queue where messages are held for TTL.
        channel.exchange_declare(exchange=self.retry_exchange, exchange_type='direct')
        channel.queue_declare(exclusive=False, queue=self.retry_queue_name, durable=True, arguments={'x-dead-letter-exchange':self.retry_ready_exchnage,'x-message-ttl':RETRY_DELAY} )
        channel.queue_bind(exchange=self.retry_exchange, queue=self.retry_queue_name, routing_key = '',)
                           
        channel.basic_consume(callback, queue=self.queue_name, no_ack=False)
        return channel
        

    def connect(self, credentials):    
        """
        Continually attempts connection to MQ. If unable to connect then a sleep before retry.
        """

        ready = False
        while not ready:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.queue_host, credentials=credentials))
                logging.info( "Completed connection to MQ..." )
                ready = True
            except pika.exceptions.ConnectionClosed as ex:
                logging.warning( "Connection to MQ not ready, retry... ({})".format(ex) )
                time.sleep(5)
            except pika.exceptions.IncompatibleProtocolError as ex:
                logging.error( "Connection to MQ threw protocol error - possible server restarting, retry... ({})".format(ex) )
                time.sleep(60)
        return connection

        
    def main_loop(self):
        channel = None
        connection = None
        done = False

        try:
            credentials = pika.PlainCredentials(self.queue_user, self.queue_pass)
            connection = self.connect(credentials)
        
            while not done:
                try:
                   channel = self.queue_setup(connection, self.queue_callback)
                   channel.start_consuming()
                except pika.exceptions.ConnectionClosed:
                    logging.warning( "Connection to MQ closed. retry..." )
                    connection = None
                    time.sleep(5)
                    connection = self.connect(credentials)
                    
        except KeyboardInterrupt:
            print( 'Bye' )

        if channel:
            channel.stop_consuming()
        
        if connection:
            connection.close()

            
if __name__ == "__main__":
    
    qtp = QueueTriggerPattern(TEST_NAME, TEST_EXCHANGES, sys.argv[1], sys.argv[2], sys.argv[3])
    qtp.main_loop()
    
