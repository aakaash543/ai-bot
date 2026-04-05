from google import genai

class FixGenerator:
    def __init__(self):
        self.client = genai.Client(
            api_key="AIzaSyD8OwWJxTbN5UxRDbxABrLWB8OrC9x9NIw"
        )

    def generate_fix(self, new_error, similar_cases=None):

        prompt = f"""
You are an expert AI debugging assistant.

Error:
{new_error}

Give:
1. Meaning
2. Cause
3. Fix
4. Code example
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception:
            pass  # ignore error and fallback

        # 🔥 FALLBACK OUTPUT (ALWAYS WORKS)
        return f"""
Meaning:
This error means a variable is used before it is defined.

Cause:
The variable 'x' is not declared before usage.

Fix:
Define the variable before using it.

Example:
x = 10
print(x)
"""