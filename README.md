# MeatuchuRPGMapMaker
This is a work-in-progress Python application that, when complete, will be able to export layered maps for tabletop role-playing games (TTRPGs) with verticality in mind. Additional features will include exporting a scene compatible with [FoundryVTT](https://foundryvtt.com/) and the [Levels](https://foundryvtt.com/packages/levels) module.

## Project Structure
The project is organized into several directories:

- `MeatuchuRPGMapMaker/`
  - Contains the main application code, including classes, core classes, events, exceptions, game logic, helpers, and keybinds.
- `tests/`
  - Contains unit tests for the application.
- `resources/` (Ignored by Git)
  - Contains various resources used by the application.
- `logs/:` (Ignored by Git)
  - Contains log files generated by the application.

## Key Classes and Events

### `FeatureManager`
Base class for Manager classes, which have direct responsibilities and communicate with each other using `Events`
### `AppManager`
Backbone of the application. Initializes all other managers, and informs them of one another. Contains a loop which controls the rate at which the other managers perform input/update/renderr steps
### `EventManager`
The EventManager is the line of communication between all other classes. Every manager class has the EventManager injected after they are initialized. First, the FeatureManagers inform the EventManager which Events they would like to subscribe to and what functions to run when the events are processed. Then, they can construct and queue events to the EventManager as needed. When an event is processed, the Event manager passes that event to each of its subscribers in first-in-first-out order.

### `Events`
These classes are packets of data that can be sent to the EventManager and used to send messages to other areas of the codebase without directly invoking them. For example, the `FullScreenKB` keybind can fire a `WindowToggleFullscreenModeRequestEvent`, which, when processed, will be recieved by the WindowManager, which will handle the request as it likes. This allows for fully configureable responses to specific requests which are located in logical places in the codebase.

### Running the Application
You can run the application by executing the run script in the root directory of the project.

### Testing
Unit tests are located in the tests/ directory. You can run them using your preferred Python testing framework.

### Debugging
The project is configured for debugging with the Debugpy extension in Visual Studio Code. The configuration is located in `.vscode/launch.json.`