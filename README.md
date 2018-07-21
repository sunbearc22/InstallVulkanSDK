# InstallVulkanSDK
Bash script to install LunarG's Vulkan SDK.

Tested on Ubuntu 16.04.3 with linux kernel 4.10.0-42-generic, 4.10.0-38-generic, and 4.10.0-33-generic.

Works with SDK versions:
  
  `1.1.77.0`  `1.1.73.0`  `1.1.70.0`
  
  `1.0.68.0`  `1.0.65.0`  `1.0.61.0`  `1.0.57.0`  `1.0.54.0`  `1.0.51.0`  `1.0.49.0`   `1.0.46.0`   `1.0.42.2`   `1.0.39.1`   `1.0.39.0`               
  

## Preliminaries
1. Download `InstallVulkanSDK` to your Ubuntu system.
2. Goto `InstallVulkanSDK` directory with command `cd ~/InstallVulkanSDK/directory/name`.
3. Make script executable with command `chmod ugo+x installVulkanSDK`.
4. All System Requirements and Packages outlined by LunarG have to be satisfied https://vulkan.lunarg.com/doc/view/latest/linux/getting_started.html#user-content-packages

## Install LunarG's Vulkan SDK
1. You need to decide on these user inputs before sourcing *installVulkanSDK*: 
   - The SDK version number you want to install, e.g. `1.0.61.1`.
   - The full path of your Vulkan directory, e.g. `~/Vulkan` or `~/New/Directory/Vulkan`. 
     If the directory/directories does/do not exist, the script will create it/them.
2. Source script with command `source installVulkanSDK`.

_Note: This bash scipt will install LunarG Vulkan SDK, as well as builds it's examples, samples and tools, and also performs via. 
      The entire building process can take a bit of time so you need to have some patience. 2 to 3 minutes on my system. 
      It can take longer when internet download speed and/or CPU speed slows._

## Runtime Environment Settings
During installation, three new environment variables `VULKAN_SDK`, `LD_LIBRARY_PATH`, `VK_LAYER_PATH` will be created to your environment. These are described in LunarG VulkanSDK documentation. In addition, `VULKAN_SDK` will be appended to your system's `PATH` environment variable each time you run this script. 

**Note:** _In the event this script is executed multiple times, there will be multiple_ `VULKAN_SDK` _paths added to_ `PATH`. _I have not included an alogorithm to avoid this situation. You have to use bash_ `export` _ command to ensure only one_ `VULKAN_SDK` _path appears in_ `PATH`.**

## Environment Variable Persistence
Per LunarG Vulkan SDK documentation, you can `source` the `setup-env.sh` file that is provided in the LunarG Vulkan SDK in your `.profle` file. Example, you can append this statement to `.profile`:

`source $HOME/NewVulkanDirectory/VulkanSDK/1.x.yy.z/setup-env.sh`

## Motivation
I created this script to help me install the LunarG Vulkan SDK as its version evolves. Hope it can benefit fellow Vulkan users. Please alert me of needed corrections/improvements when you encounter them. Thanks.   
