# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     messages = data.get('messages', [])

#     def generate():
#         stream = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo-0125",
#             messages=messages,
#             stream=True
#         )

#         for chunk in stream:
#             if chunk.choices[0].delta.get("content"):
#                 yield chunk.choices[0].delta.content

#     return Response(generate(), mimetype='text/event-stream')

