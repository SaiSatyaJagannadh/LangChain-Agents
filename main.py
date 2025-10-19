# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama


# load_dotenv()


# def main():
#     print("Hello from langchain-course!")
#     information = """
#     Elon Musk FRS (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman, known for his leadership of Tesla, SpaceX, X (formerly Twitter), and the Department of Government Efficiency (DOGE). Musk has been the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion.

#  activities, views, and statements have made him a polarizing figure, especially following the COVID-19 pandemic. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories, and affirming antisemitic, racist, and transphobic comments. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. His role in the second Trump administration attracted public backlash, particularly in response to DOGE.
#     """

#     summary_template = """
#     given the information {information} about a person I want you to create:
#     1. A short summary
#     2. two interesting facts about them
#     """

#     summary_prompt_template = PromptTemplate(
#         input_variables=["information"], template=summary_template
#     )

#     #llm = ChatOllama(temperature=0, model="gemma3:270m")
#     #llm = ChatOpenAI(temperature=0, model="o3-mini")
#     #gpt-oss:20b
#     llm = ChatOllama(model="gemma3:270m", temperature=0)
#    # llm = ChatOllama(model="gpt-oss:20b", temperature=0)


#     chain = summary_prompt_template | llm

#     response = chain.invoke(input={"information": information}) #invokes the chain
#     print(response.content)

# if __name__ == "__main__":
#     main()


# from dotenv import load_dotenv

# load_dotenv()

# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama

# from langchain_tavily import TavilySearch

# from schemas import AgentResponse


# tools = [TavilySearch()]
# # llm = ChatOpenAI(model="gpt-4o")
# llm = ChatOllama(model="llama3.2:latest")
# #llm = ChatOllama(model="gemma3:270m")



# agent = create_agent(
#     model=llm,
#     tools=tools,
#     response_format=AgentResponse,
# )


# def main():
#     result = agent.invoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": "search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details",
#                 }
#             ]
#         }
#     )
#     # Access structured response from the agent
#     structured = result.get("structured_response", None)
#     print(structured if structured is not None else result)


# if __name__ == "__main__":
#     main()



from typing import List

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.tools import tool, BaseTool
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


from callbacks import AgentCallbackHandler

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters just in case

    return len(text)


def find_tool_by_name(tools: List[BaseTool], tool_name: str) -> BaseTool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello LangChain Tools (.bind_tools)!")
    tools = [get_text_length]

    llm = ChatOllama(
        model="llama3.2:latest",
        temperature=0,
        callbacks=[AgentCallbackHandler()],
    )
    llm_with_tools = llm.bind_tools(tools)

    # Start conversation
    messages = [HumanMessage(content="What is the length of the word: DOG")]

    while True:
        ai_message = llm_with_tools.invoke(messages)

        # If the model decides to call tools, execute them and return results
        tool_calls = getattr(ai_message, "tool_calls", None) or []
        if len(tool_calls) > 0:
            messages.append(ai_message)
            for tool_call in tool_calls:
                # tool_call is typically a dict with keys: id, type, name, args
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")

                tool_to_use = find_tool_by_name(tools, tool_name)
                observation = tool_to_use.invoke(tool_args)
                print(f"observation={observation}")

                messages.append(
                    ToolMessage(content=str(observation), tool_call_id=tool_call_id)
                )
            # Continue loop to allow the model to use the observations
            continue

        # No tool calls -> final answer
        print(ai_message.content)
        break