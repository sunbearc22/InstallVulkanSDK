# InstallVulkanSDK
Bash script to install LunarG's Vulkan SDK.

Tested on Ubuntu 16.04.3 with linux kernel 4.10.0-33-generic and 4.10.0-38-generic.

## Preliminaries
1. Download InstallVulkanSDK to your Ubuntu system.
2. Goto InstallVulkanSDK directory with command `cd ~/InstallVulkanSDK/directory/name`.
3. Make script executable with command `chmod ugo+x installVulkanSDK`.

## Install LunarG's Vulkan SDK
1. You need to decide on these user inputs before running *installVulkanSDK*: 
   - The SDK version number you want to install, e.g. `1.0.61.1`.
   - The full path of your Vulkan directory, e.g. `~/Vulkan` or `~/New/Directory/Vulkan`. If the directory/directories does/do not exist, the script will create it/them.
2. Run script with command `./installVulkanSDK`.

Note: Version uploaded on 2017-11-3 installs the SDK, builds the examples, samples and tools and also performs via. 
      The entire building process can take a bit of time so you need to have some patience.   
      
