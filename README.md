# API Documentation for FastAPI Project

## Overview
This project is a FastAPI-based application for managing orders, products, and users for a business that sells dairy and flowers. The API supports two roles: `admin` and `user`, and provides functionality for order placement, product management, authentication using OTP, and location-based features.

---

## Authentication Endpoints

- **`POST /send-otp`**: Send an OTP to a user's email.
  - **Body:**
    ```json
    {
      "email": "user@example.com"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "OTP sent successfully"
    }
    ```

- **`POST /verify-otp`**: Verify OTP and log in or register the user.
  - **Body:**
    ```json
    {
      "email": "user@example.com",
      "otp": 123456
    }
    ```
  - **Response:**
    ```json
    {
      "verified": true,
      "access_token": "<jwt-token>",
      "token_type": "bearer",
      "redirect_url": "https://yourdomain.com/home",
      "message": "User verified successfully"
    }
    ```

---

## Admin Endpoints

### Category Management

- **`POST /admin/category/add`**: Add a new category.
  - **Body:**
    ```json
    {
      "name": "Dairy"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Category added successfully"
    }
    ```

- **`GET /admin/categories`**: Retrieve all categories.
  - **Response:**
    ```json
    [
      {"name": "Dairy"},
      {"name": "Flowers"}
    ]
    ```

- **`DELETE /admin/category/delete/{name}`**: Delete a category by name.
  - **Response:**
    ```json
    {
      "message": "Category deleted successfully"
    }
    ```

### Product Management

- **`POST /admin/product/add`**: Add a new product.
  - **Body:**
    ```json
    {
      "product_id": "product1",
      "name": "Milk",
      "category": "Dairy",
      "price": 50.0,
      "stock": 100,
      "description": "Fresh cow milk"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Product added successfully"
    }
    ```

- **`GET /admin/products`**: Retrieve all products.
  - **Response:**
    ```json
    [
      {
        "product_id": "product1",
        "name": "Milk",
        "category": "Dairy",
        "price": 50.0,
        "stock": 100,
        "description": "Fresh cow milk"
      }
    ]
    ```

### Order Management

- **`POST /admin/orders/insert`**: Insert multiple orders.
  - **Body:**
    ```json
    [
      {
        "order_id": "order1",
        "user_id": "user1",
        "products": [
          {"product_id": "product1", "quantity": 2}
        ],
        "total_price": 100.0,
        "status": "pending"
      }
    ]
    ```
  - **Response:**
    ```json
    {
      "message": "Orders inserted successfully",
      "orders": ["order1"]
    }
    ```

- **`GET /admin/orders`**: Retrieve all orders.
  - **Response:**
    ```json
    {
      "orders": [
        {
          "order_id": "order1",
          "user_id": "user1",
          "products": [
            {"product_id": "product1", "quantity": 2}
          ],
          "total_price": 100.0,
          "status": "pending",
          "order_date": "2025-02-16T10:00:00Z"
        }
      ]
    }
    ```

- **`DELETE /admin/orders/delete/{order_id}`**: Delete an order.
  - **Response:**
    ```json
    {
      "message": "Order 'order1' deleted successfully"
    }
    ```

---

## User Endpoints

- **`GET /user/profile`**: Get the profile of the logged-in user.
  - **Response:**
    ```json
    {
      "user_id": "user1",
      "email": "user@example.com",
      "username": "user",
      "role": "user",
      "is_verified": true
    }
    ```

- **`PUT /user/profile/update`**: Update the user's profile.
  - **Body:**
    ```json
    {
      "username": "newusername"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Profile updated successfully"
    }
    ```

---

## Order Endpoints

- **`POST /orders/create`**: Place a new order.
  - **Body:**
    ```json
    {
      "products": [
        {"product_id": "product1", "quantity": 2}
      ],
      "total_price": 100.0
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Order created successfully",
      "order_id": "order1"
    }
    ```

- **`GET /orders/history`**: Retrieve the order history for the logged-in user.
  - **Response:**
    ```json
    {
      "history": [
        {
          "order_id": "order1",
          "products": [
            {"product_id": "product1", "quantity": 2}
          ],
          "total_price": 100.0,
          "status": "delivered",
          "order_date": "2025-02-16T10:00:00Z"
        }
      ]
    }
    ```

- **`PUT /orders/update-status/{order_id}`**: Update the status of an order.
  - **Body:**
    ```json
    {
      "status": "shipped"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Order status updated to shipped"
    }
    ```

---

## Subscription Endpoints

- **`POST /subscriptions/create`**: Create a new subscription.
  - **Body:**
    ```json
    {
      "user_id": "user1",
      "product_id": "product1",
      "frequency": "weekly"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Subscription created successfully"
    }
    ```

- **`GET /subscriptions`**: Retrieve all subscriptions for the logged-in user.
  - **Response:**
    ```json
    [
      {
        "subscription_id": "sub1",
        "product_id": "product1",
        "frequency": "weekly"
      }
    ]
    ```

- **`DELETE /subscriptions/delete/{subscription_id}`**: Delete a subscription.
  - **Response:**
    ```json
    {
      "message": "Subscription deleted successfully"
    }
    ```

---

### Notes:
- Order statuses include `pending`, `shipped`, and `delivered`. Delivered orders are automatically moved to order history.
- Location is fetched using the IP API at `https://ipapi.co/json/`.
- Authentication uses OTP-based login without passwords.
- User actions are restricted based on their assigned category access.

## Run the Project

```bash
uvicorn main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`.

