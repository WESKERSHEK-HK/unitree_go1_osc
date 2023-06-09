<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->




<!-- PROJECT LOGO -->

<div align="center">

<h1 align="center">Unitree Go1 OSC</h3>
<br />
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

  This project aims to use python-osc with ROS melodic to controls robot dog: Unitree Go1.

### Requirments

* Python3 Library
  ```sh
  sudo apt-get install python3-pip python3-yaml
  sudo pip3 install rospkg catkin_pkg python-osc
  ```
* Unitree Legged SDK 3.8.0 (https://github.com/unitreerobotics/unitree_legged_sdk)

* Unitree Legged Real 3.5.1 (https://github.com/unitreerobotics/unitree_ros_to_real)

### Installation

1. Clone the repo to your workspace:
   ```sh
   git clone https://github.com/WESKERSHEK-HK/unitree_go1_osc.git
   ```
2. Change IP address in osc_control.py line 84:
   ```sh
   server = osc_server.ThreadingOSCUDPServer(('IP', PORT), disp)
   ```
3. Catkin_make
   ```js
   cd
   cd "your work space here"
   catkin_make
   ```
4. Run
   ```js
   roslaunch unitree_legged_real keyboard_control.launch
   rosrun unitree_go1_osc osc_control
   ```

### Additional Configuration
* Edit unitree_legged_real/include/covert.h line 308-329:
  ```js
  cmd.head[0] = 0xFE;
  cmd.head[1] = 0xEF;
  cmd.levelFlag = UNITREE_LEGGED_SDK::HIGHLEVEL;
  cmd.mode = 0;
  cmd.gaitType = 0;
  cmd.speedLevel = 0;
  cmd.footRaiseHeight = 0;
  cmd.bodyHeight = 0;
  cmd.euler[0] = 0;
  cmd.euler[1] = 0;
  cmd.euler[2] = 0;
  cmd.velocity[0] = 0.0f;
  cmd.velocity[1] = 0.0f;
  cmd.yawSpeed = 0.0f;
  cmd.reserve = 0;

  cmd.velocity[0] = msg->linear.x;
  cmd.velocity[1] = msg->linear.y;
  cmd.yawSpeed = msg->angular.z;
  cmd.bodyHeight = msg->angular.y;

  cmd.mode = 2;
  cmd.gaitType = 1;
  ```
