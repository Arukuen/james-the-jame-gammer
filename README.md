# james-the-jame-gammer

To setup in a discord server, make sure to configure the integration for each of the commands, that is, they can only be accessed by a permitted role.

To host the app in your local machine:
1. Create a .env file containing the following.:
```
DISCORD_TOKEN = [YOUR DISCORD TOKEN]
```
2. Run main.py

---

### Commands:
1. `/set_config` - Set the configuration for the bot. The `channel` is where the bot will post the reminders and `jammer` is the role which will be pinged. Should only be accessible to jam organizers.

2. `/create jam` - Create a new game jam reminder with `title`, `theme`, `duration`, and `date` of the ***end of the jam***. The reminders will be set based on the `duration` (look up with config in database) and the end `date`. Should only be accessible to jam organizers.

3. `/timeleft` - Messages the time left for jam.

4. `/theme` - Messages the theme of the jam.

5. `/list` - Messages the list of jams.

6. `/reset` - Resets the bot. Should only be accessible to jam organizers.

---

### How to use the bot:
1. Assuming the bot is already hosted and runs in the discord server, setup the ***integration*** to allow the  commands `/set_config`, `/create jam`, and `/reset` to be accessed only by the game jam organizers.

![Setting up the integration](/assets/readme1.png)

2. Use the `/set_config` command to set ***channel*** and the ***jammer*** role.

![Example of set_config](/assets/readme2.png)

3. Use the `/create_jam` command to create a new game jam. Note that the `year`, `month`, `day`, `hour`, and `minute` pertains to the date for the end of the jam. As for the initial configuration for the `duration`, the bot will remind in the following ***time*** before the end of the jam:
   * 2 days: 1 day, 12 hours, 6 hours, 1 hour
   * 1 week: 3 days, 1 day, 12 hours, 6 hours, 1 hour
   * 2 weeks: 1 week, 3 days, 1 day, 12 hours, 6 hours, 1 hour
   
![Example of create_jam](/assets/readme3.png)
   * In the example, the start of the jam is 2023/3/25 23:59, since the `duration` is 2 days and the `end of the jam` supplied is 2023/3/27 23:59.

4. The game jam is now created and automatically started. Everyone in the server can use the `/timeleft` and `/theme` to check the information.