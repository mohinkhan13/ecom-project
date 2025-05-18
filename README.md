# 🛒 E-Commerce Project (Django)

This is a beginner-friendly e-commerce web application built using the Django framework. The project aims to simulate a basic online shopping experience and can be extended with features like cart, checkout, user login, and payment gateway integration.

![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/HomePage.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/Producthome.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/Product_home2.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/ProductDetail.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/cart.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/wishlist.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/myorders.png)
![Project Screenshot](https://github.com/mohinkhan13/ecom-project/blob/main/media/orderDetail.png)

## 🚀 Features

- 🏠 Home Page 
- 🛍️ Product Listing 
- 🔍 Product Detail Page 
- ➕ Add to Cart
- 🛒 View Cart
- 💳 Checkout System
- 👤 User Authentication (Login & Signup)
- 📦 Order Tracking
- ⚙️ Admin Panel for Product Management (Working)
- 🔎 Search and Filter Products

## 📁 Project Structure

```
ecom-project/
├── ecom_project/        # Django project configuration
├── myapp/               # Main application
│   ├── views.py         # Contains the home view
│   ├── urls.py          # App-level URLs
│   └── templates/
│       └── home.html    # Homepage template
├── db.sqlite3           # SQLite database
└── manage.py            # Django project manager
```

## ⚙️ Installation & Setup

Follow the steps below to run this project on your local machine:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/ecom-project.git
   cd ecom-project
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Open in Browser**

   Visit: `http://127.0.0.1:8000/`

## 🔧 Future Improvements

- Product category and filtering system
- Add to cart and remove from cart logic
- Secure checkout with payment integration
- User registration and login system
- Improved UI using Bootstrap or Tailwind CSS
- REST API integration for frontend/backend separation

## 🙋‍♂️ Author

**Your Name**  
[GitHub Profile]([https://github.com/your-username](https://github.com/mohinkhan13))

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
