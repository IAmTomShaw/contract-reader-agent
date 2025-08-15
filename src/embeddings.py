from openai import OpenAI

def generate_embedding(text: str) -> list[float]:
  """Generate embedding for the input text. Implement based on your model."""
  openai = OpenAI()
  response = openai.embeddings.create(
    model="text-embedding-ada-002",
    input=text
  )
  return response.data[0].embedding