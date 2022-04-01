# rando-setup-checker

An application that runs various checks to help verify that KH2 Randomizer is correctly set up.

This may get incorporated into the seed generator application someday as part of the first-time setup process.

### Instructions

* Open the application
* Choose your platform
* Fill in the location(s) requested
* Click "Check Configuration" to run the checks

### Checks Performed (PC)

* Mods Manager Bridge location
  * Verifies the Mods Manager Bridge executable is found and configured
* Game Install location
  * Verifies the KH2 game executable is found
  * Verifies the LuaBackend Hook DLL is found
* OpenKH location
  * Verifies the OpenKH Mods Manager executable is found and configured
  * Verifies the extracted game data locations match between OpenKH Mods Manager and Mods Manager Bridge
  * Verifies that at least one mod is found, and lists each mod found
* Games Extract location
  * Verifies that the extracted KH2 data location is found and contains KH2 data
* Patches location
  * Verifies the patch location is found if configured, and lists each patch found there
* Lua scripts
  * Verifies that the Lua scripts location is found
  * Verifies that at least one Lua script exists, and lists each script found

### Checks Performed (PCSX2)

* OpenKH location
  * Verifies the OpenKH Mods Manager executable is found and configured
  * Verifies that at least one mod is found, and lists each mod found
* Games Extract location
  * Verifies that the extracted KH2 data location is found and contains KH2 data
* Cheats location
  * Verifies that the cheats location is found
  * Verifies that at least one pnach file exists, and lists each pnach file found
