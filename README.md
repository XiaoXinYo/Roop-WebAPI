![Release](https://img.shields.io/badge/Release-0.1.0-blue)
---
## Introduce
[S0md3v/Roop](https://github.com/s0md3v/roop) WebAPI.  
WebUI: [Coaixy/Roop-WebUI-V](https://github.com/Coaixy/Roop-WebUI-V)
## Demand
1. Platform: Windows/Linux/Docker.
2. Language: Python3.8+.
3. Package: gunicorn,gevent,flask,flask_cors,flask_apscheduler,redis.
4. Database: Redis.
5. Other: Roop(Including What It Requires).
## Config
Enter the config.py file view.
## Arrange
### Step
1. Install Python3.8+.
3. Download the corresponding version of the Loop and copy it into the Loop folder.
2. Install FFmpeg.
3. Install Cuda(If Nvidia GPU is used).
4. Install Redis.
5. Install Visual Studio,then install C++ desktop development dependencies(If the platform is Windows).
6. install the Roop python package.
7. Install the Roop-WebAPI python package.
8. Configure the config.py file.
9. Run(The first task execution will download dependencies).
### Run
1. Windows: run wsgi.py file.
2. Linux: execute `gunicorn main:APP -c gunicorn.py` command.
3. Support Docker.
