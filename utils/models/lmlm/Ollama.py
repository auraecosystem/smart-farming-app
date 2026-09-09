from litellm import completion

response = completion(
  model="ollama/llama3",
  messages=[{"role": "user", "content": "Hello, how are you?"}],
  api_base="http://localhost:6080"
)
print(response.choices[0].message.content)
