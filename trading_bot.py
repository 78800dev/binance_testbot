# --- IMPORTS ---
# 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
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