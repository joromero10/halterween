
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import check_budget

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are CostumeCraft, a creative Halloween costume stylist.

Recommend exactly 3 costumes based on the user's:
- Budget
- Existing wardrobe
- Preferred style
- Preparation time
- Locations to non-existing source materials


Rules:
1. Reuse clothing the user already owns.
2. Suggest affordable additional materials.
3. All costs are estimates in USD, not live prices.
4. Provide simple DIY instructions.
5. Avoid unsafe costume materials or instructions.
6. Be creative, practical, and Halloween-themed.

Return ONLY valid JSON with this structure:

{
  "costumes": [
    {
      "name": "Costume name",
      "description": "Short description",
      "items_needed": [
        {"name": "Item", "price": 5}
      ],
      "owned_items": ["Black dress"],
      "steps": ["Step 1", "Step 2"],
      "time_minutes": 30
    }
  ]
}

Prices must be numbers, not strings.
Items needed must only include things the user must buy.
"""



def generate_costumes(budget, wardrobe, style, prep_time):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
            Budget: ${budget}
            Wardrobe: {wardrobe}
            Style: {style}
            Preparation time: {prep_time} minutes

            Generate exactly 3 costume ideas.
            """
        }
    ]

    # Agent can revise its recommendations up to 3 times
    for attempt in range(3):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        costumes = result.get("costumes", [])
        valid = []
        feedback = []

        for costume in costumes:
            items = costume.get("items_needed", [])

            check = check_budget(items, budget)

            costume["total_cost"] = check["total_cost"]
            costume["within_budget"] = check["within_budget"]

            if not check["within_budget"]:
                feedback.append(
                    f"{costume['name']} costs "
                    f"${check['total_cost']}, "
                    f"but the budget is ${budget}."
                )

            elif costume.get("time_minutes", 9999) > prep_time:
                feedback.append(
                    f"{costume['name']} takes too long."
                )

            else:
                valid.append(costume)

        if len(valid) == 3:
            return valid

        # Give the AI feedback so it can improve
        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "user",
            "content": f"""
            Your previous recommendations failed validation.

            Problems:
            {feedback}

            Valid costumes found: {len(valid)}.

            Generate exactly 3 costumes again.
            All must meet the budget and time limits.
            """
        })

    # Return whatever valid recommendations remain
    return valid
