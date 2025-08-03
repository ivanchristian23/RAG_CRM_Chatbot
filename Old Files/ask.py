import requests

while True:
    question = input("You: ")
    if question.lower() in ['exit', 'quit']:
        break

    response = requests.post("http://192.168.10.9/generate", json={"question": question})

    if response.status_code == 200:
        print("Bot:", response.json()["response"])
    else:
        print("Error:", response.status_code, response.text)
