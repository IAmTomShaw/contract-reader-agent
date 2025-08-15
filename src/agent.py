from agents import Agent, Runner, TResponseInputItem, function_tool, WebSearchTool

from pydantic import BaseModel, Field

from src.astra import vector_search, find_all_snippets

import json

class HistoricalChange(BaseModel):
  id: str = Field(..., description="The unique identifier for the historical change.")
  original_snippet: str = Field(..., description="The original snippet of the contract that you want to query or change.")
  modified_snippet: str = Field(..., description="The modified snippet of the contract.")
  ignored: bool = Field(..., description="Whether this change has been ignored.")

@function_tool
def search_for_similar_historical_changes(original_snippet: str) -> list[HistoricalChange]:
  """
    Use a snippet from the contract that you are unsure about to search the database to check for any historical changes to this clause.

    Input: {original_snippet}

    Output: A list of similar historical changes found in the database (includes a the matched snippet that is similar to your query, the modified version which replaced the matched snippet and whether the matched snippet should be ignored)
  """

  print("Checking for similar historical changes...: ", original_snippet)

  results = vector_search(original_snippet)
  return [HistoricalChange(**doc) for doc in results]



class AgentSuggestedContractChange(BaseModel):
  original_snippet: str = Field(..., description="The original snippet of the contract that you want to query or change.")
  modified_snippet: str = Field(None, description="The modified snippet of the suggested update that you want to make to the snippet.")
  question_from_agent: str = Field(None, description="A question that you would like to ask the user about the original snippet")


async def run_agent(input: str):

  snippets = find_all_snippets()

  # Format snippets separated with <snippet><original><modified><ignored></snippet>
  formatted_snippets_string = "\n".join(
    f"<snippet><original>{s['original']}</original><modified>{s['modified']}</modified><ignored>{s['ignored']}</ignored></snippet>"
    for s in snippets
  )

  agent = Agent(
    name="Contract Reviewer Agent",
    instructions=f"""
      <background>
        You are a contract reviewer agent. Your job is to analyze and review contract clauses. You are reviewing contracts for an influencer (also referred to as "talent", "content creator" and potentially other terms), so any changes that you made should be with the intention of protecting the influencer's best interests and aligning with their standard terms for engaging with brands.
      </background>
      <task>
      Review the contract text provided in the input. For each clause, identify any potential issues or areas for improvement. Before returning a suggestion back to the user, if you are unsure of a clause or how the influencer would like to handle a specific clause, look through the <historical changes> to see if a clause similar to the one you're struggling with has already been handled. If you find a record of how a similar clause was modified or not modified, use that information to inform your review. If there is a clause that has already been modified and saved in the database, you should suggest the exact modified version that is stored in the database. If you do not find a similar clause, add it to your response to send to the user.
      If you find a snippet that has been recorded in the database as ignored, you should not return this snippet to the user.
      </task>
      <output>
      You should output an array of change suggestions or queries to send to the user. When you make a suggestion, it should be written exactly how you would amend the contract text. Do not address the user in the "modified_snippet" field.
      </output>
      <historical changes>
      {formatted_snippets_string}
      </historical changes>
    """,
    model="gpt-4o-mini",
    output_type=list[AgentSuggestedContractChange],
  )

  result = await Runner.run(agent, input, max_turns=40)
  # Convert Pydantic model to dict for JSON serialization
  # Handle different result structures
  if hasattr(result, 'content') and result.content:
    output_data = result.content
  elif hasattr(result, 'final_output') and result.final_output:
    output_data = result.final_output
  else:
    return []
  
  # Save the result as JSON (if you want to keep it)
  with open("processed_result.json", "w", encoding="utf-8") as f:
    # Convert VideoEdit objects to dict for JSON serialization
    if isinstance(output_data, list):
      json_data = [change.dict() if hasattr(change, 'dict') else change for change in output_data]
    else:
      json_data = output_data
    json.dump(json_data, f, ensure_ascii=False, indent=4)

  return json_data