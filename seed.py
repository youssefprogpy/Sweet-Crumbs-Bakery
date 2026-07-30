# Run only against a fresh/empty database. If you get UNIQUE constraint errors, delete instance/sweetcrumbs.db and re-run migrations first.

from app.extentions import db
from app import create_app
from app.models import User, Product, Category

# seeding real data to initiate the db
app = create_app()
# needs with here so it acts like a server in order to insert the data in
with app.app_context():
    # Category seeds
    category1 = Category(name="Moroccan Pastries", slug="moroccan-pasteries")
    category2 = Category(name="French Pastries", slug="french-pasteries")
    category3 = Category(name="Breads", slug="breads")
    category4 = Category(name="Cakes", slug="cakes")
    category5 = Category(name="Cookies & Biscuits", slug="cookies-biscuits")
    category6 = Category(name="Beverages", slug="beverages")
    # Category session
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)
    db.session.add(category5)
    db.session.add(category6)
    # Product seeds
    product1 = Product(
        name="Chebakia",
        description="Sesame and honey spiral pastry, fried and coated in honey and sesame seeds",
        price=25.00,
        category=category1,
    )
    product2 = Product(
        name="Ghriba",
        description="Traditional Moroccan almond and sesame cookies with a crackled top",
        price=20.00,
        category=category1,
    )
    product3 = Product(
        name="Kaab el Ghazal(Gazelle Hornes)",
        description="Crescent-shaped pastry filled with almond paste and orange blossom water",
        price=30.00,
        category=category1,
    )
    product4 = Product(
        name="Sello",
        description="Roasted flour, almonds, and sesame sweet, no baking required",
        price=35.00,
        category=category1,
    )

    product5 = Product(
        name="Croissant",
        description="Buttery, flaky, laminated pastry, baked fresh every morning",
        price=12.00,
        category=category2,
    )
    product6 = Product(
        name="Pain au Chocolat",
        description="Classic croissant dough wrapped around two batons of dark chocolate",
        price=14.00,
        category=category2,
    )
    product7 = Product(
        name="Éclair",
        description="Choux pastry filled with vanilla cream, topped with chocolate glaze",
        price=18.00,
        category=category2,
    )
    product8 = Product(
        name="Mille-feuille",
        description="Layers of puff pastry and pastry cream, finished with a light glaze",
        price=22.00,
        category=category2,
    )

    product9 = Product(
        name="Khobz",
        description="Traditional round Moroccan bread, baked daily",
        price=4.00,
        category=category3,
    )
    product10 = Product(
        name="Batbout",
        description="Soft Moroccan flatbread, perfect for sandwiches",
        price=5.00,
        category=category3,
    )
    product11 = Product(
        name="Baguette",
        description="Classic French baguette, crisp crust and soft interior",
        price=6.00,
        category=category3,
    )
    product12 = Product(
        name="Sourdough Loaf",
        description="Naturally leavened bread with a tangy flavor and chewy crust",
        price=28.00,
        category=category3,
    )

    product13 = Product(
        name="Chocolate Fondant Cake",
        description="Rich dark chocolate cake with a molten center",
        price=120.00,
        category=category4,
    )
    product14 = Product(
        name="Orange Blossom Cake",
        description="Light sponge cake infused with orange blossom water and almonds",
        price=95.00,
        category=category4,
    )
    product15 = Product(
        name="Red Velvet Cake",
        description="Classic red velvet layers with cream cheese frosting",
        price=130.00,
        category=category4,
    )
    product16 = Product(
        name="Cheesecake",
        description="Creamy baked cheesecake with a buttery biscuit base",
        price=110.00,
        category=category4,
    )

    product17 = Product(
        name="Cornes de Gazelle (mini)",
        description="Bite-sized almond-filled cookies dusted with powdered sugar",
        price=15.00,
        category=category5,
    )
    product18 = Product(
        name="Chocolate Chip Cookies",
        description="Classic soft-baked cookies loaded with chocolate chips",
        price=10.00,
        category=category5,
    )
    product19 = Product(
        name="Amlou Stuffed Cookies",
        description="Cookies filled with almond, argan oil, and honey spread",
        price=18.00,
        category=category5,
    )

    product20 = Product(
        name="Moroccan Mint Tea",
        description="Fresh mint tea served traditionally, sweet and aromatic",
        price=10.00,
        category=category6,
    )
    product21 = Product(
        name="Espresso",
        description="Single shot of freshly ground espresso",
        price=8.00,
        category=category6,
    )
    product22 = Product(
        name="Almond Milk",
        description="Cold, freshly made almond milk, lightly sweetened",
        price=12.00,
        category=category6,
    )
    # Product session
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.add(product7)
    db.session.add(product8)
    db.session.add(product9)
    db.session.add(product10)
    db.session.add(product11)
    db.session.add(product12)
    db.session.add(product13)
    db.session.add(product14)
    db.session.add(product15)
    db.session.add(product16)
    db.session.add(product17)
    db.session.add(product18)
    db.session.add(product19)
    db.session.add(product20)
    db.session.add(product21)
    db.session.add(product22)

    # User seeds
    admin = User(email="admin@sweetcrumbs.com", name="Youssef", is_admin=True)
    admin.password_hash = User.hashing_pass("testpass123")
    user = User(email="sara.amrani@gmail.com", name="Sara Amrani")
    user.password_hash = User.hashing_pass("testpass123")
    # User session
    db.session.add(admin)
    db.session.add(user)

    # commiting to db
    db.session.commit()
