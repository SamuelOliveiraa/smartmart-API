# SmartMart API

This API was developed as a practical test for the full-stack development internship selection process at **APOLLO SOLUTIONS**. The objective is to provide a set of endpoints to manage products, categories, and sales for a fictional retail system, SmartMart.

## 📝 About the Project

The SmartMart API is a RESTful service built in Python that offers CRUD functionalities for the main entities of a sales system. In addition to basic operations, the API also includes routes for bulk data import and export via CSV files, facilitating integration and data management.

The application uses a clean and modular architecture, separating business logic, database access, and endpoint definitions, which makes it scalable and easy to maintain.

## 💻 Technologies Used

The project was built with the following technologies:

- **Python 3.12:** Main programming language.
- **FastAPI:** High-performance web framework for building APIs.
- **SQLAlchemy:** ORM (Object-Relational Mapper) for interacting with SQL databases.
- **Uvicorn:** ASGI (Asynchronous Server Gateway Interface) server to run the FastAPI application.
- **Pydantic:** For data validation and serialization.
- **SQLite:** Lightweight relational database, used for development and local storage.
- **Pandas:** Used for data manipulation, especially in import/export operations.
- **Vercel:** Configured for simplified API deployment in a serverless environment.

## 📂 Project Structure

The source code is organized as follows:

```
├── api/
│   └── index.py         # Entry point for Vercel deployment
├── app/
│   ├── crud.py          # Data access and manipulation functions (CRUD)
│   ├── database.py      # Database connection configuration
│   ├── main.py          # Main FastAPI application entry point
│   ├── models.py        # SQLAlchemy table model definitions
│   ├── routers.py       # API endpoint (route) definitions
│   └── schemas.py       # Pydantic schema definitions for data validation
├── requirements.txt     # Python dependencies list
├── vercel.json          # Vercel deployment configuration
├── Insomnia_2026-01-08.yaml # Configuration file for Insomnia
└── smartmart.db         # SQLite database file
```

## 🚀 How to Run Locally

Follow the steps below to set up and run the project in your local environment.

### Prerequisites

- Python 3.10 or higher
- Pip (Python package manager)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/smartmart-API.git
    cd smartmart-API
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Execution

With the environment configured, start the Uvicorn development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. The interactive documentation (Swagger UI) can be accessed at `http://127.0.0.1:8000/docs`.

## 🛠️ Using the API with Insomnia

To facilitate testing the endpoints, the project includes a configuration file for the **Insomnia** API client. This file already contains all API routes pre-configured.

### How to import the file into Insomnia:

1.  Open Insomnia.
2.  Go to the main menu (top left corner) and click on **"Import/Export"**.
3.  In the window that opens, click on **"Import Data"** and then **"From File"**.
4.  Select the `Insomnia_2026-01-08.yaml` file located at the root of this project.
5.  After importing, a new collection named "SmartMart Solutions" will be created, containing all requests ready to be used.

## API Endpoints

The API offers the following endpoints:

### Products (`/products`)

- `GET /products`: Returns a list of all products.
- `POST /products`: Creates a new product.
- `GET /products/export_csv`: Exports all products to a CSV file.
- `POST /products/import_csv`: Imports products from a CSV file.

### Categories (`/categories`)

- `GET /categories`: Returns a list of all categories.
- `POST /categories`: Creates a new category.
- `POST /categories/import_csv`: Imports categories from a CSV file.

### Sales (`/sales`)

- `GET /sales`: Returns a list of all sales.
- `POST /sales`: Records a new sale.
- `POST /sales/import_csv`: Imports sales data from a CSV file.

## ☁️ Deploy

The project is pre-configured for deployment on the **Vercel** platform. The `vercel.json` file defines the build route and redirection, pointing all requests to the `api/index.py` entrypoint. To deploy, simply connect your Git repository to Vercel.
