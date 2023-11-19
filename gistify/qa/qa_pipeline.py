import argparse

import torch
from gistify.config import logger
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer


def answer(question: str, context: str) -> str:
    """Question answering pipeline.

    Args:
        question (str): Question to ask from the context.
        text (str): The context from which questions are to be asked.

    Returns:
        str: response/answer.
    """
    inputs = tokenizer(question, context, return_tensors="pt")
    with torch.no_grad():
        logger.info("Running question answering pipeline.")
        outputs = model(**inputs)

    answer_start_index = torch.argmax(outputs.start_logits)
    answer_end_index = torch.argmax(outputs.end_logits)

    try:
        logger.info("Decoding qa response.")
        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        response = tokenizer.decode(predict_answer_tokens)
    except Exception as e:
        logger.error(e)

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input question and context based on which the answer should be given.")

    parser.add_argument("--question", metavar="", type=str, help="Question to ask.")
    parser.add_argument("--context", metavar="", type=str, default="transcribe", help="Context based on which answer should be given.")

    args = parser.parse_args()

    question = args.question
    context = args.context

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    model = DistilBertForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

    # question, text = (
    #     "What are some limitations of JavaScript?",
    #     "JavaScript doesn't allow you to specify what type something is. I'm guessing that wasn't deemed very useful for simply animating some HTML buttons. It also makes sense because it's quite common in web development that variables hold different types of data depending on what the user does or what kind of data the server returns. However, if you want to develop a full-fledged web application, not having these types is a recipe for disaster. And this is also why TypeScript has become so popular. TypeScript is a superset of JavaScript that adds static types to the language. With TypeScript, you can write type annotations and the TypeScript compiler will check the types at compile time when you compile the code to JavaScript, helping you catch common errors before they run.",
    # )
    response = answer(question, context)
    print(response)
