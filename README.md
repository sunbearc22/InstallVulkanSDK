# InstallVulkanSDK
A Python 3.6 script to install LunarG Vulkan SDK in Ubuntu 18.04.

Tested on Ubuntu 18.04 with linux kernel 5.0.0-23-generic and with Vulkan SDK versions:
  
 `1.2.141.2`, `1.2.135.0`, `1.2.131.2`, `1.2.131.1`,
 `1.1.130.0`, `1.1.126.0`, `1.1.121.1`, `1.1.114.0`, `1.1.108.0`,
 `1.1.106.0`, `1.1.101.0`,  `1.1.97.0`,  `1.1.92.1`,  `1.1.85.0`,
  `1.1.82.1`,  `1.1.82.0`,  `1.1.77.0`,  `1.1.73.0`,  `1.1.70.1`,
  `1.1.70.0`,
  `1.0.68.0`,  `1.0.65.0`,  `1.0.61.1`,  `1.0.61.0`,  `1.0.57.0`,
  `1.0.54.0`, `1.0.51.0`,   `1.0.49.0`,  `1.0.46.0`,  `1.0.42.2`,
  `1.0.39.1`, `1.0.39.0`,   `1.0.33.0`,  `1.0.30.0`,  `1.0.26.0`,
  `1.0.24.0`, `1.0.21.1`,   `1.0.21.0`,  `1.0.17.0`,  `1.0.13.0`,
  `1.0.11.0`,  `1.0.8.0`,   `1.0.5.0`,   `1.0.3.1`


## Preliminary
1. Clone/Download `InstallVulkanSDK` to your Ubuntu system and extract the file `installVulkanSDK.py`.

## Install LunarG Vulkan SDK
1. You need to decide on these user inputs before running *installVulkanSDK.py*: 
   - The SDK version number you want to install, e.g. `1.0.61.1`.
   - The full path of your Vulkan directory, e.g. `~/Vulkan` or `~/New/Directory/Vulkan`. 
     If the directory/directories does/do not exist, this script will create it/them.
2. Run python script to locally install Vulkan SDK:
   - Run script with command `python3.6 installVulkanSDK.py` to install SDK with no Environment Settings.

_Note_: This Python 3.6 script will install all the prerequisite packages outlined in LunarG's documentation https://vulkan.lunarg.com/doc/view/latest/linux/getting_started.html#user-content-packages before it installs your desired LunarG Vulkan SDK version.

## Runtime Environment Settings
You need to "Set up the runtime environment" as stated in LunarG's Vulkan documentation, e.g. 
`source ~/NewVulkanDirectory/VulkanSDK/1.1.xx.y/setup-env.sh`.  

## Environment Variable Persistence
For the above environment settings to be present at every Ubuntu 18.04 login sessions, you need to open your `.profile` file in your home directory, append `source $HOME/NewVulkanDirectory/VulkanSDK/1.x.yy.z/setup-env.sh` to the file, save `.profile` followed by `source ~/.profile`.

## Motivation
I created this Python 3.6 script to help me install the LunarG Vulkan SDK as its version evolves. I hope it can benefit fellow Vulkan users. Please raise an issue if you notice any correction/improvement is needed. Thanks.   
