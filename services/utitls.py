import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product_and_prices(package):
    """
    Create or update Stripe product and prices for a package.
    """
    if not package:
        raise ValueError("Package instance is required.")

    monthly_price = (
        package.discount_price_per_month
        if package.discount_price_per_month and package.discount_price_per_month > 0
        else package.regular_price_per_month
    )
    yearly_price = (
        package.discount_price_per_year
        if package.discount_price_per_year and package.discount_price_per_year > 0
        else package.regular_price_per_year
    )

    if monthly_price is None or monthly_price <= 0:
        raise ValueError("A valid monthly price is required.")
    if yearly_price is None or yearly_price <= 0:
        raise ValueError("A valid yearly price is required.")
    if not package.title or package.title.strip() == "":
        raise ValueError("Package title is required.")

    try:
        # If product already exists, reuse it
        if package.stripe_product_id:
            product_id = package.stripe_product_id
        else:
            product = stripe.Product.create(name=package.title.strip())
            package.stripe_product_id = product.id
            package.save()
            product_id = product.id

        # Always create new prices (Stripe prices are immutable)
        monthly_price_obj = stripe.Price.create(
            unit_amount=int(monthly_price * 100),
            currency="usd",
            recurring={"interval": "month"},
            product=product_id,
        )

        yearly_price_obj = stripe.Price.create(
            unit_amount=int(yearly_price * 100),
            currency="usd",
            recurring={"interval": "year"},
            product=product_id,
        )

        # Update price IDs in package
        package.stripe_monthly_price_id = monthly_price_obj.id
        package.stripe_yearly_price_id = yearly_price_obj.id
        package.save()

    except stripe.error.StripeError as e:
        raise ValueError(f"Stripe API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")
