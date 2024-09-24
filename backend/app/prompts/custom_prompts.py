# Define the prompt template
company_name_crafter_template = """
    Given the product description and target audience below, generate three creative 
    and original company names. The names should reflect the product's unique value, 
    resonate with the target audience, and be easy to remember and pronounce. Avoid 
    common or generic terms, and focus on delivering distinctive and impactful names.


    INSTRUCTIONS: Don't add text like ```json
    Product Description: {product_name}
    Target Audience: {target_audience}
    Please return the suggestions in the following JSON format only.
    {{
    "company_name_suggestions": [
        "Name 1",
        "Name 2",
        "Name 3"
    ]
    }}
    """
