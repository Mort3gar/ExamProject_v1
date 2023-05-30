from sqlalchemy import create_engine
from datetime import datetime
import config
from TablesClasses import Base, Product, ProductAvailability, WeightProduct, PieceProduct, Customer, Shop, Sale
from tabulate import tabulate

engine = create_engine(f"mysql+pymysql://{config.user}:{config.password}@localhost/{config.dbName}", echo=False)

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
from sqlalchemy import select


#  DeadlineDate=date(2020, 9, 30)
def updateProductAvailability(sellAmount: int, id):
    with Session(engine) as session:
        temp = session.scalars(select(ProductAvailability).where(ProductAvailability.id == id)).one()
        if temp.curAmount - sellAmount > 0:
            temp.curAmount -= sellAmount
        else:
            session.delete(temp)
        session.commit()


with Session(engine) as session:
    product1 = Product(barcode=1234567890123,
                       code=34,
                       name="Spaghetti",
                       packageWeight=100,
                       price=200
                       )
    piece1 = PieceProduct(productId=product1.id, product=product1)

    product2 = Product(barcode=2134567890123,
                       code=45,
                       name="Rise",
                       packageWeight=150,
                       price=100
                       )
    piece2 = PieceProduct(productId=product2.id, product=product2)

    product3 = Product(barcode=3124567890123,
                       code=64,
                       name="Buckwheat",
                       packageWeight=0,
                       price=30
                       )
    weight1 = WeightProduct(productId=product3.id, product=product3)

    product4 = Product(barcode=4123567890123,
                       code=91,
                       name="Pancakes",
                       packageWeight=300,
                       price=300
                       )
    piece3 = PieceProduct(productId=product4.id, product=product4)

    shop1 = Shop(address="Самара, проспект Кирова, 202")
    shop2 = Shop(address="Самара, ул. Луначарского, 60")

    prodAval1 = ProductAvailability(productID=product1.id,
                                    product=product1,
                                    curAmount=200,
                                    deadlineDate=datetime(2023, 6, 18))
    prodAval2 = ProductAvailability(productID=product2.id,
                                    product=product2,
                                    curAmount=150,
                                    deadlineDate=datetime(2023, 7, 13)
                                    )
    prodAval3 = ProductAvailability(productID=product3.id,
                                    product=product3,
                                    curAmount=300,
                                    deadlineDate=datetime(2023, 6, 5)
                                    )
    prodAval4 = ProductAvailability(productID=product4.id,
                                    product=product4,
                                    curAmount=50,
                                    deadlineDate=datetime(2023, 10, 7)
                                    )
    prodAval5 = ProductAvailability(productID=product1.id,
                                    product=product1,
                                    curAmount=15,
                                    deadlineDate=datetime(2023, 5, 31)
                                    )

    customer1 = Customer(name="Иван Иванович", cardID=1234)
    customer2 = Customer(name="Вася Пупкин", cardID=2154)
    customer3 = Customer(name="Олег Петрович", cardID=9713)

    session.add_all([product1, piece1, product2, piece2, product3, weight1, product4, piece3,
                     shop1, shop2, prodAval1, prodAval2, prodAval3, prodAval4, prodAval5,
                     customer1, customer2, customer3])
    session.commit()

    print("Товары")
    print(tabulate(
        session.execute(select(Product.id,
                               Product.barcode,
                               Product.code,
                               Product.name,
                               Product.packageWeight,
                               Product.price)).all(),
        headers=["№", "Barcode", "Code", "Name", "Package Weight", "Price"]
    ))
    print("Товары на складах")
    print(tabulate(
        session.execute(select(ProductAvailability.id,
                               ProductAvailability.productID,
                               ProductAvailability.curAmount,
                               ProductAvailability.deadlineDate
                               ).join(Product)).all(),
        headers=["№", "ProductId", "CurAmount", "DeadlineDate"]
    ))

    print("Магазины")
    print(tabulate(
        session.execute(select(Shop.id, Shop.address)).all(),
        headers=["№", "Address"]
    ))

    print("Покупатели")
    print(tabulate(
        session.execute(select(Customer.id, Customer.name, Customer.cardID)).all(),
        headers=["№", "Name", "CardID"]
    ))

    sale1 = Sale(customerId=customer1.id, customer=customer1,
                 productId=product3.id, product=product3,
                 amount=10, shopId=shop1.id, shop=shop1)
    session.add(sale1)
    session.commit()
    print("Продажи")
    print(tabulate(
        session.execute(select(Sale.id, Sale.customerId, Sale.productId,
                               Sale.amount, Sale.shopId).
                        join(Customer).join(Product).join(Shop)).all(),
        headers=["№", "CustomerId", "ProductId", "Amount", "ShopId"]))

    updateProductAvailability(10, 1)
with Session(engine) as session:
    print("Товары на складах")
    print(tabulate(
        session.execute(select(ProductAvailability.id,
                               ProductAvailability.productID,
                               ProductAvailability.curAmount,
                               ProductAvailability.deadlineDate
                               ).join(Product)).all(),
        headers=["№", "ProductId", "CurAmount", "DeadlineDate"]
    ))
