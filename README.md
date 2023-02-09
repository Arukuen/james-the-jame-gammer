# james-the-jame-gammer

To setup in a discord server, make sure to configure the integration for each of the commands, that is, they can only be accessed by a permitted role.

To host the app in your local machine:
1. Create a .env file containing the following.:
```
DISCORD_TOKEN = [YOUR DISCORD TOKEN]
```
2. Run main.py

---

Commands:
1. `/set_config` - Set the configuration for the bot. The `channel` is where the bot will post the reminders and `jammer` is the role which will be pinged. Should only be accessible to jam organizers.

2. `/create jam` - Create a new game jam reminder with `title`, `theme`, `duration`, and `date` of the end of the jam. The reminders will be set based on the `duration` (look up with config in database) and the end `date`. Should only be accessible to jam organizers.

3. `/timeleft` - Messages the time left for jam.

4. `/theme` - Messages the theme of the jam.

5. `/list` - Messages the list of jams.

6. `/reset` - Resets the bot. Should only be accessible to jam organizers.
