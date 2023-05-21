from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
import config
from TablesClasses import Base, Products, ProductsAvailability, Customers
from tabulate import tabulate

from sqlalchemy import create_engine, ScalarResult
import re

engine = create_engine(f"mysql+pymysql://{config.user}:{config.password}@localhost/{config.dbName}", echo=False)

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
from sqlalchemy import select



def barcodeInp():
    while True:
        barcode = input("Enter barcode (13 digits): ")
        if len(barcode) == 13 and barcode.isdigit():
            return int(barcode)
        else:
            print("Error")


def typeIntp():
    types_ = ["piece", "weight"]
    while True:
        type_ = input("""1. Piece goods
2. Goods by weight
->""")
        if type_ in ["1", "2"]:
            return types_[int(type_) - 1]
        else:
            print("Must be 1 or 2")


def digInp(outStr: str):
    while True:
        code = input(outStr)
        if code.isdigit():
            return int(code)
        else:
            print("Must be digits")


def dateInp():
    re_ = "(?:[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(?:.|-)(?:[1-9]|0[1-9]|1[0-2])(?:.|-|)(?:20[0-9][0-9]|[0-9][0-9])"
    while True:
        date = input("Enter deadline date (DD.MM.YYYY): ")
        if re.fullmatch(re_, date):
            return date
        else:
            print("Error")


def addProduct(barcode: int, code: int, name: str, packageWeight: int, type_: str, price: int):
    with Session(engine) as session:
        temp = Products(Barcode=barcode,
                        Code=code,
                        Name=name,
                        PackageWeight=packageWeight,
                        Type=type_,
                        Price=price,
                        )
        session.add(temp)
        session.commit()


def addProductsAvailability(product_: Products, maxAmount_: int, deadlineDate_: str):
    with Session(engine) as session:
        temp = ProductsAvailability(productID = product_.id,
                                    product = product_,
                                    curAmount = maxAmount_,
                                    maxAmount = maxAmount_,
                                    DeadlineDate = deadlineDate_)
        session.add(temp)
        session.commit()


def selectAllProductsAvailability():
    with Session(engine) as session:
        req = select(ProductsAvailability)
        t = []
        for item in session.scalars(req):
            t.append(item)
        return t


def selectProduct(productID:int):
    with Session(engine) as session:
        return session.scalars(select(Products).where(Products.id == productID)).one()


def productsAvailabilityMenu():
    temp = selectAllProductsAvailability()
    if len(temp) != 0:
        n = 3
        page = 1
        pages = int(len(temp)/n)
        if len(temp)%n != 0:
            pages += 1

        while True:
            if len(temp) > n:
                t_list = []
                for i, item in enumerate(temp[n * (page - 1):n * page]):
                    t_list.append([i+1]+str(selectProduct(item.productID)).split()+[item.curAmount, item.maxAmount, item.DeadlineDate])
                    # print(i+1, selectProduct(item.productID), item.curAmount, item.maxAmount, item.DeadlineDate)
                print(tabulate(t_list,
                               headers=["№", "Barcode", "Code", "Name", "Package Weight", "Type", "Price", "CurAmount", "MaxAmount", "Deadline Date"]))
                if page == 1:
                    print("""1. Next page
2. Choose product""")
                elif page != pages:
                    print("""1. Next page
2. Prev page
3. Choose product""")
                else:
                    print("""1. Prev page
2. Choose product""")
                choice = input("-> ")
                if page == 1:
                    if choice == "1":
                        page += 1
                    elif choice == "2":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
                elif page != pages:
                    if choice == "1":
                        page += 1
                    elif choice == "2":
                        page -= 1
                    elif choice == "3":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
                else:
                    if choice == "1":
                        page -= 1
                    elif choice == "2":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
            else:
                for i, item in enumerate(temp):
                    print(i + 1, selectProduct(item.productID), item)
                print("Choose product")
                return productChoose(temp)
    else:
        raise ValueError("There are no items in db")


def selectAllProducts():
    with Session(engine) as session:
        req = select(Products)
        t = []
        for item in session.scalars(req):
            t.append(item)
        return t


def productChoose(productsList: list):
    while True:
        choice = digInp("->")
        if choice <= len(productsList):
            return productsList[choice - 1]
        else:
            print("Error")


def productsMenu():
    temp = selectAllProducts()
    if len(temp) != 0:
        n = 3
        page = 1
        pages = int(len(temp) / n)
        if len(temp) % n != 0:
            pages += 1
        while True:
            if len(temp) > n:
                t_list = []
                for i, item in enumerate(temp[n * (page - 1):n * page]):
                    t_list.append([i+1]+str(item).split())
                    # print(i + 1, item)
                print(tabulate(t_list,
                               headers=["№", "Barcode", "Code", "Name", "Package Weight", "Type", "Price"]))
                if page == 1:
                    print("""1. Next page
2. Choose product""")
                elif page != pages:
                    print("""1. Next page
2. Prev page
3. Choose product""")
                else:
                    print("""1. Prev page
2. Choose product""")
                choice = input("-> ")
                if page == 1:
                    if choice == "1":
                        page += 1
                    elif choice == "2":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
                elif page != pages:
                    if choice == "1":
                        page += 1
                    elif choice == "2":
                        page -= 1
                    elif choice == "3":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
                else:
                    if choice == "1":
                        page -= 1
                    elif choice == "2":
                        return productChoose(temp[n * (page - 1):n * page])
                    else:
                        print("Error")
            else:
                for i, item in enumerate(temp):
                    print(i + 1, item)
                print("Choose product")
                return productChoose(temp)

    else:
        raise ValueError("There are no items in db")


def productSellAmount(productAvail: ProductsAvailability):
    while True:
        code = input("Enter the quantity of the product sold: ")
        if code.isdigit() and int(code) <= productAvail.curAmount:
            return int(code)
        else:
            print("Must be digits")


def addCustomer(name_:str, cardID_:int, product_:ProductsAvailability, amount_:int):
    with Session(engine) as session:
        temp = Customers(name=name_,
                         cardID=cardID_,
                         product=selectProduct(product_.productID).id,
                         productName=selectProduct(product_.productID).Name,
                         amount=amount_)
        session.add(temp)
        session.commit()


def updateProductsAvailability(sellAmount:int, product_):
    with Session(engine) as session:
        temp = session.scalars(select(ProductsAvailability).where(ProductsAvailability.id==product_.id)).one()
        if temp.curAmount - sellAmount > 0:
            temp.curAmount -= sellAmount
        else:
            session.delete(temp)
        session.commit()


def showTable(tableName:str):
    with Session(engine) as session:
        if tableName == "products":
            t = session.scalars(select(Products))
            t_list = []
            for item in t:
                t_list.append(str(item).split())
            print(tabulate(t_list,
                           headers=["Barcode", "Code", "Name", "PackageWeight", "Type", "Price"],
                           tablefmt='orgtbl'))
        elif tableName == "productsAvailability":
            t = session.scalars(select(ProductsAvailability))
            t_list = []
            for item in t:
                t_list.append(str(item).split())
            print(tabulate(t_list,
                           headers=["productID", "Barcode", "Code", "Name", "PackageWeight", "Type", "Price", "curAmount", "maxAmount", "DeadlineDate"],
                           tablefmt='orgtbl'))
        elif tableName == "customers":
            t = session.scalars(select(Customers))
            t_list = []
            for item in t:
                t_list.append(str(item).split())
            print(tabulate(t_list,
                           headers=["name", "cardID", "productID", "productName", "Amount"],
                           tablefmt='orgtbl'))



if __name__ == "__main__":
    userState = "main"
    state = True

    while state:
        if userState == "main":
            print("""
1. Add new product
2. New supply
3. Sell product
4. Show tables
5. Exit
""")
            choice = input("-> ")
            if choice == "1":
                userState = "newProduct"
            elif choice == "2":
                userState = "newSupply"
            elif choice == "3":
                userState = "sell"
            elif choice == "4":
                userState = "tables"
            elif choice == "5":
                state = False
            else:
                print("Error")
        elif userState == "newProduct":
            # addProduct(1234567890123, 34, "Spaghetti", 100, "piece", 200)
            # addProduct(2134567890123, 45, "Rise", 150, "piece", 100)
            # addProduct(3124567890123, 64, "Buckwheat", 200, "piece", 50)
            # addProduct(4123567890123, 91, "Pancakes", 300, "piece", 300)
            barcode = barcodeInp()
            code = digInp("Enter product group code (digits): ")
            name = input("Enter product name: ")
            type_ = typeIntp()
            if type_ == "piece":
                packageWeight = digInp("Enter package weight: ")
            else:
                packageWeight = 0
            price = digInp("Enter product price: ")
            addProduct(barcode, code, name, packageWeight, type_, price)
            userState = "main"
            showTable("products")

        elif userState == "newSupply":
            product = None
            try:
                product = productsMenu()
            except ValueError as e:
                print(e)

            if product is not None:
                maxAmount = digInp("Enter the amount of the received product: ")
                deadlineDate = dateInp()
                addProductsAvailability(product, maxAmount, deadlineDate)

            userState = "main"
            showTable("productsAvailability")
        elif userState == "sell":
            product = None
            try:
                product = productsAvailabilityMenu()
            except ValueError as e:
                print(e)

            if product is not None:
                name = input("Enter customer`s name: ")
                cardID = digInp("Enter customer`s card ID (4 digits): ")
                amount = productSellAmount(product)
                addCustomer(name, cardID, product, amount)
                updateProductsAvailability(amount, product)
            userState = "main"
            showTable("customers")
        elif "tables":
            print("""1. Products
2. Products availability
3. Customers""")
            choice = input("->")
            if choice == "1":
                showTable("products")
            elif choice == "2":
                showTable("productsAvailability")
            elif choice == "3":
                showTable("customers")
            userState = "main"