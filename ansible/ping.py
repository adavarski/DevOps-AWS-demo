import time
import subprocess

#currenttime = time.strftime("%H:%M:%S", time.gmtime())
currenttime = time.time()
Ftime = time.time() + 30

def lambda_handler(event,context):
    while time.time() <= Ftime:
        # response = pyping.ping('www.google.com')
        # if response.ret_code == 0:
        #     print("Ping successfull for google.com")
        # else:
        #     print("Google.com unreacble")
        status,result = subprocess.getstatusoutput("ping -c1 www.google.com")
        if status == 0:
            print("Ping successfull for google.com")
        else:
            print("Google.com unreacble")
        time.sleep(10)


if __name__ == '__main__':
    event = 1
    context = 1
    lambda_handler(event,context)
