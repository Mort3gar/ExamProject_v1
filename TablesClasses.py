from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, BigInteger, DateTime


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(BigInteger, nullable=False, unique=True)
    code = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    packageWeight = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    # def __str__(self) -> str:
    #     return f"{self.barcode} {self.code} {self.name} {self.packageWeight} {self.price}"

    def __repr__(self) -> str:
        return f"{self.barcode} {self.code} {self.name} {self.packageWeight} {self.price}"


class ProductAvailability(Base):
    __tablename__ = "productsAvailability"
    id = Column(Integer, primary_key=True, autoincrement=True)
    productID = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship(Product)
    curAmount = Column(Integer, nullable=False)
    deadlineDate = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"{self.productID} {self.product} {self.curAmount} {self.deadlineDate}"


class WeightProduct(Base):
    __tablename__ = "weightProducts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, ForeignKey('products.id'))
    product = relationship(Product)


class PieceProduct(Base):
    __tablename__ = "pieceProducts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, ForeignKey('products.id'))
    product = relationship(Product)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    cardID = Column(Integer, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"{self.name} {self.cardID}"


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(Text, nullable=False)


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, ForeignKey("customers.id"))
    customer = relationship(Customer)
    productId = Column(Integer, ForeignKey("products.id"))
    product = relationship(Product)
    amount = Column(Integer, nullable=False)
    shopId = Column(Integer, ForeignKey("shops.id"))
    shop = relationship(Shop)
