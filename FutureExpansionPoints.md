FutureExpansionPoints

-----

P0
------
Work end to end for an app. Hinge to start with 
- Fix the analysis results, right now its defaulting to 5 - most likely because of errors during parsing.
- Create a setting to allows allow [or always reject] - in case people are desperate and want to sent request to everyone, especially for people with premium
- Add net time taken for a single profile evaluation
- Need to scroll horizontally so that i can fetch the entire content of Hinge's screen. Especially the drinks, smoke etc section
- Right now execution stops after crossing out a profile, it should continue till limit of profiles reached for the day
- Get scrcpy to work across networks , and in other devices by using the solution in this issue : "https://github.com/Genymobile/scrcpy/issues/5794"

- Also chat with people already in match list
- Notify user when the user is ready for a date
- Suggest places nearby - activities based on match's interest ( activities / dinner )
- Remove duplicate screenshots before sending them to AI for analysis
- Before each run, 
    - Clear screenshots_from_last_run folder
    - Move all images in screenshots folder to screenshots_from_last_run folder 
    - Clear the screenshots folder
- Short circuit[just like humans] : Analyse the first screenshot before proceeding to full analysis. If the image is anything that the client is not looking for, click on cross and move to next profile, this saves time that would have otherwise gone in a full profile analysis
- Human based swiping actions 
    - to prevent getting bot banned
    - not a straight line
    - add varying speed of scroll and varying delay between scrolls
- Implement error handling
- Fix the lcoation for before and after location of screenshot so that , debugging is easier. And they are cleaned up only at the beginning of a new run, not during a run

P1
-------
- Identify the exact girl to which the profile belongs - sometimes, girls can have multiple people in their profile pictures - potentially skewing results
- Clicking on a specific picture rather than the last one
- Clicks Works for dynamic window placement, Right now it works for hardcoded values based on the assumption that the window will open at a certain specific place on my desktop. Snippets:
    - Cross button: physical device screen coordinates: (X,Y) : (180,2600)
    - [Physical device screen coordinates: (X,Y) : (1190,2300)- map this to relative coordinates based on the scrcpy window placement]
-------
Work with other apps like bumble etc
