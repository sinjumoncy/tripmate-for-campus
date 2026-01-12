import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=os.getenv("HF_TOKEN")
)

def generate_itinerary(prompt: str) -> str:
    response = client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an expert travel planner for college students."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=700,
        temperature=0.7,
        top_p=0.9
    )

    return response.choices[0].message.content




