# # imports
# import spacy
# from spacy.matcher import PhraseMatcher

# from skillNer.general_params import SKILL_DB
# from skillNer.skill_extractor_class import SkillExtractor

# nlp = spacy.load("en_core_web_lg")
# skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# job_description = """
# You are a Python developer with a solid experience in web development
# and can manage projects. You quickly adapt to new environments
# and speak fluently English and French
# """

# annotations = skill_extractor.annotate(job_description)

# print(annotations)

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from together import Together
import random

app = FastAPI()
client = Together()

@app.get("/generate_question/{request}")
async def generate_coding_question(request):
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {"role": "system", "content": "You are an AI that generates coding questions."},
                {"role": "user", "content": f"Generate only one random and unique coding question about {request} and just return the question in string format."},
            ],
            temperature=round(random.uniform(0.4, 0.9), 1),
        )
        question_content = response.choices[0].message.content
        return (question_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)