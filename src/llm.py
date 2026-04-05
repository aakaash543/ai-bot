import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class FixGenerator:
    def __init__(self):
        # We assume GEMINI_API_KEY is in the environment
        if not os.environ.get("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        self.client = genai.Client()

    def generate_fix(self, new_error, similar_cases):
        """
        Takes the new error and similar historical cases to generate a fix using the LLM.
        """
        # Prompt Augmentation
        prompt = "You are an expert AI debugging assistant.\n"
        prompt += f"A developer encountered the following error:\n{new_error}\n\n"
        
        if similar_cases and len(similar_cases.get('documents', [])) > 0 and len(similar_cases['documents'][0]) > 0:
            prompt += "Here are some similar errors from our internal history and how they were fixed:\n"
            
            docs = similar_cases['documents'][0]
            metas = similar_cases['metadatas'][0]
            
            for i, (doc, meta) in enumerate(zip(docs, metas)):
                prompt += f"\n--- Historical Case {i+1} ---\n"
                prompt += f"Error Context:\n{doc}\n"
                prompt += f"Solution Applied:\n{meta['solution_code']}\n"
                prompt += f"Explanation:\n{meta['explanation']}\n"
                prompt += "---------------------------\n"
        else:
            prompt += "We do not have any historical cases matching this error.\n\n"
            
        prompt += "\nBased on the error context and the historical solutions provided above (if any), please suggest the best code fix for the new error.\n"
        prompt += "Include an explanation of the fix and the suggested code."

        # Make the LLM call using google-genai
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return response.text
