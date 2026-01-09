import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, database, schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET all products
@router.get("/products", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


# POST a new product
@router.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


# GET all categories
@router.get("/categories", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# POST a new category
@router.post("/categories", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


# GET all sales
@router.get("/sales", response_model=list[schemas.Sale])
def list_sales(db: Session = Depends(get_db)):
    return crud.get_sales(db)


# POST a new sale
@router.post("/sales", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)


# Returns a CSV file for download
@router.get("/products/export_csv")
def export_products_csv(db: Session = Depends(get_db)):
    products = crud.get_products(db)

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(["id", "name", "category_id", "price"])

    # Rows
    for p in products:
        writer.writerow([p.id, p.name, p.category_id, p.price])

    # Go back to the beginning
    output.seek(0)

    # Return as CSV file for download
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"},
    )


# Imports a CSV file for upload products
@router.post("/products/import_csv")
async def import_products_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    # Check if filename exists and validate extension
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Validate file extension
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Read the file content into memory
    contents = await file.read()

    # Decode bytes to string and initialize the CSV reader
    # DictReader automatically maps the first row as dictionary keys
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    products_created = 0

    # Iterate over each row and save to database
    try:
        for row in reader:
            if not any(row.values()):
                continue

            # Map CSV columns to the Pydantic Schema
            product_data = schemas.ProductCreate(
                name=row["name"],
                category_id=int(row["category_id"]),
                price=float(row["price"]),
            )

            crud.create_product(db, product_data)
            products_created += 1

    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Missing required column in CSV: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

    return {"message": f"Successfully imported {products_created} products."}


# Imports a CSV file for upload categories
@router.post("/categories/import_csv")
async def import_categories_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    # 1. Type Guard for Pyright/Zed
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    categories_created = 0

    try:
        for row in reader:
            if not any(row.values()):
                continue

            # Map columns: name
            category_data = schemas.CategoryCreate(name=row["name"])
            crud.create_category(db, category_data)
            categories_created += 1

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    return {"message": f"Successfully imported {categories_created} categories."}


# Imports a CSV file for upload sales data
@router.post("/sales/import_csv")
async def import_sales_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    sales_created = 0

    try:
        for row in reader:
            if not any(row.values()):
                continue

            # Aligning with your SaleBase Schema:
            # product_id (int), date (str), quantity (int), total_price (float)
            sale_data = schemas.SaleCreate(
                product_id=int(row["product_id"]),
                date=row["date"],  # Your schema expects a string here
                quantity=int(row["quantity"]),
                total_price=float(
                    row["total_price"]
                ),  # You included total_price in schema
            )

            crud.create_sale(db, sale_data)
            sales_created += 1

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing sales CSV: {str(e)}"
        )

    return {"message": f"Successfully imported {sales_created} sales."}
