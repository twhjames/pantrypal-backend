from fastapi import FastAPI, UploadFile, File
from utils import filter_food_items
import uuid
import base64
import json
import requests
import re

from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()


# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Subcategories (as before)
subcategories = [
    'Baby & Toddler Food', 'Baking Needs', 'Beef & Lamb', 'Beer', 'Beverages', 'Biscuits', 'Breads',
    'Breakfast', 'Butter, Margarine & Spreads', 'Canned Food', 'Champagne & Sparkling Wine', 'Cheese',
    'Chicken', 'Chilled Beverages', 'Chilled Food', 'Chocolates', 'Coffee', 'Condiments',
    'Cooking Paste & Sauces', 'Cream', 'Delicatessen', 'Dried Fruits & Nuts', 'Drink Mixers', 'Eggs',
    'Fish & Seafood', 'Fresh Milk', 'Frozen Desserts', 'Frozen Food', 'Frozen Meat', 'Frozen Seafood',
    'Fruits', 'Ice Cream', 'Infant Formula', 'Jams, Spreads & Honey', 'Juices', 'Meatballs', 'Milk Powder',
    'Non Alcoholic', 'Noodles', 'Oil', 'Pasta', 'Pork', 'Ready-To-Eat', 'Rice', 'Seasonings', 'Snacks',
    'Soups', 'Spirits', 'Sugar & Sweeteners', 'Sweets', 'Tea', 'Uht Milk', 'Vegetables', 'Water', 'Wine',
    'Yoghurt'
]

def extract_json(text):
    # Try to find a ```json ... ``` block
    match = re.search(r'```(?:json)?\s*(\[\s*{.*?}\s*\])\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback: look for any array of dicts
    match = re.search(r'(\[\s*{.*?}\s*\])', text, re.DOTALL)
    if match:
        return match.group(1)
    
    raise ValueError("No valid JSON array found in the LLM output.")


def classify_receipt_items(receipt_json: dict) -> list:
    cleaned_items = receipt_json['Items']
    final_items = [item['ITEM'].replace("\n", " ") for item in cleaned_items]

    subcat_text = ", ".join(f'"{cat}"' for cat in subcategories)

    prompt = f"""
You are a helpful assistant trained to classify receipt items from Singapore supermarkets (e.g., Sheng Siong, FairPrice, Cold Storage). These items include local produce, regional snacks, and brands common in Southeast Asia.
For example, here is a list of known Singapore brands and what they typically sell:

- Marigold: Milk, yogurt, fruit juices, condensed milk
- Gold Roast: Instant coffee, cereal drinks
- Yeo’s: Asian beverages, sauces
- F&N: Soft drinks, canned milk
- Kara: Coconut cream, coconut milk
- Ayam Brand: Canned tuna, sardines, baked beans
- Khong Guan: Biscuits, crackers
- Han’s: Ready-to-eat meals, pastries
- Prima Taste: Cooking pastes, instant noodles
- Chng Kee’s: Asian cooking sauces
- Tong Garden: Nuts, snacks
- Camel Nuts: Nuts and snacks
- Bee Cheng Hiang: Bak kwa, pork floss
- Koka: Instant noodles
- Myojo: Instant noodles
- Chilli Brand: Sambal, chili pastes
- CP (Singapore): Ready-to-eat frozen meals
- SongHe: Rice
- Golden Peony: Rice
- FairPrice: Groceries, household goods
- Pasar: Fruits, vegetables, fresh meats
- Mama Lemon: Dishwashing liquid
- Softlan: Fabric softener
- Top: Laundry detergent
- Dumex Dugro: Baby formula
- Mamil Gold: Infant formula
- NooTree: Plant-based snacks for kids

Use this context to determine whether an item is a food or non-food item, and assign an appropriate sub-category.

For each item, do the following:
- Extract the quantity of each item. If there is no quantity, put 1 as default
- Determine whether it is a "food" or "non-food" item.
- If it is a "food" item, assign one sub-category from the list below:
{subcat_text}
- If it is a "non-food" item, set sub-category to null.

Return your answer in only JSON array format with fields:
- ITEM
- CATEGORY ("food" or "non-food")
- SUBCATEGORY (must match exactly one of the listed values, or null for non-food)
- QUANTITY 

Items:
""" + "\n".join(f"{i+1}. {item}" for i, item in enumerate(final_items))

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.choices[0].message.content
    json_str = extract_json(raw_output)
    return json.loads(json_str)


app = FastAPI()

# ✅ AWS Lambda API Gateway endpoint (receives base64 image)
UPLOAD_API_URL = "https://q2wq7z7gbh.execute-api.ap-southeast-2.amazonaws.com/upload_receipts"
RETRIEVE_API_URL = "https://q2wq7z7gbh.execute-api.ap-southeast-2.amazonaws.com/receipt-status"  

# 🟩 Route: Upload a receipt image
@app.post("/upload-receipt/")
async def upload_receipt(file: UploadFile = File(...)):
    # 🔑 Step 1: Simulate user ID (later replace with real login system)
    user_id = "user234"

    # 🧾 Step 2: Generate unique filename (e.g. 123e4567.jpg)
    receipt_id = str(uuid.uuid4()) + ".jpg"

    # 📦 Step 3: Read and encode image to base64
    image_bytes = await file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # 🧳 Step 4: Prepare JSON payload
    payload = {
        "user_id": user_id,
        "receipt_id": receipt_id,
        "image_base64": encoded_image
    }

    # 🚀 Step 5: Send to AWS Lambda
    headers = {"Content-Type": "application/json"}
    response = requests.post(UPLOAD_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return {"error": "Upload failed", "details": response.text}

    return {
        "message": "Upload successful",
        "user_id": user_id,
        "receipt_id": receipt_id
    }

# 🟦 Route: Retrieve scanned result
@app.get("/get-classified-receipt-result/")
def get_result(user_id: str, receipt_id: str):
    response = requests.get(RETRIEVE_API_URL, params={
        "user_id": user_id,
        "receipt_id": receipt_id
    })

    if response.status_code != 200:
        return {"error": "Result not ready", "details": response.text}

    try:
        # return response.json()
         receipt_json = response.json()

        # Step 2: Classify items using Groq
         classification_result = classify_receipt_items(receipt_json)

         return {
            "receipt_id": receipt_id,
            "vendor": receipt_json.get("Vendor"),
            "date": receipt_json.get("Date"),
            "classified_items": classification_result
        }



    except Exception as e:
        return {"error": "Failed to process response", "exception": str(e)}



