import os

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_price(payment):
    stripe_product = stripe.Product.create(name=payment.paid_course.name)

    stripe_price = stripe.Price.create(
        currency="usd",
        unit_amount=payment.amount,
        product_data={"name": stripe_product['name']},
    )
    return stripe_price['id']


def create_stripe_session(stripe_price_id):
    session = stripe.checkout.Session.create(
        success_url=os.getenv("MAIN_URL"),
        line_items=[{"price": stripe_price_id, "quantity": 1}],
        mode="payment",
    )

    return session['id'], session['url']
