from huggingface_hub import InferenceClient

# NOTE:
# Token is used as per the reference guide followed for this project.
# For production systems, environment variables are recommended.
HF_TOKEN = "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"

client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=HF_TOKEN
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
#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