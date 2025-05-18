# 🛒 E-Commerce Project (Django)

This is a full-featured e-commerce web application built using the Django framework. It supports both **buyer** and **seller** roles and includes features like user authentication, product listing, wishlist, cart management, online payment via Stripe, and order tracking.

---

## 🖼️ Project Screenshot

![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/HomePage.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/Producthome.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/Product_home2.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/ProductDetail.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/cart.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/wishlist.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/myorders.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/orderDetail.png)


---

## 🚀 Key Features

### 👤 User Management

* Register as Buyer or Seller
* Login / Logout functionality
* Change & reset password (OTP-based via mobile)
* Profile update with image upload

### 📅 Product Management (Seller)

* Add, edit, delete products
* Manage categories
* View product-wise inventory
* Update stock levels
* View seller orders & order details

### 🌟 Product Display (Buyer)

* View all products or filter by category
* See featured, hot trend, and best seller sections
* View product details with related products

### ❤️ Wishlist & Cart

* Add/remove items from wishlist
* Add/remove/update items in cart
* View total price, quantity

### 💳 Payment & Checkout

* Checkout system integrated with Stripe
* Create Stripe session & handle success/cancel pages
* View order summary after payment

### 📆 Orders

* Buyers can view order history & order details
* Sellers can view their received orders

### 🛍️ Misc Pages

* About Us
* Contact Page

---

## 📂 Project Structure

```bash
ecom-project/
├── ecom_project/            # Django project settings
├── myapp/                   # Main app containing views, models, templates
│   ├── views.py             # All function-based views
│   ├── urls.py              # Route definitions
│   ├── templates/           # HTML templates (buyers & sellers)
│   └── static/              # Static files (CSS, JS, images)
├── db.sqlite3               # SQLite database
└── manage.py                # Django entry point
```

---

## ⚙️ How to Run This Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecom-project.git
cd ecom-project
```

### 2. Create a virtual environment and activate it

```bash
python -m venv env
source env/bin/activate        # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Access in your browser

```
http://127.0.0.1:8000/
```

---

## 🔄 Future Enhancements

* Add product reviews and ratings
* Email-based verification
* Pagination and filtering
* REST API support with DRF
* Responsive UI with Tailwind CSS
* Advanced admin dashboard for analytics

---

## 👨‍💻 Author

**Your Name**
[GitHub Profile](https://github.com/mohinkhan13)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
