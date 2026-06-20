from google import genai

client = genai.Client(api_key="AQ.Ab8RN6Log7ZuBgbdBwNiIbzZozI0gxiAR9VajyjE5QbJzF-SUw")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is coding?"
)

print(response.text)
