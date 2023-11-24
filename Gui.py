import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from ttkthemes import ThemedStyle
from order_management_system import OrderManagementSystem

class OrderManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Management System")
        self.oms = OrderManagementSystem()

        # Apply themed style
        self.style = ThemedStyle(self.root)
        self.style.set_theme("clam")  # You can try different themes

        self.style.configure("Main.TLabel", background="#4682B4", foreground="#FFFFFF", font=('Arial', 14))  # White Text
        self.style.configure("TButton", background="#FF4500", foreground="#FFFFFF", font=('Arial', 12))  # White Text, Red Button
        self.style.configure("TFrame", background="#87CEEB")  # Sky Blue Background
        self.style.configure("TListbox", background="#87CEEB", foreground="#000000", font=('Arial', 12))  # Black Text

        self.create_widgets()
    
    def create_widgets(self):
        self.root.configure(bg="#87CEEB")
        # Header
        header_frame = ttk.Frame(self.root, padding=(10, 5))
        ttk.Label(header_frame, text="QuickOrder Pro", font=('Arial', 16, 'bold')).pack()
        header_frame.pack(pady=10)

        # Customer Name Entry
        customer_frame = ttk.Frame(self.root, padding=(10, 5))
        self.customer_name_label = ttk.Label(customer_frame, text="Enter your name:", style="Main.TLabel")
        self.customer_name_label.grid(row=0, column=0, pady=5, sticky='w')
        self.customer_name_entry = ttk.Entry(customer_frame, font=('Arial', 12))
        self.customer_name_entry.grid(row=0, column=1, pady=5, sticky='w')
        customer_frame.pack(pady=10)

        # Product List
        product_frame = ttk.Frame(self.root, padding=(10, 5), style="TFrame")
        product_frame.pack(pady=10, padx=20)

        self.products_label = ttk.Label(product_frame, text="Available Products:", style="Main.TLabel")
        self.products_label.grid(row=0, column=0, columnspan=2, pady=5, sticky='w')

        self.product_listbox = tk.Listbox(product_frame, selectmode=tk.MULTIPLE, font=('Arial', 12), bg="#87CEEB", fg="#000000", width=40)
        for product in self.oms.products:
            self.product_listbox.insert(tk.END, f"{product.product_id}: {product.name} - ₹{product.price}")
        self.product_listbox.grid(row=1, column=0, columnspan=2, pady=5, sticky='w')
        
        # Add a scroll bar
        scrollbar = ttk.Scrollbar(product_frame, orient=tk.VERTICAL, command=self.product_listbox.yview)
        scrollbar.grid(row=1, column=2, pady=5, sticky='ns')
        self.product_listbox.config(yscrollcommand=scrollbar.set)

        product_frame.pack(pady=10, padx=20)
        # Buttons
        button_frame = ttk.Frame(self.root, padding=(10, 5))
        self.place_order_button = ttk.Button(button_frame, text="Place Order", command=self.place_order)
        self.place_order_button.grid(row=0, column=0, pady=5)

        self.track_order_button = ttk.Button(button_frame, text="Track Order", command=self.track_order)
        self.track_order_button.grid(row=0, column=1, pady=5)

        self.recommend_button = ttk.Button(button_frame, text="Get Recommendation", command=self.get_recommendation)
        self.recommend_button.grid(row=0, column=2, pady=5)

        button_frame.pack(pady=10)

        # Bill Frame
        self.bill_frame = ttk.Frame(self.root, padding=(10, 5))
        self.bill_frame.pack(pady=10)

    def place_order(self):
        customer_name = self.customer_name_entry.get()
        selected_indices = self.product_listbox.curselection()
        if not customer_name or not selected_indices:
            self.show_error("Please enter your name and select at least one product.")
            return

        product_ids = [self.oms.products[i].product_id for i in selected_indices]
        order = self.oms.place_order(customer_name, product_ids)
        self.show_bill(order)

    def track_order(self):
        order_id = simpledialog.askinteger("Track Order", "Enter Order ID:")

        if order_id is not None:
            order = self.oms.get_order(order_id)
            if order:
                self.show_info(f"Order ID: {order_id}\nCustomer Name: {order.customer_name}\nStatus: {order.status}")
            else:
                self.show_info("Order not found")

    def get_recommendation(self):
        customer_name = self.customer_name_entry.get()
        if not customer_name:
            self.show_error("Please enter your name.")
            return

        recommended_product = self.oms.recommend_products(customer_name)
        if recommended_product:
            self.show_info(f"We recommend: {recommended_product.name} - ${recommended_product.price}")
        else:
            self.show_info("No product recommended this time.")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Information", message)

    def show_bill(self, order):
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Order Bill")

        # Update style configurations for the bill window
        bill_window_style = ThemedStyle(bill_window)
        bill_window_style.set_theme("clam")  # You can choose a different theme
        bill_window_style.configure("Main.TLabel", background="#FFFFFF", foreground="#000000", font=('Arial', 12))
        ttk.Label(bill_window, text="Order Bill", font=('Arial', 14, 'bold'), style="Main.TLabel").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(bill_window, text="Order ID:", style="Main.TLabel").grid(row=1, column=0, pady=5, sticky='w')
        ttk.Label(bill_window, text=order.order_id, style="Main.TLabel").grid(row=1, column=1, pady=5, sticky='w')
        ttk.Label(bill_window, text="Customer Name:", style="Main.TLabel").grid(row=2, column=0, pady=5, sticky='w')
        ttk.Label(bill_window, text=order.customer_name, style="Main.TLabel").grid(row=2, column=1, pady=5, sticky='w')
        ttk.Label(bill_window, text="Products:", style="Main.TLabel").grid(row=3, column=0, pady=5, sticky='w')
        products_text = "\n".join([f"{product.name} - ${product.price}" for product in order.products]) 
        ttk.Label(bill_window, text=products_text, style="Main.TLabel").grid(row=3, column=1, pady=5, sticky='w')
        total_price_label = ttk.Label(bill_window, text="Total Price:", style="Main.TLabel")
        total_price_label.grid(row=4, column=0, pady=5, sticky='w')
        total_price = sum(product.price for product in order.products)
        ttk.Label(bill_window, text=f"${total_price}", style="Main.TLabel").grid(row=4, column=1, pady=5, sticky='w')
        status_label = ttk.Label(bill_window, text="Status:", style="Main.TLabel")
        status_label.grid(row=5, column=0, pady=5, sticky='w')
        if order.status == "Placed": 
            ttk.Label(bill_window, text="Order Placed", style="Main.TLabel").grid(row=5, column=1, pady=5, sticky='w')
        else:
            ttk.Label(bill_window, text="Order Not Placed", style="Main.TLabel").grid(row=5, column=1, pady=5, sticky='w')
        bill_window.protocol("WM_DELETE_WINDOW", lambda: self.on_bill_window_close(bill_window))

    def on_bill_window_close(self, bill_window):
        # Reset input fields and selections after closing the bill window
        self.reset_inputs()
        bill_window.destroy()

    def reset_inputs(self):
        # Clear the customer name entry
        self.customer_name_entry.delete(0, tk.END)

        # Clear the product listbox selection
        self.product_listbox.selection_clear(0, tk.END)
if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManagementGUI(root)
    root.mainloop()