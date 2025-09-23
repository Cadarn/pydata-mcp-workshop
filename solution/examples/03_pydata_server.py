import json
import httpx
from fastmcp import FastMCP
from typing import Any

mcp = FastMCP(
    name="PyData Amsterdam Server",
)

@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Provides a simple greeting message from PyData Amsterdam 2025"""
    return "Hello from the PyData Amsterdam 2025 Server!"


@mcp.resource(
        uri="resource://pydata-amsterdam-2025-schedule.json",
        description="Fetches schedule JSON data from the PyData Amsterdam 2025 conference online schedule",
        mime_type="application/json"
        )
def get_pydata_schedule() -> json:
    """Fetches schedule JSON data from the PyData Amsterdam 2025 conference online schedule and returns it."""
    url = "https://cfp.pydata.org/pydata-amsterdam-2025/schedule/export/schedule.json"
    resp = httpx.get(url)
    resp.raise_for_status()
    data = process_pydata_schedule(resp.json())
    return json.dumps(data)

@mcp.prompt
def linkedIn_post_generator(topic: str) -> str:
    """
    Generates a LinkedIn post for a given topic at the PyData Amsterdam 2025 conference.
    """
    prompt = f"""You are an expert social media manager that excels in writing LinkedIn posts that garner engagement. 
    Produce a LinkedIn post that highlights the excitement around new learnings and topics at the PyData Amsterdam 
    2025 conference. Make sure to use emojis as approriate, and keep the post less than 250 words. 
    Use the topic context below to inform the post:
    CONTEXT: {topic}
    """
    return prompt

def process_pydata_schedule(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Simplifies and cleans the raw schedule data from a PyData JSON export.

    This function navigates the nested dictionary structure to extract individual
    talk details, flattens them into a list, and enriches them with
    speaker information.

    Args:
        raw_data: The raw dictionary loaded from the schedule.json file.

    Returns:
        A list of dictionaries, where each dictionary represents a single,
        cleaned talk or event. Returns an empty list if the expected
        data structure is not found.
    """
    all_talks: list[dict[str, Any]] = []
    keys_to_keep = [
        "date", "start", "duration", "room", "url", 
        "title", "abstract", "type"
    ]

    try:
        # Safely access the nested list of days
        days = raw_data.get("schedule", {}).get("conference", {}).get("days", [])

        for day in days:
            # Iterate through each room and its list of talks
            for room_name, talks_in_room in day.get("rooms", {}).items():
                for talk in talks_in_room:
                    # Use a dictionary comprehension for conciseness
                    processed_talk = {key: talk.get(key) for key in keys_to_keep}
                    
                    # Manually set the room name from the dictionary key
                    processed_talk["room"] = room_name

                    # Use a list comprehension to extract and format speaker details
                    # .get("persons", []) ensures it works even if there are no speakers
                    processed_talk["persons"] = [
                        {"name": person.get("name"), "url": person.get("url")}
                        for person in talk.get("persons", [])
                    ]
                    
                    all_talks.append(processed_talk)

    except (KeyError, TypeError) as e:
        print(f"⚠️ Error processing data: The data structure might be invalid. Details: {e}")
        return [] # Return an empty list on failure

    return all_talks

if __name__ == "__main__":
    mcp.run()