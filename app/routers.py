import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud, database, models, schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota de teste para confirmar se está online
@router.get("/health")
def health_check():
    return {"status": "online", "database": "connected"}


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


# Returns a CSV file for download of products
@router.get("/products/export_csv")
def export_products_csv(db: Session = Depends(database.get_db)):
    def generate():
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["id", "name", "description", "price", "category_id", "brand"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        products = db.query(models.Product).yield_per(100)

        for product in products:
            writer.writerow(
                [
                    product.id,
                    product.name,
                    product.description,
                    product.price,
                    product.category_id,
                    product.brand,
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    headers = {"Content-Disposition": 'attachment; filename="products_export.csv"'}
    return StreamingResponse(generate(), media_type="text/csv", headers=headers)


# Returns a CSV file for download of sales
@router.get("/sales/export_csv")
def export_sales_csv(db: Session = Depends(database.get_db)):
    def generate():
        output = io.StringIO()
        writer = csv.writer(output)

        # Cabeçalho do CSV de Vendas
        writer.writerow(
            ["id", "product_id", "quantity", "total_price", "sale_date", "customer_id"]
        )
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        # Usamos yield_per para não sobrecarregar a RAM se houver milhares de vendas
        sales = db.query(models.Sale).yield_per(100)

        for sale in sales:
            writer.writerow(
                [
                    sale.id,
                    sale.product_id,
                    sale.quantity,
                    sale.total_price,
                    sale.sale_date.strftime("%Y-%m-%d %H:%M:%S")
                    if sale.sale_date
                    else "",
                    sale.customer_id,
                ]
            )
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    headers = {"Content-Disposition": 'attachment; filename="sales_export.csv"'}
    return StreamingResponse(generate(), media_type="text/csv", headers=headers)


# Imports a CSV file for upload category data
@router.post("/products/import_csv")
async def import_products_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    products_to_create = []

    try:
        for row in reader:
            if not any(row.values()):
                continue

            new_product = models.Product(
                id=int(row["id"]),
                name=row["name"],
                description=row["description"],
                price=float(row["price"]),
                category_id=int(row["category_id"]),
                brand=row["brand"],
            )
            products_to_create.append(new_product)

        if products_to_create:
            db.bulk_save_objects(products_to_create)
            db.commit()

            db.execute(
                text("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products))")
            )
            db.commit()

        return {"message": f"Successfully imported {len(products_to_create)} products."}

    except (KeyError, ValueError) as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Erro de dados ou coluna ausente: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


# Imports a CSV file for upload category data
@router.post("/categories/import_csv")
async def import_categories_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    categories_to_create = []

    try:
        for row in reader:
            if not any(row.values()):
                continue

            new_category = models.Category(id=int(row["id"]), name=row["name"])
            categories_to_create.append(new_category)

        if categories_to_create:
            db.bulk_save_objects(categories_to_create)
            db.commit()

            db.execute(
                text(
                    "SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories))"
                )
            )
            db.commit()

        return {
            "message": f"Successfully imported {len(categories_to_create)} categories."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


# Imports a CSV file for upload sales data
@router.post("/sales/import_csv")
async def import_sales_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um CSV")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(stream)

    sales_to_create = []

    try:
        for row in reader:
            if not any(row.values()):
                continue

            # Conversão Manual de Tipos
            p_id = int(row["product_id"])
            qty = int(row["quantity"])
            price = float(row["total_price"])

            # Conversão de Data
            date_obj = datetime.strptime(row["date"], "%Y-%m-%d")

            # Criamos o objeto do MODEL diretamente
            new_sale = models.Sale(
                product_id=p_id, date=date_obj, quantity=qty, total_price=price
            )
            sales_to_create.append(new_sale)

        # SALVAMENTO EM LOTE
        if sales_to_create:
            db.bulk_save_objects(sales_to_create)
            db.commit()

            db.execute(
                text("SELECT setval('sales_id_seq', (SELECT MAX(id) FROM sales))")
            )
            db.commit()
        else:
            return {"message": "CSV vazio ou sem dados válidos."}

    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Erro no formato dos dados (Data ou Números): {str(e)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Erro ao processar CSV de vendas: {str(e)}"
        )
    finally:
        db.close()

    return {"message": f"Successfully imported {len(sales_to_create)} sales."}
