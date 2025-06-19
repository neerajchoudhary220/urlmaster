import os,subprocess

def kill_pid():
    ports =[8080,8090]
    for port in ports:
        command=f"lsof -i :{port} -t"
        result= subprocess.run(command,shell=True,stdout=subprocess.PIPE, text=True)
        pids = result.stdout.strip().splitlines()
        for pid in pids:
            os.kill(int(pid),9)


    