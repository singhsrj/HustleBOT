SUMMARY_TEMPLATE = """
You are an expert startup evaluator.

Below are the internal thoughts and tool outputs (intermediate logs) from an AI agent analyzing the Problem-Solution Fit of a startup idea.

Your task is to:
1. Extract key insights from each step.
2. Summarize the reasoning the AI used to evaluate the idea.
3. Highlight findings related to:
    - Problem Clarity
    - Urgency
    - User Willingness to Pay
    - Market Relevance
4. Present the summary in clean bullet points.

--- INTERMEDIATE LOGS START ---
{logs}
--- INTERMEDIATE LOGS END ---

Now provide a concise, bullet-point summary of what the agent discovered:
"""
problem_solution_fit_template=f""" Given the startup idea description below, evaluate its Problem-Solution Fit:

Startup Idea: {idea_description}

Answer the following:

Is this solving a clearly defined and urgent problem?

How likely are people to pay for this solution? Provide reasoning.

Is the problem widespread and relevant to a large or niche group?

Score the following:

Problem clarity and relevance (out of 8%)

Urgency of the problem (out of 10%)

User willingness to pay / validation (out of 12%)

Total score (out of 30%): ___% 
         
Just return the score , nothing more, nothing less """ 