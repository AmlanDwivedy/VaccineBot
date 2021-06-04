import schedule
import time


def job():
    print("I am working")


schedule.every(3).seconds.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(2)
