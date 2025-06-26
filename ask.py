import requests

while True:
    question = input("You: ")
    if question.lower() in ['exit', 'quit']:
        break

    response = requests.post("http://localhost:8000/chat", json={"question": question})

    if response.status_code == 200:
        print("Bot:", response.json()["response"])
    else:
        print("Error:", response.status_code, response.text)
