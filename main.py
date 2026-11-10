import asyncio
import json
import os
from engine import QureoExecutor

async def main():
    config_path = "config.json"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found. Please create it first.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    CHAPTER = config.get("chapter", "23")
    USERNAME = config.get("username")
    PASSWORD = config.get("password")
    LESSON_NUMBERS = config.get("lessons", [])

    if not USERNAME or not PASSWORD:
        print("Error: Username and password are required in config.json")
        return

    lessons = [f"900{CHAPTER}0{l_num}0" for l_num in LESSON_NUMBERS]

    bot = QureoExecutor()
    await bot.start(headless=False, record_video=True, video_name=f"Solve_Chapter_{CHAPTER}")
    
    try:
        await bot.login(USERNAME, PASSWORD)
        
        print(f"--- Starting Lessons for Chapter {CHAPTER} ---")
        for l_id in lessons:
            await bot.surgical_skip(CHAPTER, l_id)
        
        print("\n Level and Test progression complete")
        await bot.page.goto(f"https://me-tp.qureo.education/chapter/900{CHAPTER}/")
        
        print("Close the browser when ready")
        await asyncio.Future()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())