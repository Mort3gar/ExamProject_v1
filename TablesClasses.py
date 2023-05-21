from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, BigInteger

class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Barcode = Column(BigInteger, nullable=False, unique=True)
    Code = Column(Integer, nullable=False)
    Name = Column(Text, nullable=False)
    PackageWeight = Column(Integer, nullable=False)
    Type = Column(Text, nullable=False)
    Price = Column(Integer, nullable=False)
    def __repr__(self) -> str:
        return f"{self.Barcode} {self.Code} {self.Name} {self.PackageWeight} {self.Type} {self.Price}"
class ProductsAvailability(Base):
    __tablename__ = "productsAvailability"
    id = Column(Integer, primary_key=True, autoincrement=True)
    productID = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship(Products)
    curAmount = Column(Integer, nullable=False)
    maxAmount = Column(Integer, nullable=False)
    DeadlineDate = Column(Text, nullable=False)
    def __repr__(self) -> str:
        return f"{self.productID} {self.product} {self.curAmount} {self.maxAmount} {self.DeadlineDate}"


class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    cardID = Column(Integer, nullable=False)
    product = Column(Integer, ForeignKey('products.id'))
    productName = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False)
    def __repr__(self)->str:
        return f"{self.name} {self.cardID} {self.product} {self.productName} {self.amount}"