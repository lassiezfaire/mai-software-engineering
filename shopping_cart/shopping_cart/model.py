from sqlmodel import Field, SQLModel, Session, select, delete

from .db import engine, session


class CartBase(SQLModel):
    user_id: int
    product_id: str
    product_amount: int = 1

    class Config:
        validate_assignment = True

    def add_to_cart(self):
        statement = select(Cart).where(Cart.user_id == self.user_id, Cart.product_id == self.product_id)
        row = session.exec(statement).first()

        if row is None:
            db_cart = Cart.model_validate(self)
            session.add(db_cart)
            session.commit()
            session.refresh(db_cart)
            return db_cart
        else:
            cart_data = self.model_dump(exclude_unset=True)
            cart_data['product_amount'] += row.product_amount
            row.sqlmodel_update(cart_data)
            session.add(row)
            session.commit()
            session.refresh(row)
            return row

    @classmethod
    def read(cls, id: int):
        cart = session.get(Cart, id)
        return cart

    @classmethod
    def read_by_user(cls, user_id: int):
        statement = select(Cart).where(Cart.user_id == user_id)
        carts = session.exec(statement).all()
        return carts

    @classmethod
    def read_by_product(cls, product_id: str):
        statement = select(Cart).where(Cart.product_id == product_id)
        carts = session.exec(statement).all()
        return carts

    @classmethod
    def read_all(cls, limit: int = 100, start_pos: int = 0):
        statement = select(Cart).limit(limit).offset(start_pos)
        carts = session.exec(statement).all()
        return carts

    @classmethod
    def delete(cls, id: int):
        cart = session.get(Cart, id)
        if not cart:
            return None
        session.delete(cart)
        session.commit()
        return {"ok": True}

    @classmethod
    def delete_by_user(cls, user_id: int):
        statement = delete(Cart).where(Cart.user_id == user_id)
        session.exec(statement)
        session.commit()
        return {"ok": True}

    @classmethod
    def delete_by_product(cls, product_id: str):
        statement = delete(Cart).where(Cart.product_id == product_id)
        session.exec(statement)
        session.commit()
        return {"ok": True}


class Cart(CartBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CartCreate(CartBase):
    pass


class CartRead(CartBase):
    id: int
