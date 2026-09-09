import litellm

litellm.success_callback = ["langfuse", "mlflow", "helicone"]

response = litellm.completion(
  model="gpt-5.6-terra",
  messages=[{"role": "user", "content": "Hi!"}]
)
