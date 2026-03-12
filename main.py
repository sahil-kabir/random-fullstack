import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch.nn.functional as F

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    context: str


class AnswerResponse(BaseModel):
    answer: str
    score: float
    start: int
    end: int


device: int | str = -1
if torch.backends.mps.is_available():
    device = "mps"

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained(
    "distilbert-base-uncased-distilled-squad"
)
model.to(device)


@app.get("/")
async def hello() -> HTMLResponse:
    return HTMLResponse(content="<h1>Hello</h1>")


@app.post("/agent", response_model=AnswerResponse)
async def answer_question(request: QuestionRequest) -> AnswerResponse:
    if not request.question or not request.context:
        raise HTTPException(status_code=400, detail="Question and context are required")

    inputs = tokenizer(
        request.question,
        request.context,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    start_logits = outputs.start_logits[0]
    end_logits = outputs.end_logits[0]

    start_idx = torch.argmax(start_logits)
    end_idx = torch.argmax(end_logits) + 1

    if end_idx < start_idx:
        end_idx = start_idx + 1

    answer_ids = inputs["input_ids"][0][start_idx:end_idx]
    answer = str(tokenizer.decode(answer_ids, skip_special_tokens=True))

    start_prob = F.softmax(start_logits, dim=-1)[start_idx].item()
    end_prob = F.softmax(end_logits, dim=-1)[end_idx - 1].item()
    score = (start_prob + end_prob) / 2

    return AnswerResponse(
        answer=answer,
        score=score,
        start=int(start_idx.item()),
        end=int(end_idx.item()) - 1,
    )
