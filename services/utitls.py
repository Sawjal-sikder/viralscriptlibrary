import stripe 
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY



def create_stripe_product_and_prices(package):
    """
    Create Stripe product and prices for a package.
    
    Args:
        package: Package instance with title and price fields
    
    Raises:
        ValueError: If required price fields are missing or invalid
        stripe.error.StripeError: If Stripe API call fails
    """
    # Validate that package exists
    if not package:
        raise ValueError("Package instance is required.")
    
    # Validate required fields
    if not hasattr(package, 'discount_price_per_month') or not hasattr(package, 'discount_price_per_year'):
        raise ValueError("Package must have discount_price_per_month and discount_price_per_year fields.")
    
    # Validate prices before creating
    if package.discount_price_per_month is None or package.discount_price_per_year is None:
        raise ValueError("Both discount_price_per_month and discount_price_per_year must be provided.")
    
    # Validate price values are positive
    if package.discount_price_per_month <= 0 or package.discount_price_per_year <= 0:
        raise ValueError("Prices must be positive values.")
    
    # Validate title exists
    if not package.title or package.title.strip() == "":
        raise ValueError("Package title is required.")

    try:
        # Create Stripe Product
        product = stripe.Product.create(name=package.title.strip())

        # Create Monthly Price
        monthly_price = stripe.Price.create(
            unit_amount=int(package.discount_price_per_month * 100),
            currency="usd",
            recurring={"interval": "month"},
            product=product.id,
        )

        # Create Yearly Price
        yearly_price = stripe.Price.create(
            unit_amount=int(package.discount_price_per_year * 100),
            currency="usd",
            recurring={"interval": "year"},
            product=product.id,
        )

        # Save Stripe IDs
        package.stripe_product_id = product.id
        package.stripe_monthly_price_id = monthly_price.id
        package.stripe_yearly_price_id = yearly_price.id
        package.save()
        
    except stripe.error.StripeError as e:
        # Handle Stripe-specific errors
        raise ValueError(f"Stripe API error: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise ValueError(f"Unexpected error creating Stripe product: {str(e)}")
