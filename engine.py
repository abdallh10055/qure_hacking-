import asyncio
import os
from playwright.async_api import async_playwright

class QureoExecutor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.video_name = None

    async def start(self, headless=False, record_video=False, video_name=None):
        self.video_name = video_name
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        
        context_args = {
            "viewport": {'width': 1280, 'height': 800}
        }
        
        if record_video:
            video_dir = os.path.join(os.getcwd(), "saved", "videos")
            os.makedirs(video_dir, exist_ok=True)
            context_args["record_video_dir"] = video_dir
            print(f"Video recording enabled. Saved to: {video_dir}")

        self.context = await self.browser.new_context(**context_args)
        self.page = await self.context.new_page()

    async def login(self, username, password):
        print(f"Logging in...")
        await self.page.goto("https://me-portal.qureo.education/login")
        await self.page.click("text=Go to Learning")
        await self.page.fill("#student_id", username)
        await self.page.fill("#password", password)
        await self.page.click("button.login-button")
        try:
            await self.page.wait_for_selector("text=ابدأ", timeout=15000)
            print(" Logged In.")
        except:
            print("Login wait timeout.")

    async def surgical_skip(self, chapter_id, lesson_id):
        lesson_url = f"https://me-tp.qureo.education/chapter/900{chapter_id}/lecture/{lesson_id}"
        print(f"Processing Lesson: {lesson_id}...")
        try:
            await self.page.goto(lesson_url, wait_until="networkidle")
            await asyncio.sleep(1)
            
            script = f"""
            fetch('https://me-tp.qureo.education/api/study/students/lectures/{lesson_id}/complete', {{ method: 'PUT' }})
            .then(res => res.status)
            .catch(e => 404)
            """
            status = await self.page.evaluate(script)
            
            if status not in [200, 204, 400]:
                script2 = f"""
                fetch('https://me-tp.qureo.education/api/study/students/lecture-talks/{lesson_id}/complete', {{ method: 'PUT' }})
                .then(res => res.status)
                """
                status = await self.page.evaluate(script2)

            if status in [200, 204]:
                print(f"   ID {lesson_id}: Success")
                return True
            elif status == 400:
                print(f"   ID {lesson_id}: Already Done")
                return True
            else:
                print(f"   ID {lesson_id}: Failed (Status {status})")
                return False
        except Exception as e:
            print(f"   Error: {e}")
            return False

    async def close(self):
        video_path = None
        if self.page and self.page.video:
            try:
                video_path = await self.page.video.path()
            except:
                pass

        try:
            if self.browser: await self.browser.close()
            if self.playwright: await self.playwright.stop()
        except Exception as e:
            pass
        
        if video_path and os.path.exists(video_path):
            final_path = video_path
            if self.video_name:
                directory = os.path.dirname(video_path)
                safe_name = "".join([c for c in self.video_name if c.isalnum() or c in (' ', '.', '_', '-')]).strip()
                if not safe_name.lower().endswith(".webm"):
                    safe_name += ".webm"
                
                final_path = os.path.join(directory, safe_name)
                try:
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(video_path, final_path)
                except Exception as e:
                    print(f"   Warning: Could not rename video: {e}")
                    final_path = video_path

            print(f"\n Video saved successfully!")
            print(f" Path: {final_path}")
            print(f" You can share this file directly.")
