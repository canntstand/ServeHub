from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from backend.async_send_message import async_send_message
import asyncio

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(async_send_message, trigger=IntervalTrigger(minutes=1), id="email_sending", replace_existing=True)
    scheduler.start()
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())