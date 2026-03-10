## FastAPI Shop Backend

This project is a simple **e‑commerce backend** built with FastAPI and SQLAlchemy.  
It exposes REST APIs for browsing product categories, listing products, and managing a lightweight shopping cart on the client side.  
The goal is to demonstrate a clean service / repository architecture with Pydantic schemas and a SQLite database.

### Project Structure

- **backend/**
  - **run.py** – entry point to start the FastAPI application with Uvicorn.
  - **requirements.txt** – Python dependencies used by the backend.
- **backend/app/**
  - **main.py** – FastAPI application instance, CORS configuration, static files mount, and router registration.
  - **config.py** – application settings (app name, debug flag, database URL, CORS origins, static paths) using `pydantic-settings`.
  - **database.py** – SQLAlchemy engine, session factory, base model and database initialization helpers.
  - **models/** – SQLAlchemy ORM models:
    - `product.py` – `Product` table (name, description, price, category, image URL, timestamps).
    - `category.py` – `Category` table (name, slug, relation to products).
  - **schemas/** – Pydantic models for request and response validation:
    - `product.py` – product input/output and list response schemas.
    - `category.py` – category input/output schemas.
    - `cart.py` – cart items, cart summary, and request payload schemas.
  - **repositories/** – data access layer (CRUD and query methods for products and categories).
  - **services/** – business logic:
    - `product_service.py` – product retrieval and creation, including validation.
    - `category_service.py` – category retrieval and creation.
    - `cart_service.py` – cart manipulation and calculation of totals.
  - **routes/** – API routers:
    - `products.py` – product endpoints.
    - `categories.py` – category endpoints.
    - `cart.py` – cart endpoints.
  - **static/** – static assets (e.g. images) served under `/static`.
- **backend/seed_data.py** – script to populate the database with demo categories and products.

### Technologies Used

- **FastAPI** – web framework for building the HTTP API.
- **Uvicorn** – ASGI server used to run the FastAPI app.
- **SQLAlchemy** – ORM and database abstraction layer.
- **SQLite** – default database (configurable via `database_url`).
- **Pydantic v2** – data validation and serialization for request/response models.
- **pydantic-settings** – configuration management via environment variables and `.env`.

### Running the Backend

#### 1. Create and activate a virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure environment (optional)

You can override defaults from `config.py` using a `.env` file in `backend/app/`:

```env
APP_NAME="FastAPI Shop"
DEBUG=true
DATABASE_URL="sqlite:///./shop.db"
```

The most important setting is **`DATABASE_URL`** if you want to use a different database.

#### 4. Initialize and seed the database (optional but recommended)

By default, tables are created automatically during app startup (`init_db()` in `lifespan`).  
To also fill the database with demo categories and products, run:

```bash
cd backend
python seed_data.py
```

#### 5. Start the API server

From the `backend` directory:

```bash
python run.py
```

The app will be available at `http://127.0.0.1:8000`.

- **Root endpoint**: `GET /` – returns a simple greeting and a link to the docs.
- **Health check**: `GET /healthcheck` – returns the current status.

Interactive documentation:

- **Swagger UI**: `http://127.0.0.1:8000/api/docs`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc`

Static files are served from the `static` directory under:

- `GET /static/...`

### Main API Endpoints

All business endpoints are prefixed with `/api`.

#### Categories

- **GET `/api/categories`**
  - **Description**: Get a list of all categories.
  - **Response**: `200 OK` – array of category objects:
    - `id`, `name`, `slug`.

- **GET `/api/categories/{category_id}`**
  - **Description**: Get a single category by its ID.
  - **Path params**:
    - `category_id` – integer category ID.
  - **Response**: `200 OK` – category object.
  - **Errors**:
    - `404 NOT FOUND` – if category does not exist.

#### Products

- **GET `/api/products`**
  - **Description**: Get all products.
  - **Response**: `200 OK` – object:
    - `products` – array of products.
    - `total` – total number of products.

- **GET `/api/products/{product_id}`**
  - **Description**: Get a single product by its ID.
  - **Path params**:
    - `product_id` – integer product ID.
  - **Response**: `200 OK` – product object including category.
  - **Errors**:
    - `404 NOT FOUND` – if product does not exist.

- **GET `/api/products/category/{category_id}`**
  - **Description**: Get all products that belong to a specific category.
  - **Path params**:
    - `category_id` – integer category ID.
  - **Response**: `200 OK` – object with `products` and `total`.
  - **Errors**:
    - `404 NOT FOUND` – if the category does not exist.

#### Cart

The cart is stored and managed on the **client side** as a dictionary of `{product_id: quantity}`.  
The API receives the cart state, applies operations, and returns the updated cart or a detailed view.

- **POST `/api/cart`**
  - **Description**: Get detailed cart information (prices, subtotals, totals).
  - **Request body**:
    - `cart`: object mapping product IDs to quantities, e.g.:

```json
{
  "cart": {
    "1": 2,
    "3": 1
  }
}
```

  - **Response**: `200 OK` – `CartResponse`:
    - `items` – array with `product_id`, `name`, `price`, `quantity`, `subtotal`, `image_url`.
    - `total` – total price of all items.
    - `items_count` – total quantity of items.

- **POST `/api/cart/add`**
  - **Description**: Add a product to the cart (or increase quantity).
  - **Request body** (`AddToCartRequest`):

```json
{
  "product_id": 1,
  "quantity": 2,
  "cart": {
    "1": 1,
    "3": 1
  }
}
```

  - **Response**: `200 OK`:

```json
{
  "cart": {
    "1": 3,
    "3": 1
  }
}
```

  - **Errors**:
    - `404 NOT FOUND` – if the product does not exist.

- **PUT `/api/cart/update`**
  - **Description**: Update the quantity of an item in the cart.
  - **Request body** (`UpdateCartRequest`):

```json
{
  "product_id": 1,
  "quantity": 5,
  "cart": {
    "1": 3,
    "3": 1
  }
}
```

  - **Response**: `200 OK`:

```json
{
  "cart": {
    "1": 5,
    "3": 1
  }
}
```

  - **Errors**:
    - `404 NOT FOUND` – if the product ID is not present in the cart.

- **DELETE `/api/cart/remove/{product_id}`**
  - **Description**: Remove an item from the cart.
  - **Path params**:
    - `product_id` – integer product ID to remove.
  - **Request body** (`RemoveFromCartRequest`):

```json
{
  "cart": {
    "1": 5,
    "3": 1
  }
}
```

  - **Response**: `200 OK`:

```json
{
  "cart": {
    "3": 1
  }
}
```

  - **Errors**:
    - `404 NOT FOUND` – if the product ID is not present in the cart.

### Notes

- Error responses use standard HTTP status codes and messages from FastAPI.
- CORS is configured to allow typical local frontend development origins (e.g. `http://localhost:5173`).
- You can use the interactive docs to test all endpoints and inspect request/response schemas.

