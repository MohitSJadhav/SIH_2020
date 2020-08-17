# SIH_2020
Slide 1:
According to the global data, almost 4 out of 100 people are visually impaired.
    • Around 285 million people in the world are visually impaired out of which 62 million are Indians.

Why Captcha?
Everyday life of majority of the population in the world revolves around Internet. The utmost need is to provide security to the user’s data and prevent the bots from automatically submitting forms with spam or other unwanted content. To avoid this, captchas are developed.

What is a Captcha?
A CAPTCHA is a type of challenge–response test used in computing to determine whether or not the user is human. 
Different types of captchas include:
    1. Simple Math problem
    2. No captcha recaptcha
    3. Time based 
    4. Audio
    5. Invisible
    6. Picture identification
    7. Social media sign in
When it comes to visually impaired people, they use audio captcha for accessing any protected resource.

Slide 2: Flaws in the existing captcha authentication system

 reCaptcha works with screen readers like JAWS. Whenever visually impaired person tries to access a protected resource or submit a form, he is asked to solve an audio captcha. The audio instruction is not easy to decipher because of the background noise added to it. The user is expected to type what he hears in the audio instruction and verify. Depending on whether or not the typed words/numbers match with the audio instruction, the access will be provided to the visually impaired user. Moreover, the audio instruction is provided in English.

hCaptcha is a drop-in replacement for reCAPTCHA. It has no option for audio captcha, this proves to be a major problem for visually impaired people.

To summarize, captchas are inaccessible because:
    1. Many websites don’t have an option of audio captcha for visually impaired users.
    2. The websites that have an option of audio captcha provide audio instructions only in English, thus reducing the accessibility.
    3. The audio instruction cannot be easily deciphered due to background noise in the audio and randomness of words.
    4. System security is compromised mainly because some of the audio captchas allow authentication with partially correct CAPTCHA words.

Slide 3: Idea/Approach:

According to our survey conducted at a blind school and some research on the capabilities of visually impaired people, we came to a conclusion that some generic, simple yet efficient system, devoid of language barrier is needed, which will be largely accessible.
Visually impaired people of all age groups know basic shapes like circle, triangle, rectangle, diamond, given, they have the ability to feel things. This very ability eliminates the difference between a normal user and visually impaired user. 
When we visited blind school, we asked the students whether they are comfortable in recognizing basic shapes. They not only knew the basic shapes but were also able to draw them in tools such as Paint. We closely observed the time required for them to draw the shapes and noted it down. We repeated the same process with the staff in the school, who was visually impaired as well. We found out that they also responded correctly by drawing the instructed shapes. We explained our system to them and they found it comparatively much easier than the existing captcha authentication system. They were relieved by the fact that our system doesn’t have language barriers.
On the basis of the capabilities of the students and staff members to draw different shapes, we came up with our dataset, and also specified a time limit for drawing the shape, taking our survey into consideration.



Slide 4:Working of the system:

    1. When user tries to access a protected resource, he will be asked to choose a language of audio instruction of his choice.
    2. A canvas will pop up on the browser window.
    3. An audio instruction will be played in the user preferred language.
    4. The audio will basically be an instruction with a user friendly noise (example: chirping of birds, nature sounds, etc) for security purpose, and will ask the user to draw a particular shape.
    5. Canvas will cover the maximum browser area in order to allow the user to freely draw the shape specified in the audio instruction.
    6. A timer will start as soon as the audio instruction ends to ensure security.
    7. If the user draws the instructed shape within the specified time limit, he will have to click on the submit button, the shape drawn will be authenticated by a trained model of image classifier.
    8. If the shape drawn is correct, and as specified in the audio instruction, user will get a message that captcha has been authenticated successfully, and will be redirected to the dashboard. If the shape drawn by the user is found to be incorrect, he will get a message that Captcha authentication has failed and will be redirected to the login page where he will have to go through the authentication process again.
    9. In case, the user is not able to draw the instructed shape within the specified time limit, the system will auto-submit the shape drawn by user and will 
repeat the step 8 depending on whether the user-drawn       shape is correct or not.

Slide 5: Keynotes:
    • Language barrier eliminated
    • Platform independent with the help of responsive canvas. It can be used efficiently on smart phones and laptops.
    • User friendly noise in the audio instruction
    • Generic system (visually impaired people and normal users can use the system simultaneously)
    • Cost effective because of the fact that no extra hardware installation is required
    • Increased security, because of time constraint given to draw the instructed shape.

To execute this project on your system:
1.execute requirements.txt first.
2.exectue shapefinal.py.
