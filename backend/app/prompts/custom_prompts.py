# Define the prompt template
title_prompt = """
    Given the following user query, generate a concise and descriptive title 
    that accurately captures the main topic or intent of the query. The title should be 
    upto 5 words long and summarize the essence of the user's question or statement. 
    Keep it short, clear, and engaging.
    
    User Query: '{question}'

    Instructions: Please reply in plain text only. Don't use markdown or other formats for this response.
    """
