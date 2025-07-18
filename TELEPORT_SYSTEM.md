# Enhanced Teleport System

## Overview

This Lua script provides an enhanced teleport system for 3v3 and 5v5 game modes with anti-cheat protection. The system uses slower, more natural movement patterns to avoid detection by anti-cheat systems.

## Features

### ✅ Anti-Cheat Protection
- **Configurable delays** between teleports (1-10 seconds)
- **Waypoint-based movement** instead of direct teleportation
- **Randomization** to appear more human-like
- **Safety checks** to prevent rapid consecutive teleports

### ⚙️ Configurable Settings
- Teleport delay adjustment
- Waypoint usage toggle
- Movement randomization toggle
- Auto-win system enable/disable

### 🎮 Game Mode Support
- **3v3 Mode**: Optimized teleport sequence for 3v3 matches
- **5v5 Mode**: Extended sequence for 5v5 matches with longer delays
- **Automatic detection**: Can detect current game mode

## Usage

### Basic Functions

```lua
-- Enable/disable the auto-win system
setAutoWinEnabled(true)  -- Enable
setAutoWinEnabled(false) -- Disable

-- Adjust teleport speed (1-10 seconds)
setTeleportDelay(5)  -- 5 second delay between teleports

-- Configure movement options
setUseWaypoints(true)        -- Use waypoints for natural movement
setRandomizeMovement(true)   -- Add randomization

-- Start auto-win sequence
performAutoWinTeleport()     -- Automatically detects game mode

-- Manual mode-specific teleport
doTeleport3v3()             -- Force 3v3 teleport sequence
doTeleport5v5()             -- Force 5v5 teleport sequence

-- Emergency stop
emergencyStop()             -- Immediately disable auto-win system
```

### Configuration Management

```lua
-- Save current settings
saveConfig()

-- Load saved settings
loadConfig()

-- Check current configuration
local config = getConfigurationStatus()
for key, value in pairs(config) do
    print(key .. ": " .. tostring(value))
end

-- Get system status
local status = getSystemStatus()
```

### Game Mode Management

```lua
-- Set game mode manually
setGameMode("3v3")
setGameMode("5v5")

-- Detect current game mode (automatic)
local mode = detectGameMode()
```

## Configuration Options

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| `teleportDelay` | 1-10 seconds | 3 | Delay between major teleport positions |
| `useWaypoints` | true/false | true | Use multiple waypoints for natural movement |
| `randomizeMovement` | true/false | true | Add random offsets to positions |
| `waypointCount` | 1-5 | 3 | Number of waypoints between positions |
| `randomOffset` | 1-10 | 5 | Maximum random position offset |

## Safety Features

### Anti-Cheat Protection
- **Minimum delay enforcement**: Prevents teleports faster than configured delay
- **Waypoint movement**: Simulates natural player movement patterns
- **Randomization**: Adds human-like unpredictability
- **Cooldown system**: Tracks time between teleports

### Safety Checks
- **Auto-win toggle**: Master switch to enable/disable entire system
- **Game mode validation**: Only works in supported modes
- **Emergency stop**: Immediate shutdown capability
- **Configuration validation**: Ensures settings are within safe ranges

## Installation

1. Place `pasted.txt` in your game directory
2. Load the script: `dofile("pasted.txt")`
3. The system will initialize automatically
4. Configure settings as needed
5. Enable auto-win when ready: `setAutoWinEnabled(true)`

## Example Usage

```lua
-- Load the script
dofile("pasted.txt")

-- Configure for safer operation
setTeleportDelay(5)          -- 5 second delays
setUseWaypoints(true)        -- Use waypoints
setRandomizeMovement(true)   -- Add randomization

-- Enable and start
setAutoWinEnabled(true)
performAutoWinTeleport()

-- If needed, emergency stop
emergencyStop()
```

## Testing

A test script is provided to verify functionality:

```bash
lua5.3 test_teleport_system.lua
```

This will test all functions and verify the system is working correctly.

## Notes

- **Game Integration**: The current implementation uses placeholder functions for game integration. Replace teleport and position functions with actual game API calls.
- **Coordinates**: Update target positions in `doTeleport3v3()` and `doTeleport5v5()` with actual game coordinates.
- **Performance**: The system is designed to be lightweight and efficient.
- **Compatibility**: Written in Lua 5.3, compatible with most Lua environments.

## Troubleshooting

### Common Issues

1. **"Teleport on cooldown"**: Wait for the configured delay or check `lastTeleportTime`
2. **"Auto-win system is disabled"**: Enable with `setAutoWinEnabled(true)`
3. **"Not in 3v3/5v5 mode"**: Set game mode manually or check detection logic
4. **Invalid delay**: Ensure delay is between 1-10 seconds

### Debug Information

```lua
-- Check system status
local status = getSystemStatus()
print("System enabled:", status.systemEnabled)
print("Game mode:", status.gameMode)
print("Time since last teleport:", status.timeSinceLastTeleport)
```

## Changelog

### v1.0.0 (Current)
- Initial implementation with anti-cheat protection
- Configurable delays and waypoint system
- 3v3 and 5v5 mode support
- Safety checks and emergency stop
- Configuration save/load system
- Comprehensive testing suite

---

**⚠️ Disclaimer**: This script is for educational purposes. Users are responsible for compliance with game terms of service and anti-cheat policies.