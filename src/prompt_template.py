# openai_prompt_template = """Please respond in detail to the question (within the [##Question##] and [/##Question##] blocks), considering only the context (within the [##Context##] and [/##Context##] blocks). 

# If the context does not allow for answering the question, please respond with the following text only: 
# "Regrettably, I was unable to locate information pertinent to your inquiry. I kindly recommend reaching out to our dedicated customer support team at 333-333-333-333 or via email at customer-support@fabian.com for further assistance". 

# [##Question##]{question}[/##Question##]

# [##Context##]{context}[/##Context##]"""
from attr import dataclass


@dataclass
class Templates:
        
    openai_prompt_template="""For accurate assistance, please address your inquiry within the designated [##Question##] and [/##Question##] blocks, while providing relevant details in the [##Context##] and [/##Context##] blocks.

    If the context is insufficient to generate a response, please consider using the following response template:
    "Unfortunately, I'm unable to find relevant information based on the provided context."

    [##Question##]{question}[/##Question##]

    [##Context##]{context}[/##Context##]"""


    summarize_prompt = """Provide a summary of the context as a response to the user's question.
    If the context is insufficient for a response, use this template: "Unable to find relevant information based on the provided context. 
    Return the summary without prephase "The provided context is a"
    Question:{question}
    Context:{context}
    """
