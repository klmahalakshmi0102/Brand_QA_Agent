
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.graph.state import BrandQAState


class RelevanceGrade(BaseModel):
    relevant: bool = Field(
        description=(
            "True if the document contains useful information "
            "for answering the user's question, otherwise False."
        )
    )


if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from the .env file")


llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    api_key=GROQ_API_KEY
)

grader = llm.with_structured_output(
    RelevanceGrade,
    method="json_schema"
)



async def grade_node(state: BrandQAState) -> dict:
    question = state["question"]
    retrieved_docs = state.get("retrieved_docs", [])

    relevant_docs = []

    for doc in retrieved_docs:
        prompt = f"""
        You are a relevance evaluator for a multi-tenant
        brand question-answering system.

        User question:
        {question}

        Retrieved document:
        {doc.page_content}

        Determine whether this document contains useful
        evidence for answering the user's question.

        Mark it relevant only if it provides information
        that helps answer the question.

        Do not use outside knowledge.
        """

        # Asynchronous Groq call
        result = await grader.ainvoke(prompt)

        if result.relevant:
            relevant_docs.append(doc)

    trace = list(state.get("trace", []))
    trace.append(
        f"Graded {len(retrieved_docs)} retrieved chunks; "
        f"{len(relevant_docs)} relevant chunks found."
    )

    return {
        "relevant_docs": relevant_docs,
        "trace": trace
    }
