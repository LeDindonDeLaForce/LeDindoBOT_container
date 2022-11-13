# LeDindoBOT

Fork of LeixBOT created by Leix/Leochely.

## Installation

Edit the .env file with the following variables and format:

```
ACCESS_TOKEN=bot_token
CLIENT_SECRET=channel_token
BOT_PREFIX=!
CHANNEL=your_twitch_channel[stream, not bot]
INITIAL_CHANNELS=your_twitch_channel[stream, not bot]
```

To generate the access token, go to the twitch [token generator](https://twitchtokengenerator.com/), login as your **bot account** and select "bot chat token".
To generate the channel access token, go to the [token generator](https://twitchtokengenerator.com/), login as your **own account** and choose "custom scope token". Select all the permissions and generate the token.

Here are provided the Dockerfile to create the custom BOT image.
This code is compatible with docker and podman HOWEVER I recommend to use podman for security reasons.

Debian/Ubuntu : 
```
apt install -y podman
```

RedHat/CentOS/Rocky/Alma...:
```
yum install -y podman
```

SUSE/openSUSE :
```
zypper install podman
```


Then as a non root and NON SUDO user, create your mysql container with your own parameters:
```
podman run --name=bot_mysql -d -p Your_MySQL_Port:3306 -v mysql_bot:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=CreateRootPassword \
-e MYSQL_USER=CreateUserName \
-e MYSQL_PASSWORD=CreateUserPassword \
-e MYSQL_DATABASE=CreateDatabase  \
mysql:8.0.31-oracle
```

Let's build your database :

Debian/Ubuntu : 
```
apt install -y mysql-client
```

RedHat/CentOS/Rocky/Alma...:
```
yum install -y mysql
```


SUSE/openSUSE :
```
zypper install mysql
```

Then:

```
cd /your/directory/image_docker
mysql YourDatabaseName --host=YourIP --port=YourPort --user=root -p < TWITCH_BOT.sql


### Caution : "YourIP" cannot be "localhost" or "127.0.0.1" even if it is the same machine
```



Now edit the Python file custom_commands.py
```
params = {
    'user':'Put Your DB user',
    'password':'Put your DB password',
    'host':'127.0.0.1',         ###Keep addr 127.0.0.1 we will see it later
    'port':3306,                ###Keep port 3306, it's inside container POV, not external
    'database':'Your Database Name'
}
```

Now edit the python file cogs/misc.py
Go to https://www.blagues-api.fr/, login with your Discord account and get a token, paste it in the 'blagues=BlaguesAPI' parameter (remove spaces)
```
    @commands.command(name="blague")
    async def blagueapi(self, ctx: commands.Context):
        blagues=BlaguesAPI("***Token_Blagues-API***") #token a récupérer sur https://www.blagues-api.fr/
        rep = await blagues.random(disallow=[BlagueType.DARK,BlagueType.LIMIT,BlagueType.BEAUF])
        await ctx.send("[" + rep.type.capitalize() + "] : " + rep.joke)
        await asyncio.sleep(3)
        await ctx.send(rep.answer + " Kappa")
```





Now create the volume which will host the Twitch BOT python files (stored in BOT_DIR)
```
cd ..
podman volume create Your_Bot_Volume
cp -rp BOT_DIR/* ~/.local/share/containers/storage/volumes/Your_Bot_Volume/_data/
cp -rp BOT_DIR/.env ~/.local/share/containers/storage/volumes/Your_Bot_Volume/_data/
chmod 755 ~/.local/share/containers/storage/volumes/Your_Bot_Volume/_data/*
chmod 444 ~/.local/share/containers/storage/volumes/Your_Bot_Volume/_data/.env
chmod 700 ~/
```

Go to the image_docker directory and build your image with your name and your tag:
```
cd image_docker
podman build . < Dockerfile --tag=YourImageName:YourTag
```

Now launch the BOT container:

```
podman run --name=YourBotContainerName -d -v Your_Bot_Volume:/BOT_DIR YourImageName:YourTag
```





At this step, the bot will start to interact with yout channel chat but he nas not access to database yet. Let's create a containers pod

```
podman generate kube -f YourPodFileName.yaml bot_mysql YourBotContainerName 
## With bot_mysql : the name given to the mysql container on podman run command
## With YourBotContainerName : the name given to the bot container on podman run command
```


Now stop and delete the containers, they will be recreated with the pod and will be automatically linked like a unique host.
```
podman stop bot_mysql YourBotContainerName
podman rm bot_mysql YourBotContainerName
podman play kube YourPodFileName.yaml
```


Now the bot installation is complete. Let's make it as a service to keep the pod up
```
systemctl --user --now enable podman
cd ~/.config/systemd/user/
podman pod ls ### Get the POD ID corresponding to the Twitch BOT; we will name it "POD_ID"
podman generate systemd --files --name POD_ID
### A file pod-******.service and some files container-*****.service will be created.


podman stop POD ID
systemctl --user enable --now pod-******.service   ###Enable only the pod service, not containers.
```

Finally, as ROOT user perform the following command:
```
loginctl enable-linger YourNonSudoUser
```



Bot installation and configuration is now complete
