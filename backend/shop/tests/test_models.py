from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from ..models import (
    Product,
    ProductCategory,
    ProductImage,
    ProductProperty,
    Cart,
    Order,
    Payment,
    Item
)

# getting user model 
User = get_user_model()

class ShopModelTests(TestCase):
    def setUp(self):
        # part 1 
        self.phone_category = ProductCategory.objects.create(title="phone", slug="phone", description="phone category")
        self.property1 = ProductProperty.objects.create(title="price", value="as god as price", place=1)
        self.phone = Product.objects.create(title="phone", slug="phone", description="phone product", category=self.phone_category, price=2500000, quantity=1, discountable=False)
        self.phone.properties.add(self.property1)
        self.phone.save()

        # part 2

        self.user = User.objects.create_user(email="test@example.com", username="test", password="test", phone_number="09125689898")
        self.item = Item.objects.create(item=self.phone, quantity=1)
        self.secondItem = Item.objects.create(item=self.phone, quantity=2) 

    def test_create_product(self):
        self.assertEqual(self.phone.title, "phone")
        self.assertEqual(self.phone.slug, "phone")
        self.assertEqual(self.phone.description, "phone product")
        self.assertEqual(self.phone.category, self.phone_category)
        self.assertEqual(self.property1.value, "as god as price")
        self.assertEqual(self.phone_category.title, "phone")

    def test_create_product_information(self):
        image = ProductImage.objects.create(title="First image", product=self.phone, image="ProductImages/2021/5/22")

        # testing part

        self.assertEqual(image.title, "First image")
        self.assertEqual(image.product, self.phone)
        self.assertEqual(image.image, "ProductImages/2021/5/22") 

    def test_create_same_slug(self):
        phone_category1 = ProductCategory(title="phone", slug="phone", description="phone category")
        phone_category2 = ProductCategory(title="phone", slug="phone", description="phone category")

        # testing part

        with self.assertRaises(IntegrityError):
            phone_category1.save()
            phone_category2.save()

    def test_create_cart(self):
        cart = Cart.objects.create(user=self.user, is_ordered=False)
        cart.items.add(self.item)
        cart.items.add(self.secondItem)
        cart.save()

        # testing part

        self.assertEqual([cart.items.get(pk=self.item.pk), cart.items.get(pk=self.secondItem.pk)], [self.item, self.secondItem])
        self.assertEqual(cart.user, self.user)   
        self.assertFalse(cart.is_ordered)

    def test_create_order(self):
        order1 = Order.objects.create(user=self.user, is_purchased=False)
        order1.items.add(self.item)
        order1.save()

        # testing part

        self.assertEqual(order1.user, self.user)
        self.assertEqual(order1.items.get(pk=self.item.pk), self.item)
        self.assertFalse(order1.is_purchased) 

    def test_create_payment(self):
        payment = Payment.objects.create(user=self.user, total=2500000)
        payment.items.add(self.item)
        payment.save()

        # testing part

        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.total, 2500000) 
        self.assertEqual(payment.items.get(pk=self.item.pk), self.item)                                         