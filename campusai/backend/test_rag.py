from app.services.llm_service import generate_answer
question = "What is the minimum attendance requirement?"
context = "The minimum attendance requirement is 75% for all courses."
answer=generate_answer(question,context)
print(answer)