import chainlit as cl
from agent import main
from agents import ItemHelpers


@cl.on_chat_start
async def start_chating():
    await cl.Message(content="Ask me about any Word.").send()

@cl.on_message
async def message(message:cl.Message):
    res = await  main(message.content)
    final_output = ""
    async for chunck in res.stream_events():
       if chunck.type == "run_item_stream_event":
            if chunck.item.type == "tool_call_item":
                print("Tool call:")
            elif chunck.item.type == "tool_call_output_item":
                print("Tool call output:")
            elif chunck.item.type == "message_output_item":
                print({ItemHelpers.text_message_output(chunck.item)})
                final_output = ItemHelpers.text_message_output(chunck.item)
    await cl.Message(content=f"{final_output}").send()