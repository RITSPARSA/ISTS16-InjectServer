# ISTS16 Inject Manager

Email client for managing injects.

This client achieves two things:
1. Listen for new inject submissions and autoreply.
2. Download all submitted injects and save them for whiteteam.

Injects will be submitted with a correctly formatted subject line.

If the inject is an on-time submission, the team will be sent a 
verification email and the next inject in the inject path.

If the inject is not on time, the team will get notified that the 
inject is not on time and that it will not be graded.

If the inject does not follow the correct format, the team will receive
an email informing them to resubmit.
