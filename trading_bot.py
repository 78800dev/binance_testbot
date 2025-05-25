# # This file will contain the main logic of bot.
# import logging
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
# from binance.exceptions import BinanceAPIException, BinanceRequestException
# from binance.enums import FuturesType # Import FuturesType
# import sys
# import os
# import time

# # Load API keys from config.py
# try:
#     from config import API_KEY, API_SECRET
# except ImportError:
#     print("Error: config.py not found or API_KEY/API_SECRET not defined.")
#     print("Please create a config.py file with your API_KEY and API_SECRET.")
#     sys.exit(1)

# # --- Configuration ---
# TESTNET_BASE_URL = "https://testnet.binancefuture.com"
# # FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi/v1" # This is the correct base URL for futures API calls
# LOG_FILE = "trading_bot.log"

# # --- Logging Setup ---
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler(sys.stdout) # Also print to console
#     ]
# )
# logger = logging.getLogger(__name__)

# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
# from binance.exceptions import BinanceAPIException, BinanceRequestException
# import sys
# import os
# import time

# # ... (rest of your existing imports and code)

# class BasicBot:
#     def __init__(self, api_key, api_secret, testnet=True):
#         """
#         Initializes the trading bot with Binance API client for Futures.
#         """
#         self.api_key = api_key
#         self.api_secret = api_secret
#         self.testnet = testnet

#         # This is the modern way to instantiate a Futures client in recent python-binance
#         if self.testnet:
#             logger.info("Connecting to Binance Futures Testnet.")
#             self.client = Client(api_key, api_secret, tld='com', testnet=True)
#             # Note: tld='com' is often needed if you're not explicitly using .us or other domains
#             # For testnet, 'com' is usually correct.
#         else:
#             logger.info("Connecting to Binance Futures Mainnet.")
#             self.client = Client(api_key, api_secret, tld='com')
#             # If you need mainnet *futures* specifically, and not just spot, it might be:
#             # self.client = Client(api_key, api_secret, tld='com').futures()
#             # However, for a general bot, the default Client often works for both after init.
#             # Let's stick with the most direct for the testnet problem.


#         self._check_connection()
# # class BasicBot:
# #     def __init__(self, api_key, api_secret, testnet=True):
# #         """
# #         Initializes the trading bot with Binance API client.
# #         """
# #         self.api_key = api_key
# #         self.api_secret = api_secret
# #         self.testnet = testnet

# #         # Try the original base_url parameter with the constant string
# #         if self.testnet:
# #             logger.info(f"Connecting to Binance Futures Testnet at {FUTURES_TESTNET_URL}")
# #             self.client = Client(api_key, api_secret, base_url=FUTURES_TESTNET_URL)
# #         else:
# #             logger.info("Connecting to Binance Futures Mainnet (default URL).")
# #             self.client = Client(api_key, api_secret) # Default mainnet URL for spot/futures
# #                                                      # For mainnet futures, it might need base_url=Client.FUTURES_URL
# #                                                      # but let's focus on testnet for now.

# #         self._check_connection()

#         # # Initialize the client specifically for Futures trading
#         # if self.testnet:
#         #     logger.info("Connecting to Binance Futures Testnet.")
#         #     self.client = Client(api_key, api_secret, base_url=Client.FUTURES_TESTNET_URL)
#         # else:
#         #     logger.info("Connecting to Binance Futures Mainnet.")
#         #     self.client = Client(api_key, api_secret, base_url=Client.FUTURES_URL)

#         # self._check_connection()
# # class BasicBot:
# #     def __init__(self, api_key, api_secret, testnet=True):
# #         """
# #         Initializes the trading bot with Binance API client.
# #         """
# #         self.api_key = api_key
# #         self.api_secret = api_secret
# #         self.testnet = testnet
#         # if self.testnet:
#         #     logger.info(f"Connecting to Binance Futures Testnet at {FUTURES_TESTNET_URL}")
#         #     self.client = Client(api_key, api_secret, base_url=FUTURES_TESTNET_URL)
#         # else:
#         #     logger.info("Connecting to Binance Futures Mainnet.")
#         #     self.client = Client(api_key, api_secret) # Default mainnet URL
      

#     def _check_connection(self):
#         """
#         Tests connectivity to the Binance API.
#         """
#         try:
#             server_time = self.client.futures_ping()
#             logger.info(f"Successfully connected to Binance Futures Testnet. Server time ping successful.")
#         except BinanceRequestException as e:
#             logger.error(f"Connection failed: {e}. Please check your internet connection or API keys.")
#             sys.exit(1)
#         except Exception as e:
#             logger.error(f"An unexpected error occurred during connection check: {e}")
#             sys.exit(1)

#     def _log_api_call(self, method, endpoint, params=None, response=None, error=None):
#         """
#         Logs API requests, responses, and errors.
#         """
#         log_message = f"API Call: {method} {endpoint}"
#         if params:
#             log_message += f", Params: {params}"
#         if response:
#             log_message += f", Response: {response}"
#             logger.info(log_message)
#         elif error:
#             log_message += f", Error: {error}"
#             logger.error(log_message)
#         else:
#             logger.debug(log_message) # For calls where we only log request

#     def get_account_balance(self):
#         """
#         Fetches and returns the USDT-M Futures account balance.
#         """
#         try:
#             account_info = self.client.futures_account_balance()
#             for balance in account_info:
#                 if balance['asset'] == 'USDT':
#                     logger.info(f"Current USDT Balance: {balance['balance']}")
#                     return float(balance['balance'])
#             logger.warning("USDT balance not found in account information.")
#             return None
#         except BinanceAPIException as e:
#             self._log_api_call("GET", "/fapi/v2/account", error=f"Binance API Error: {e.code} - {e.message}")
#             return None
#         except BinanceRequestException as e:
#             self._log_api_call("GET", "/fapi/v2/account", error=f"Request Error: {e}")
#             return None
#         except Exception as e:
#             self._log_api_call("GET", "/fapi/v2/account", error=f"An unexpected error: {e}")
#             return None

#     def get_symbol_info(self, symbol):
#         """
#         Fetches and returns detailed information about a trading pair,
#         including price and quantity filters.
#         """
#         try:
#             exchange_info = self.client.futures_exchange_info()
#             for s in exchange_info['symbols']:
#                 if s['symbol'] == symbol.upper():
#                     info = {
#                         'symbol': s['symbol'],
#                         'status': s['status'],
#                         'price_precision': s['pricePrecision'],
#                         'quantity_precision': s['quantityPrecision'],
#                         'min_notional': None,
#                         'min_quantity': None,
#                         'tick_size': None,
#                         'step_size': None,
#                         'filters': s['filters']
#                     }
#                     for f in s['filters']:
#                         if f['filterType'] == 'PRICE_FILTER':
#                             info['tick_size'] = float(f['tickSize'])
#                         elif f['filterType'] == 'LOT_SIZE':
#                             info['min_quantity'] = float(f['minQty'])
#                             info['step_size'] = float(f['stepSize'])
#                         elif f['filterType'] == 'MIN_NOTIONAL':
#                             info['min_notional'] = float(f['minNotional'])
#                     logger.debug(f"Symbol info for {symbol}: {info}")
#                     return info
#             logger.warning(f"Symbol {symbol} not found in exchange info.")
#             return None
#         except BinanceAPIException as e:
#             self._log_api_call("GET", "/fapi/v1/exchangeInfo", error=f"Binance API Error: {e.code} - {e.message}")
#             return None
#         except BinanceRequestException as e:
#             self._log_api_call("GET", "/fapi/v1/exchangeInfo", error=f"Request Error: {e}")
#             return None
#         except Exception as e:
#             self._log_api_call("GET", "/fapi/v1/exchangeInfo", error=f"An unexpected error: {e}")
#             return None

#     def _round_quantity(self, quantity, symbol_info):
#         """
#         Rounds quantity to the appropriate precision based on symbol info.
#         """
#         if not symbol_info or 'step_size' not in symbol_info or not symbol_info['step_size']:
#             logger.error("Could not determine step_size for quantity rounding.")
#             return quantity
#         step_size = symbol_info['step_size']
#         rounded_qty = round(quantity / step_size) * step_size
#         # Adjust precision for floating point inaccuracies
#         precision = len(str(step_size).split('.')[-1]) if '.' in str(step_size) else 0
#         return float(f"{rounded_qty:.{precision}f}")


#     def _round_price(self, price, symbol_info):
#         """
#         Rounds price to the appropriate precision based on symbol info.
#         """
#         if not symbol_info or 'tick_size' not in symbol_info or not symbol_info['tick_size']:
#             logger.error("Could not determine tick_size for price rounding.")
#             return price
#         tick_size = symbol_info['tick_size']
#         rounded_price = round(price / tick_size) * tick_size
#         # Adjust precision for floating point inaccuracies
#         precision = len(str(tick_size).split('.')[-1]) if '.' in str(tick_size) else 0
#         return float(f"{rounded_price:.{precision}f}")


#     def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
#         """
#         Places an order on Binance Futures Testnet.
#         :param symbol: Trading pair (e.g., 'BTCUSDT')
#         :param side: 'BUY' or 'SELL'
#         :param order_type: 'MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT'
#         :param quantity: Quantity to trade
#         :param price: Price for LIMIT or STOP_LIMIT orders
#         :param stop_price: Stop price for STOP_MARKET or STOP_LIMIT orders
#         :return: Order details or None on failure
#         """
#         params = {
#             'symbol': symbol.upper(),
#             'side': side.upper(),
#             'type': order_type.upper(),
#             'quantity': quantity
#         }

#         symbol_info = self.get_symbol_info(symbol)
#         if not symbol_info:
#             logger.error(f"Cannot place order for {symbol}: Could not retrieve symbol information.")
#             return None

#         # Validate and round quantity
#         if quantity < symbol_info.get('min_quantity', 0):
#             logger.error(f"Order quantity {quantity} is less than minimum allowed quantity {symbol_info['min_quantity']} for {symbol}.")
#             return None
#         params['quantity'] = self._round_quantity(quantity, symbol_info)
#         logger.info(f"Rounded quantity to {params['quantity']}")


#         if order_type.upper() == 'LIMIT' or order_type.upper() == 'STOP_LIMIT':
#             if price is None:
#                 logger.error(f"Price is required for {order_type} orders.")
#                 return None
#             params['price'] = f"{self._round_price(price, symbol_info):.{symbol_info['price_precision']}f}"
#             logger.info(f"Rounded price to {params['price']}")
#             params['timeInForce'] = 'GTC'  # Good Till Canceled for limit orders

#         if order_type.upper() in ['STOP_MARKET', 'STOP_LIMIT']:
#             if stop_price is None:
#                 logger.error(f"Stop price is required for {order_type} orders.")
#                 return None
#             params['stopPrice'] = f"{self._round_price(stop_price, symbol_info):.{symbol_info['price_precision']}f}"
#             logger.info(f"Rounded stop price to {params['stopPrice']}")

#         try:
#             logger.info(f"Attempting to place {order_type} order: {params}")
#             self._log_api_call("POST", "/fapi/v1/order", params=params)

#             if order_type.upper() == 'MARKET':
#                 order = self.client.futures_create_order(
#                     symbol=params['symbol'],
#                     side=params['side'],
#                     type='MARKET',
#                     quantity=params['quantity']
#                 )
#             elif order_type.upper() == 'LIMIT':
#                 order = self.client.futures_create_order(
#                     symbol=params['symbol'],
#                     side=params['side'],
#                     type='LIMIT',
#                     timeInForce=params['timeInForce'],
#                     quantity=params['quantity'],
#                     price=params['price']
#                 )
#             elif order_type.upper() == 'STOP_LIMIT':
#                 order = self.client.futures_create_order(
#                     symbol=params['symbol'],
#                     side=params['side'],
#                     type='STOP_LIMIT',
#                     quantity=params['quantity'],
#                     price=params['price'],
#                     stopPrice=params['stopPrice'],
#                     timeInForce=params['timeInForce']
#                 )
#             # Add other order types here if needed (e.g., TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET)
#             else:
#                 logger.error(f"Unsupported order type: {order_type}")
#                 return None

#             self._log_api_call("POST", "/fapi/v1/order", params=params, response=order)
#             logger.info("Order placed successfully:")
#             self._display_order_details(order)
#             return order
#         except BinanceAPIException as e:
#             self._log_api_call("POST", "/fapi/v1/order", params=params, error=f"Binance API Error: {e.code} - {e.message}")
#             logger.error(f"Failed to place order: Binance API Error {e.code} - {e.message}")
#             return None
#         except BinanceRequestException as e:
#             self._log_api_call("POST", "/fapi/v1/order", params=params, error=f"Request Error: {e}")
#             logger.error(f"Failed to place order: Request Error {e}")
#             return None
#         except Exception as e:
#             self._log_api_call("POST", "/fapi/v1/order", params=params, error=f"An unexpected error: {e}")
#             logger.error(f"Failed to place order due to an unexpected error: {e}")
#             return None

#     def _display_order_details(self, order):
#         """
#         Prints formatted order details.
#         """
#         if not order:
#             logger.info("No order details to display.")
#             return

#         print("\n--- Order Details ---")
#         print(f"Order ID: {order.get('orderId')}")
#         print(f"Client Order ID: {order.get('clientOrderId')}")
#         print(f"Symbol: {order.get('symbol')}")
#         print(f"Side: {order.get('side')}")
#         print(f"Order Type: {order.get('type')}")
#         print(f"Status: {order.get('status')}")
#         print(f"Original Quantity: {order.get('origQty')}")
#         print(f"Executed Quantity: {order.get('executedQty')}")
#         print(f"Price: {order.get('price')}")
#         if 'stopPrice' in order and order['stopPrice']:
#             print(f"Stop Price: {order.get('stopPrice')}")
#         print(f"Cum Quote Quantity: {order.get('cumQuote')}")
#         print(f"Time in Force: {order.get('timeInForce')}")
#         print(f"Update Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(order.get('updateTime', 0) / 1000.0))} UTC")
#         print("---------------------")

#     def get_open_orders(self, symbol=None):
#         """
#         Retrieves all open orders or open orders for a specific symbol.
#         """
#         try:
#             if symbol:
#                 open_orders = self.client.futures_get_open_orders(symbol=symbol.upper())
#                 logger.info(f"Open orders for {symbol}:")
#             else:
#                 open_orders = self.client.futures_get_open_orders()
#                 logger.info("All open orders:")

#             if not open_orders:
#                 logger.info("No open orders found.")
#                 return []

#             for order in open_orders:
#                 self._display_order_details(order)
#             return open_orders
#         except BinanceAPIException as e:
#             self._log_api_call("GET", "/fapi/v1/openOrders", params={'symbol': symbol}, error=f"Binance API Error: {e.code} - {e.message}")
#             logger.error(f"Failed to retrieve open orders: Binance API Error {e.code} - {e.message}")
#             return []
#         except BinanceRequestException as e:
#             self._log_api_call("GET", "/fapi/v1/openOrders", params={'symbol': symbol}, error=f"Request Error: {e}")
#             logger.error(f"Failed to retrieve open orders: Request Error {e}")
#             return []
#         except Exception as e:
#             self._log_api_call("GET", "/fapi/v1/openOrders", params={'symbol': symbol}, error=f"An unexpected error: {e}")
#             logger.error(f"Failed to retrieve open orders due to an unexpected error: {e}")
#             return []

#     def cancel_order(self, symbol, order_id=None, client_order_id=None):
#         """
#         Cancels an open order by order ID or client order ID.
#         """
#         if not order_id and not client_order_id:
#             logger.error("Either order_id or client_order_id must be provided to cancel an order.")
#             return None

#         params = {'symbol': symbol.upper()}
#         if order_id:
#             params['orderId'] = order_id
#         if client_order_id:
#             params['origClientOrderId'] = client_order_id

#         try:
#             logger.info(f"Attempting to cancel order: {params}")
#             self._log_api_call("DELETE", "/fapi/v1/order", params=params)
#             result = self.client.futures_cancel_order(**params)
#             self._log_api_call("DELETE", "/fapi/v1/order", params=params, response=result)
#             logger.info(f"Order {order_id if order_id else client_order_id} for {symbol} cancelled successfully.")
#             self._display_order_details(result)
#             return result
#         except BinanceAPIException as e:
#             self._log_api_call("DELETE", "/fapi/v1/order", params=params, error=f"Binance API Error: {e.code} - {e.message}")
#             logger.error(f"Failed to cancel order: Binance API Error {e.code} - {e.message}")
#             return None
#         except BinanceRequestException as e:
#             self._log_api_call("DELETE", "/fapi/v1/order", params=params, error=f"Request Error: {e}")
#             logger.error(f"Failed to cancel order: Request Error {e}")
#             return None
#         except Exception as e:
#             self._log_api_call("DELETE", "/fapi/v1/order", params=params, error=f"An unexpected error: {e}")
#             logger.error(f"Failed to cancel order due to an unexpected error: {e}")
#             return None

# def validate_positive_float(prompt):
#     while True:
#         try:
#             value = float(input(prompt))
#             if value <= 0:
#                 print("Input must be a positive number.")
#             else:
#                 return value
#         except ValueError:
#             print("Invalid input. Please enter a number.")

# def validate_symbol(prompt):
#     while True:
#         symbol = input(prompt).strip().upper()
#         if symbol and symbol.endswith('USDT'): # Basic validation for USDT-M futures
#             return symbol
#         else:
#             print("Invalid symbol. Please enter a symbol ending with 'USDT' (e.g., BTCUSDT).")

# def validate_side(prompt):
#     while True:
#         side = input(prompt).strip().upper()
#         if side in ['BUY', 'SELL']:
#             return side
#         else:
#             print("Invalid side. Please enter 'BUY' or 'SELL'.")

# def validate_order_type(prompt):
#     while True:
#         order_type = input(prompt).strip().upper()
#         if order_type in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
#             return order_type
#         else:
#             print("Invalid order type. Please choose from 'MARKET', 'LIMIT', 'STOP_LIMIT'.")


# def main():
#     bot = BasicBot(API_KEY, API_SECRET, testnet=True)

#     while True:
#         print("\n--- Binance Futures Testnet Bot ---")
#         print("1. Get Account Balance")
#         print("2. Place New Order")
#         print("3. View Open Orders")
#         print("4. Cancel Order")
#         print("5. Exit")

#         choice = input("Enter your choice: ").strip()

#         if choice == '1':
#             bot.get_account_balance()
#         elif choice == '2':
#             symbol = validate_symbol("Enter symbol (e.g., BTCUSDT): ")
#             side = validate_side("Enter side (BUY/SELL): ")
#             order_type = validate_order_type("Enter order type (MARKET/LIMIT/STOP_LIMIT): ")
#             quantity = validate_positive_float("Enter quantity: ")

#             price = None
#             stop_price = None

#             if order_type == 'LIMIT' or order_type == 'STOP_LIMIT':
#                 price = validate_positive_float("Enter limit price: ")
#             if order_type == 'STOP_LIMIT':
#                 stop_price = validate_positive_float("Enter stop price: ")
#                 if (side == 'BUY' and stop_price >= price) or (side == 'SELL' and stop_price <= price):
#                     print("Warning: For a BUY stop-limit, stop price is usually below limit price. For a SELL stop-limit, stop price is usually above limit price. Ensure your stop and limit logic is correct for your strategy.")


#             bot.place_order(symbol, side, order_type, quantity, price, stop_price)
#         elif choice == '3':
#             view_all = input("View all open orders? (yes/no, default: yes): ").strip().lower()
#             if view_all == 'no':
#                 symbol = validate_symbol("Enter symbol to view open orders for: ")
#                 bot.get_open_orders(symbol)
#             else:
#                 bot.get_open_orders()
#         elif choice == '4':
#             symbol = validate_symbol("Enter symbol of the order to cancel: ")
#             order_identifier_choice = input("Cancel by (1) Order ID or (2) Client Order ID? Enter 1 or 2: ").strip()
#             order_id = None
#             client_order_id = None
#             if order_identifier_choice == '1':
#                 try:
#                     order_id = int(input("Enter Order ID: "))
#                 except ValueError:
#                     print("Invalid Order ID. Please enter a number.")
#                     continue
#             elif order_identifier_choice == '2':
#                 client_order_id = input("Enter Client Order ID: ").strip()
#                 if not client_order_id:
#                     print("Client Order ID cannot be empty.")
#                     continue
#             else:
#                 print("Invalid choice. Please enter 1 or 2.")
#                 continue

#             bot.cancel_order(symbol, order_id=order_id, client_order_id=client_order_id)
#         elif choice == '5':
#             print("Exiting bot. Goodbye!")
#             sys.exit(0)
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main()





# --- IMPORTS ---
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException, BinanceRequestException

import sys
import os
import time
import logging

import tkinter.messagebox as messagebox
import customtkinter as ctk # This is likely why you have CustomTkinter
import tkinter as tk
import json # For pretty printing account info
# NEW: Tkinter or CustomTkinter for GUI
try:
    import customtkinter as ctk # Try CustomTkinter for a modern look
    ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"
except ImportError:
    import tkinter as ctk # Fallback to standard Tkinter
    from tkinter import messagebox, scrolledtext # Import message box and scrolled text widgets
    print("CustomTkinter not found, falling back to standard Tkinter.")


# --- CONFIGURE LOGGING (Modified to also output to GUI text box) ---
# We'll create a custom handler to direct logs to the GUI
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        def append_log():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(ctk.END, msg + "\n")
            self.text_widget.configure(state='disabled')
            self.text_widget.see(ctk.END) # Auto-scroll to the end
        # Use after() to safely update GUI from a non-GUI thread if needed
        # Though in this simple setup, calls will be on main thread.
        self.text_widget.after(0, append_log)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- API_KEY & API_SECRET (ensure these are loaded from config.py or set directly) ---
# Assuming you have API_KEY and API_SECRET defined, e.g.:
API_KEY = "9714dd00eb399ce87b0124e0cc154b180d692947bce3dba29cd85a28daf70464" # REPLACE WITH YOUR KEY
API_SECRET = "a95875ad1c515f8e809cd73d75788fc0a953ee7293c9cc7ac8910a24ca6851de" # REPLACE WITH YOUR SECRET


# --- BasicBot Class (UNCHANGED CORE LOGIC, but methods will be called by GUI) ---
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = None # Initialize to None, set in _check_connection

        # Connection check will now happen explicitly after GUI setup
        # self._check_connection() # Don't call here, call from GUI app

    def _check_connection(self):
        try:
            if self.client is None: # Only create client if not already created
                if self.testnet:
                    logger.info("Attempting to connect to Binance Futures Testnet...")
                    self.client = Client(self.api_key, self.api_secret, tld='com', testnet=True)
                else:
                    logger.info("Attempting to connect to Binance Futures Mainnet...")
                    self.client = Client(self.api_key, self.api_secret, tld='com')

            server_time = self.client.get_server_time()
            logger.info(f"Successfully connected to Binance Futures Testnet. Server time: {time.ctime(server_time['serverTime']/1000)}")
            return True
        except BinanceAPIException as e:
            logger.error(f"Binance API Error during connection check: {e.message}")
            return False
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error during connection check: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error during connection check: {e}")
            return False

    def get_account_balance(self):
        if not self.client or not self._check_connection():
            logger.error("Not connected to Binance. Please connect first.")
            return

        try:
            balances = self.client.futures_account_balance()
            logger.info("--- Futures Account Balances ---")
            found_positive_balance = False
            for balance in balances:
                if float(balance['balance']) > 0:
                    found_positive_balance = True
                    logger.info(f"  Asset: {balance['asset']}, Balance: {float(balance['balance']):.8f}, Available: {float(balance['availableBalance']):.8f}")
            if not found_positive_balance:
                logger.info("  No positive balances found. Use the Testnet faucet to get funds.")

            account_info = self.client.futures_account()
            logger.info("--- Futures Account Info (Partial) ---")
            logger.info(f"  Total Wallet Balance: {float(account_info.get('totalWalletBalance', '0.0')):.8f}")
            logger.info(f"  Total Unrealized Profit: {float(account_info.get('totalUnrealizedProfit', '0.0')):.8f}")

        except BinanceAPIException as e:
            logger.error(f"Binance API Error in get_account_balance: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error in get_account_balance: {e}")
        except Exception as e:
            logger.error(f"An unexpected error in get_account_balance: {e}")

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        if not self.client or not self._check_connection():
            logger.error("Not connected to Binance. Please connect first.")
            return

        try:
            order = None
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }

            if order_type.upper() == 'MARKET':
                order = self.client.futures_create_order(**params)
            elif order_type.upper() == 'LIMIT':
                if price is None:
                    logger.error("Price is required for a LIMIT order.")
                    return
                params['timeInForce'] = 'GTC'
                params['price'] = price
                order = self.client.futures_create_order(**params)
            elif order_type.upper() == 'STOP_LIMIT':
                if price is None or stop_price is None:
                    logger.error("Price and Stop Price are required for a STOP_LIMIT order.")
                    return
                params['timeInForce'] = 'GTC'
                params['price'] = price
                params['stopPrice'] = stop_price
                order = self.client.futures_create_order(**params)
            else:
                logger.warning(f"Unsupported order type: {order_type}")
                return

            logger.info(f"Order placed successfully: {json.dumps(order, indent=2)}") # Pretty print order
            return order # Return order details for UI confirmation

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.code} - {e.message}")
            logger.error(f"Cannot place order for {symbol}: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error: {e}")
            logger.error(f"Cannot place order for {symbol}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error in place_order: {e}")
            logger.error(f"Cannot place order for {symbol}: {e}")
        return None # Indicate failure

    def view_open_orders(self, symbol=None):
        if not self.client or not self._check_connection():
            logger.error("Not connected to Binance. Please connect first.")
            return

        try:
            if symbol:
                open_orders = self.client.futures_get_open_orders(symbol=symbol.upper())
                logger.info(f"--- Open Orders for {symbol.upper()} ---")
            else:
                open_orders = self.client.futures_get_open_orders()
                logger.info("--- All Open Orders ---")

            if not open_orders:
                logger.info("  No open orders found.")
                return

            for order in open_orders:
                logger.info(f"  Order ID: {order['orderId']}, Symbol: {order['symbol']}, Side: {order['side']}, Type: {order['type']}, "
                            f"Status: {order['status']}, Price: {float(order['price']):.8f}, Quantity: {float(order['origQty']):.8f}, "
                            f"Executed Qty: {float(order['executedQty']):.8f}")

        except BinanceAPIException as e:
            logger.error(f"Binance API Error in view_open_orders: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error in view_open_orders: {e}")
        except Exception as e:
            logger.error(f"An unexpected error in view_open_orders: {e}")

    def cancel_order(self, symbol, order_id):
        if not self.client or not self._check_connection():
            logger.error("Not connected to Binance. Please connect first.")
            return

        try:
            result = self.client.futures_cancel_order(symbol=symbol.upper(), orderId=order_id)
            logger.info(f"Order {order_id} for {symbol.upper()} cancelled successfully: {json.dumps(result, indent=2)}")
            return True
        except BinanceAPIException as e:
            logger.error(f"Binance API Error in cancel_order: {e.code} - {e.message}")
            logger.error(f"Cannot cancel order {order_id} for {symbol}: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error in cancel_order: {e}")
            logger.error(f"Cannot cancel order {order_id} for {symbol}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error in cancel_order: {e}")
            logger.error(f"Cannot cancel order {order_id} for {symbol}: {e}")
        return False


# --- NEW: GUI Application Class ---
class TradingApp(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Binance Futures Testnet Bot")
        self.geometry("800x600")

        self.bot = BasicBot(API_KEY, API_SECRET, testnet=True)

        self._create_widgets()
        self._setup_logging_to_gui()
        logger.info("GUI application started. Click 'Connect to Binance' to begin.")

    def _create_widgets(self):
        # Frame for controls
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, padx=10, fill="x")

        # Connect button
        connect_btn = ctk.CTkButton(control_frame, text="Connect to Binance", command=self.connect_to_binance)
        connect_btn.grid(row=0, column=0, padx=5, pady=5)

        # Balance button
        balance_btn = ctk.CTkButton(control_frame, text="Get Account Balance", command=self.get_balance)
        balance_btn.grid(row=0, column=1, padx=5, pady=5)

        # Place Order button (opens a new window/dialog)
        place_order_btn = ctk.CTkButton(control_frame, text="Place New Order", command=self.open_place_order_dialog)
        place_order_btn.grid(row=0, column=2, padx=5, pady=5)

        # View Open Orders button
        view_orders_btn = ctk.CTkButton(control_frame, text="View Open Orders", command=self.view_open_orders_gui)
        view_orders_btn.grid(row=0, column=3, padx=5, pady=5)

        # Cancel Order button
        cancel_order_btn = ctk.CTkButton(control_frame, text="Cancel Order", command=self.open_cancel_order_dialog)
        cancel_order_btn.grid(row=0, column=4, padx=5, pady=5)

        # Log output area
        self.log_text = ctk.CTkTextbox(self, wrap="word", state="disabled") # Use CTkTextbox for CustomTkinter
        self.log_text.pack(pady=10, padx=10, fill="both", expand=True)

    def _setup_logging_to_gui(self):
        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        # Add our custom handler
        text_handler = TextHandler(self.log_text)
        logger.addHandler(text_handler)
        # Also add a file handler to keep logs in a file
        file_handler = logging.FileHandler("trading_bot.log")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)


    def connect_to_binance(self):
        if self.bot._check_connection():
            messagebox.showinfo("Connection Status", "Successfully connected to Binance Futures Testnet.")
        else:
            messagebox.showerror("Connection Status", "Failed to connect to Binance. Check logs for details.")

    def get_balance(self):
        self.bot.get_account_balance()

    def open_place_order_dialog(self):
        dialog = ctk.CTkToplevel(self) # Use CTkToplevel for a new window in CustomTkinter
        dialog.title("Place New Order")
        dialog.geometry("400x500")

        # Labels and Entry fields for order details
        labels = ["Symbol:", "Side (BUY/SELL):", "Type (MARKET/LIMIT/STOP_LIMIT):", "Quantity:", "Limit Price (for LIMIT/STOP_LIMIT):", "Stop Price (for STOP_LIMIT):"]
        self.order_entries = {}
        for i, text in enumerate(labels):
            label = ctk.CTkLabel(dialog, text=text)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(dialog)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.order_entries[text.split('(')[0].strip().replace(':', '').lower().replace(' ', '_')] = entry

        # Place Order Button
        place_btn = ctk.CTkButton(dialog, text="Place Order", command=self.place_order_from_dialog)
        place_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def place_order_from_dialog(self):
        symbol = self.order_entries['symbol'].get()
        side = self.order_entries['side'].get()
        order_type = self.order_entries['type'].get().upper()
        quantity_str = self.order_entries['quantity'].get()
        price_str = self.order_entries['limit_price'].get()
        stop_price_str = self.order_entries['stop_price'].get()

        try:
            quantity = float(quantity_str)
            price = float(price_str) if price_str else None
            stop_price = float(stop_price_str) if stop_price_str else None
        except ValueError:
            messagebox.showerror("Input Error", "Quantity, Limit Price, and Stop Price must be numbers.")
            return

        # Basic input validation
        if not symbol or not side or not order_type or quantity <= 0:
            messagebox.showerror("Input Error", "Symbol, Side, Type, and Quantity are required.")
            return

        if order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
            messagebox.showerror("Input Error", "Order Type must be MARKET, LIMIT, or STOP_LIMIT.")
            return

        if (order_type == 'LIMIT' or order_type == 'STOP_LIMIT') and price is None:
            messagebox.showerror("Input Error", "Limit Price is required for LIMIT and STOP_LIMIT orders.")
            return

        if order_type == 'STOP_LIMIT' and stop_price is None:
            messagebox.showerror("Input Error", "Stop Price is required for STOP_LIMIT orders.")
            return

        # Call the bot's place_order method
        order_details = self.bot.place_order(symbol, side, order_type, quantity, price, stop_price)
        if order_details:
            messagebox.showinfo("Order Placed", f"Order {order_details['orderId']} for {symbol} placed successfully!")


    def view_open_orders_gui(self):
        # Simple dialog to ask for symbol (optional)
        symbol_dialog = ctk.CTkInputDialog(text="Enter symbol (optional, leave blank for all):", title="View Open Orders")
        symbol = symbol_dialog.get_input()
        if symbol is not None: # User didn't cancel
            self.bot.view_open_orders(symbol if symbol.strip() else None)


    def open_cancel_order_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cancel Order")
        dialog.geometry("300x200")

        ctk.CTkLabel(dialog, text="Symbol:").pack(pady=5)
        self.cancel_symbol_entry = ctk.CTkEntry(dialog)
        self.cancel_symbol_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Order ID:").pack(pady=5)
        self.cancel_order_id_entry = ctk.CTkEntry(dialog)
        self.cancel_order_id_entry.pack(pady=5)

        cancel_btn = ctk.CTkButton(dialog, text="Cancel Order", command=self.cancel_order_from_dialog)
        cancel_btn.pack(pady=10)

    def cancel_order_from_dialog(self):
        symbol = self.cancel_symbol_entry.get()
        order_id_str = self.cancel_order_id_entry.get()

        if not symbol or not order_id_str:
            messagebox.showerror("Input Error", "Symbol and Order ID are required.")
            return

        try:
            order_id = int(order_id_str)
        except ValueError:
            messagebox.showerror("Input Error", "Order ID must be a number.")
            return

        if self.bot.cancel_order(symbol, order_id):
            messagebox.showinfo("Order Cancelled", f"Order {order_id} for {symbol} cancelled.")
        # Error messages handled by bot.cancel_order itself via logger

# --- Main execution block ---
if __name__ == '__main__':
    app = TradingApp()
    app.mainloop()