# gameBot
This bot can be trained to recognize items and perform task in a game.
In my case, I trained it to recognize trees, check if they can be cut down, do so if possible and wait for action to be finished before repeating.
If no more trees were available, the bot would then look for an exit.

Since this was for an online game, I introduced random pauses and misclicks to avoid getting flagged.

I used the pyautogui library to find the images on the screen, the win32api, win32con to allow mouse event and os/os.path to save and locate training images on my computer.

For the script to work, your project needs the following directory:

theBot.py
itemA -> itemA1.png, itemA2.png, ...
itemB -> itemB1.png, itemB2.png, ...

Some thoughts on the project:

- Although I do not know which algorythms are used by autogui to search for an image in the given area, the fact that we can specify the alpha level (or uncertainty) means we can have some control on the type one and type two error.
- Assuming we only have one training image of our item, low alpha means that small variation in the item will result in not recognizing it (type 1) while large alpha means potentially matching with the wrong items (type 2). 
- If you have multiple training images, then you can have a higher alpha per verification. The probability that the item is not on the screen becomes alpha to power of n where n is the number match between what's on screen and our training images.
- Finally trying to match the full item results in slower analysis (more information to process) and high type 1 error (background, orientation, superposition,...). On the other hand, breaking an item down into its components reduces noise in data and the size of the array used by pyautogui.
