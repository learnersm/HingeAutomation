Steps
1. Run scrcpy in a terminal
2. Identify the open window
3. Understand the dimensions of the open window
4. Click on the Hinge app to open the hinge app
5. Wait for the first profile to load
6. Once a profile has loaded we will take preliminary steps to be able to understand the profile first
- Take the first screenshot
- Now scroll sufficiently so that what you see on screen is new content , that is non overlapping with the previous screenshot
- Take the next screenshot, continue doing this until you reach the end of the profile and cannot scroll any further
7. Now use the screenshots that represent her profile as an input and rate the girl
- Note that we need to Identify the girl who's profile picture it is. Many a times girls can have group pictures making it hard to identify the actual girl. Given you have all the screenshots of the profile, you should be able to pinpoint the girl. For this step, just provide the screenshots to the LLM layer and ask it the required questions.
- Now rate the girl on a scale of 1 to 10.
8. Perform action on the profile, use the LLM layer to find the required buttons to click
- In case the rating is < 7 , move to the next profile. i.e. click on cross. Repeat steps for the next profile
- In case the rating is >= 7, then click on like/heart button that you see
    - [In case we clicked like] Then analyse all the text in the profile and the images in the profile and create an understanding about the girl
    - Now create a witty comment (under 150 characters) to spark her interest based on your understanding of the girl, and reply to the first photo in the profile
    - After clicking on the heart icon, you will see a box saying add a comment
    - Click on the box
    - Paste your crafted comment in this box. 
    - after writing your comment in the box, Minimise the open keyboard dialog box
    - Click on "send like"
    - This will now show the next profile on the screen
- Repeat



Notes
-----
- Before exiting application, or in case of an error, stop the running terminal for scrcpy
- The open Device window is an emulation of an actual physical mobile device connected via usb
- You can perform interactions as you would with a phone : click, swipe in different directions, type via keyboard
- Do not delete anything , ever , while performing the operations
- Take screenshots after performing an action to understand how the device reacts to your input
    - In case the device reacts in an expected fashion move to the next step, else try another approach
    - Note the path where the screenshot is saved and use that path correctly when analysing screenshots
- If at anypoint of time, you get a message indicating that we cannot view more profiles: log the fact "Limit of daily profiles reached" and play a sound indicating completion of program
- 
- 
