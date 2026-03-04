# kebab_app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabella associativa per la relazione molti-a-molti tra Menu e Ingredienti
menu_ingredients = Table(
    "menu_ingredients",
    Base.metadata,
    Column("menu_id", ForeignKey("menus.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
)


class Menu(Base):
    """
    Rappresenta la categoria principale (es. Panino Kebab, Piadina).
    """

    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    base_price = Column(Float)

    variants = relationship("Variant", back_populates="menu")
    ingredients = relationship("Ingredient", secondary=menu_ingredients)


class Variant(Base):
    """
    Rappresenta la scelta di carne/stile (es. Pollo, Agnello, Veg).
    """

    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price_modifier = Column(Float, default=0.0)
    menu_id = Column(Integer, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="variants")


class Ingredient(Base):
    """
    Rappresenta i singoli ingredienti (es. Cipolla, Salsa Piccante).
    """

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_removable = Column(Boolean, default=True)


class Order(Base):
    """
    Rappresenta l'ordine complessivo del cliente.
    """

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    order_type = Column(String)  # "Tavolo" o "Asporto"
    status = Column(
        String, default="In preparazione"
    )  # In preparazione, Pronto, Consegnato
    total_price = Column(Float)
    details = Column(
        String
    )  # Per semplicità salviamo i dettagli in formato testuale/JSON stringificato
