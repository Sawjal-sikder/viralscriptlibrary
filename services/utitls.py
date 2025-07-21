import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product_and_prices(package):
    """
    Create Stripe product and prices for a package.

    Args:
        package: Package instance with title and price fields

    Raises:
        ValueError: If required fields are missing or invalid
        stripe.error.StripeError: If Stripe API call fails
    """
    if not package:
        raise ValueError("Package instance is required.")

    # Use discount price if available and greater than 0, else fallback to regular price
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

    # Validate that fallback prices exist and are greater than 0
    if monthly_price is None or monthly_price <= 0:
        raise ValueError("A valid monthly price is required (discount or regular).")
    if yearly_price is None or yearly_price <= 0:
        raise ValueError("A valid yearly price is required (discount or regular).")

    if not package.title or package.title.strip() == "":
        raise ValueError("Package title is required.")

    try:
        # Create Stripe Product
        product = stripe.Product.create(name=package.title.strip())

        # Create Monthly Price
        monthly_price_obj = stripe.Price.create(
            unit_amount=int(monthly_price * 100),
            currency="usd",
            recurring={"interval": "month"},
            product=product.id,
        )

        # Create Yearly Price
        yearly_price_obj = stripe.Price.create(
            unit_amount=int(yearly_price * 100),
            currency="usd",
            recurring={"interval": "year"},
            product=product.id,
        )

        # Save Stripe IDs
        package.stripe_product_id = product.id
        package.stripe_monthly_price_id = monthly_price_obj.id
        package.stripe_yearly_price_id = yearly_price_obj.id
        package.save()

    except stripe.error.StripeError as e:
        raise ValueError(f"Stripe API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error creating Stripe product: {str(e)}")
