from app.services.llm_service import generate_answer


context = """
College Attendance Regulations

Students must maintain a minimum attendance of 75 percent.

Students with attendance below 75 percent may not be permitted
to appear for the semester examination.

Medical leave may be considered according to college regulations.
"""


question = "What is the minimum attendance requirement?"


answer = generate_answer(
    question=question,
    context=context
)


print("\nGemini Answer:")
print(answer)