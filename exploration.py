import pydantic_ai
import os
import asyncio
import anthropic
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from dotenv import load_dotenv
from transformers import pipeline

from schema import AssistantResponse

'''


# 1. Your Key
load_dotenv()
MY_KEY = os.getenv("ANTHROPIC_API_KEY")
provider = AnthropicProvider(api_key=MY_KEY)
model = AnthropicModel('claude-sonnet-4-6', provider=provider)

# 2. Update result_type -> output_type
# In 2026, PydanticAI uses output_type for the generic response schema.
agent = Agent(model
              , model_settings={"temperature": 0.8}
              , output_type=AssistantResponse)

async def main():
    try:
        result = await agent.run("Hello, this is a test run?")
        print(f"Success! Response: {result.output.answer}")
        print(f"Confidence: {result.output.confidence}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())


print('-'*50)


client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

completion = client.messages.create(
    model="claude-sonnet-4-6",
    system="You are an physicist.",
    max_tokens=1024,
    temperature=0.8,
    messages=[
        {
            "role": "user",
            "content": [
               {
                  "type": "text",
                  "text": "An electron walks into a bar."
               }
            ]
        }
    ]
)

print(completion.content[0].text)




print('-'*50)

'''




banned_phrases = [
    # --- Medical & Disease Claims ---
    "cancer", "cure", "treat", "treatment", "prevent", "prevention", "heal", "remedy", 
    "remedies", "diagnose", "alzheimer's", "anxiety", "diabetes", "depression", 
    "hiv", "aids", "flu", "coronavirus", "covid-19", "lupus", "herpes", "parkinson", 
    "stroke", "tumor", "weight loss", "detox", "detoxify", "detoxification", 

    # --- Pesticidal & Microbial Claims ---
    "antibacterial", "anti-bacterial", "antifungal", "anti-fungal", "antimicrobial", 
    "anti-microbial", "pesticide", "pesticide-free", "sanitize", "sanitizer", 
    "disinfect", "disinfectant", "kill viruses", "germs", "non-toxic", "harmless",

    # --- Promotional & Pricing Language ---
    "free", "best price", "cheapest", "affordable", "on sale", "special offer", 
    "special promo", "discounted price", "wholesale price", "free shipping", 
    "money back guarantee", "satisfaction guaranteed", "100% quality", 
    "risk-free", "buy with confidence", "limited time offer", "bonus",

    # --- Subjective Superlatives ---
    "best", "best seller", "top rated", "award winning", "number one", "#1", 
    "amazing", "incredible", "must-have", "hot item", "hottest", "proven", 
    "validated", "top notch", "high quality", "excellent",

    # --- Logistics & Fulfillment ---
    "ready to ship", "within hours", "ups", "fedex", "amazon shipping", 
    "delivery guaranteed", "add to cart",

    # --- Prohibited Ingredients & Substances ---
    "cbd", "cannabidiol", "thc", "hemp oil", "marijuana", "ayahuasca", 
    "ephedrine", "psilocybin", "human parts", "coca leaves",

    # --- Environmental Claims (FTC regulated) ---
    "eco-friendly", "environmentally friendly", "green", "biodegradable", 
    "compostable", "degradable", "recyclable", "carbon-reducing", 'perfect', "ideal", "optimized", "sustainable", "renewable", "organic", "natural"
]
banned_phrases = [phrase.lower() for phrase in banned_phrases]

# Note: This is a representative sample. Amazon's automated system
# flags variations and synonyms of these terms constantly. Sellers should avoid using any language that could be interpreted as making unverified claims about health benefits, safety, or performance. Always refer to Amazon's official guidelines for the most up-to-date information on restricted keywords.


desired_phrases = [
    # --- Benefit-Driven Clarity (The "3-Second Test") ---
    "save cabinet space", "designed for busy lifestyles", "whisper-quiet operation",
    "fits in standard cup holders", "dishwasher safe for easy cleanup",
    "no-tool assembly", "professional grade", "ready out of the box", ' protein', "gluten-free", "vegan-friendly", "non-GMO", "sugar-free", "low-carb", "high-protein",
    "say goodbye to", "the perfect solution for", "engineered for", "ideal for", "optimized for", "built for",

    # --- Specificity & Authority (Building Trust) ---
    "tested for 50,000 cycles", "100% BPA-free", "military-grade durability",
    "ergonomically designed", "lab-certified", "recommended by [professionals]",
    "over 10,000 satisfied customers", "lifetime support included",
    "precision engineered", "30-day risk-free trial", "backed by science", "clinically tested", "patent-pending technology",

    # --- Emotional Triggers & Identity ---
    "perfect for gifting", "crafted for adventurers", "premium quality for professionals",
    "treat yourself to", "elevate your [activity]", "designed with your safety in mind",
    "join the [brand name] family", "built to last a lifetime", "experience the difference with", "unleash your potential with", "made for those who demand the best",

    # --- Use-Case Specificity (Semantic SEO) ---
    "ideal for hiking and camping", "perfect for small apartments",
    "optimized for mobile use", "great for back-to-school",
    "emergency preparedness essential", "compatible with [popular brand/model]",

    # --- Scarcity & Urgency (Psychological Triggers) ---
    "limited edition color", "exclusive access", "new 2026 model",
    "while supplies last", "special launch price",

    # --- Structural Headers (Best for Mobile Scanability) ---
    "CORE BENEFITS:", "WHAT'S INCLUDED:", "HOW IT WORKS:", 
    "SPECIFICATIONS:", "WHY CHOOSE US:", "DURABILITY MEETS DESIGN:"
]
desired_phrases = [phrase.lower() for phrase in desired_phrases]

MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(
    task="text-generation", 
    model=MODEL_ID,
    use_fast=True,
    kwargs={
        "return_full_text": False,
    },
    model_kwargs={}
)


def generate_product_description(item: str) -> str:
    system_prompt = f"""
        You are a product marketer for a company that makes nutrition supplements.
        Balance your product descriptions to attract customers, optimize SEO, and
        stay within accurate advertising guidelines.
        Product descriptions have to be 3-5 sentences.
        Provide only the product description with no preamble.
    """
    user_prompt = f"""
        Write a product description for a {item}.
    """

    input_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}   
    ]
    
    results = pipe(input_message, 
                   max_new_tokens=512)
    return results[0]['generated_text'][-1]['content'].strip()

prod = generate_product_description("protein drink")
print(prod)



def evaluate(descr: str, positives, negatives) -> int:
    # go through and count the number of desired phrases and banned phrases
    descr = descr.lower()
    num_positive = np.sum([1 for phrase in positives if phrase in descr])
    num_negative = np.sum([1 for phrase in negatives if phrase in descr])
    return int(num_positive - num_negative)

def evaluate_verbose(descr: str, positives, negatives) -> int:
    # go through and count the number of desired phrases and banned phrases
    descr = descr.lower()
    
    num_positive = num_negative = 0
    for phrase in positives:
        if phrase in descr:
            num_positive += 1
            print(f"Good: {phrase}")
    for phrase in negatives:
        if phrase in descr:
            num_negative += 1
            print(f"Bad: {phrase}")
    print(f"Good: {num_positive}   Bad: {num_negative}")
    return num_positive - num_negative

evaluate_verbose(prod, desired_phrases, banned_phrases)