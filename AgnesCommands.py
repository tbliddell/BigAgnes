# nextcord
import nextcord
import nextcord.utils
from nextcord.ext import commands

# builtin modules
import random
import json
import pytz
from datetime import timezone
from os import path

# Agnes library imports
import config


class AgnesCommands(commands.Cog):
    """A Cog object that houses and handles user commands.
    Is inherited by Agnes.
    """
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(self, ctx):
        """
        A check function to see if the message author is me.
        For use in the commands.check decorator.
        """
        return ctx.author.id == config.GOD_ID

    @commands.command(hidden=True)
    @commands.has_role('Admin')
    async def printroles(self,ctx):
        """prints a list of your roles."""
        your_id = ctx.author.id
        you = ctx.guild.get_member(your_id)
        await ctx.send(you.roles)
        roles = you.roles
        for _role in roles:
            print(_role)

    @commands.command(hidden=True)
    async def test(self, ctx, arg):
        """Echoes arg back to you. For testing purposes only."""
        await ctx.send(arg)

    @commands.command()
    async def roll(self, ctx):
        """Rolls inputted dice. Syntax is '!roll qdn + x',
        where q is the quantity of dice, n is the number of sides on the die, and x is the modifier.
        Examples of valid syntax are '!roll d20', '!roll 4d6', '!roll 2d8 + 2'."""
        roll = self.bot.utils.dice_roll(ctx.message.content)
        await ctx.message.channel.send(roll)

    @commands.command()
    async def rollchar(self, ctx):
        """
        Generates stats for a DnD character.
        Uses the method of rolling 4d6 and keeping the three highest
        """
        char_rolls = self.bot.utils.roll_char()
        await ctx.send(char_rolls)

    @commands.command()
    async def hello(self, ctx):
        """Hello!"""
        await ctx.send('Henlo!')

    @commands.command(alias=['welcome'])
    async def greet(self, ctx):
        """For welcoming new members to the channel."""
        x = random.randint(5, 50)
        msg = 'WELCOME TO HELL ' * x
        await ctx.send(msg)

    @commands.command()
    async def thank(self, ctx):
        """Not a day goes by..."""
        emoji = '<:thank:592156422150684712>'
        await ctx.message.add_reaction(emoji)
        await ctx.send(f'Not a day goes by that I don\'t thank God that my penis isn\'t on fire. {emoji}')

    @commands.command()
    async def hiskme(self, ctx):
        """Generates and prints a JT Hiskey quote"""
        quote = self.bot.utils.random_from_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\hiskey.txt')
        await ctx.send(quote)

    @commands.command()
    async def tasty(self, ctx):
        """TASTY"""
        await ctx.send(':eye: :tongue: :eye:')

    @commands.command()
    async def mulaneyme(self, ctx):
        """Prints a random John Mulaney quote."""
        quote = self.bot.utils.random_from_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\mulaney.txt')
        await ctx.send(f'{quote}')

    @commands.command()
    async def bandname(self, ctx, *, bandname):
        """
        Records a band name for later big laughs.

        Syntax:
            !bandname <bandname>
        where <bandname> is the bandname you want to add to the list.

        """
        if bandname == '' or bandname == ' ':
            return
        """
        #bandname tweeting is disabled because pointless.
        try:
            if not bandname.startswith('-t'):
                tweet_ok = self.bot.utils.tweet(f'Bandname: {bandname}')
                if tweet_ok:
                    await ctx.message.add_reaction('🐦')
                else:
                    await ctx.send('I\'m not tweeting that.')
        except Exception as e:
            print(f'An error occured while trying to tweet "{bandname}": {e}')
            await ctx.send('Something went wrong trying to tweet that.')
        """
        try:
            with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\bandnames.txt', 'a') as outfile:
                if bandname.startswith('-t'):
                    bandname = bandname[3:]
                outfile.write(f'{bandname}\n')
                await ctx.message.add_reaction('👍')
        except FileNotFoundError:
            print('Could not open bandnames.txt.')
            await ctx.send(config.error_message)
            return

    @commands.command(aliases=['givbandname', 'givebandnam'])
    async def givebandname(self, ctx):
        """Prints a random band name from the list."""
        bandname = self.bot.utils.random_from_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\bandnames.txt')
        await ctx.send(bandname.capitalize())

    @commands.command()
    async def albumname(self, ctx, *, albumname):
        """
        Records and tweets a album name

        Syntax:
            !albumname <albumname>
        where <albumname> is the album name you want to add to the list.

        Note that a message will not be tweeted if it is longer than 280 characters
        or if it contains unallowed words.
        """
        try:
            with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\albumnames.txt', 'a') as outfile:
                if albumname.startswith('-t'):
                    albumname = albumname[3:]
                outfile.write(f'{albumname}\n')
                await ctx.message.add_reaction('👍')
        except FileNotFoundError:
            print('Could not open albumname.txt.')
            await ctx.send(config.error_message)
            return

    @commands.command()
    async def givealbumname(self, ctx):
        """Prints a random album name from the list."""
        albumname = self.bot.utils.random_from_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\albumnames.txt')
        await ctx.send(albumname.capitalize())

    @commands.command()
    async def insultme(self, ctx):
        """Generates and prints a random insult."""
        await ctx.send(self.bot.utils.generate_insult())

    @commands.command()
    async def mock(self, ctx, *, user=None):
        """Syntax: !mock <user>. Mocks the most recent message from user.
        If no user is specified, mocks the most recent message.
        """
        messages = await ctx.channel.history(limit=100).flatten()
        messages = messages[1:]     # excludes the most recent message
                                    # because it is the one invoking the command.
        if user == None:
            await ctx.send(self.bot.utils.mock_str(messages[0].content))
            return
        #if user.startswith('@'):
        #    user = user [1:]
        if user == 'Big Agnes':
            await ctx.send('GOD SHALL NOT BE MOCKED.')
            return
        for msg in messages:
            if msg.author.name == user:
                await ctx.send(self.bot.utils.mock_str(msg.content))
                break
        else:
            await ctx.send(f'User {user} not found.')

    @commands.command()
    async def beemovie(self, ctx):
        """Prints the beemovie script!!!"""
        with open(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\beemovie.txt', 'r') as beemovie:
            line = beemovie.readline()
            await ctx.send(line)

    @commands.command(aliases=['givequot', 'givquote', 'giveqoute', 'giveqote'])
    async def givequote(self, ctx):
        """Prints a random quote from the list."""
        quote = self.bot.utils.getquote()
        await ctx.send(quote)

    @commands.command(hidden=True)
    @commands.has_role('Admin')
    async def getquotebyid(self, ctx, id):
        """Retrieves quote with matching id, if found.
        id must be type int.
        """
        id = int(id)
        quote = self.bot.utils.get_quote_by_id(id)
        await ctx.send(quote)


    @commands.command()
    async def searchquote(self, ctx, *, search_string):
        quotes = self.bot.utils.search_quote(search_string)
        await ctx.send("\n".join(quotes))

    @commands.command(hidden=True)
    #@commands.has_role('Admin')
    async def getquoteinfo(self, ctx, *, quote_text):
        quote_info = self.bot.utils.get_quote_info(quote_text)
        await ctx.send(quote_info)


    @commands.command(aliases=['addquot', 'adquote', 'addqoute', 'addqote'])
    async def addquote(self, ctx, *, quote):
        """
        Records a quote to record for big laughs later.

        Syntax:
            !addquote <Your quote here>

        """
        # twitter handler - disabled due to lack of usefulness.
        """
        try:
            if not quote.startswith('-t'):
                tweet_ok = self.bot.utils.tweet(quote)
                if tweet_ok:
                    await ctx.message.add_reaction('🐦')
                else:
                    await ctx.send('I\'m not tweeting that.')
        except Exception as e:
            print(f'An error occured while trying to tweet the message "{quote}": \n{e}')
            await ctx.send('Something went wrong trying to tweet that.')
        """

        # json handler
        try:
            if quote.startswith('-t'):
                quote = quote[3:]
            dir_path = path.dirname(path.realpath(__file__))
            quote_path = path.join(dir_path, '.\\txt_files\\quotes.json')
            with open(quote_path, 'r') as json_file:
                #data = json.load(json_file)
                # quotes = data['quotes']
                data = json.load(json_file)
                if ctx.guild == None:
                    author = ctx.message.author.name
                else:
                    author = ctx.message.author.nick    # i know this right here is really inelegant, but I'm tired
                    if author == None:
                        author = ctx.message.author.name
                date = ctx.message.created_at
                date_tz = date.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone('US/Mountain')).strftime("%Y-%m-%d %H:%M:%S")
                id = len(data) + 1
                to_add = {'quote': f'{quote}', 'timestamp': f'{date_tz}', 'author': f'{author}', 'id': f'{id}'}
                data.append(to_add)
            self.bot.utils.write_to_json(data, quote_path)
        except Exception as e:
            print(f'Could not addquote because of the following exception: \n{e}')
            await ctx.send(config.error_message)
            return
        await ctx.message.add_reaction('👍')
        print(f'Added quote: {quote}')
        """
        # obsolete txt quote handler
        try:
            if quote.startswith('-t'):
                quote = quote[3:]
            dir_path = path.dirname(path.realpath(__file__))
            quote_path = path.join(dir_path, '.\\txt_files\\quotes.txt')
            self.bot.utils.write_to_file(quote_path, quote)
            await ctx.message.add_reaction('👍')
            print(f'Added quote: {quote}')
        except:
            await ctx.send(config.error_message)
        """

    @commands.command()
    #@commands.has_role('Admin')
    async def editquote(self, ctx, quote_id, new_quote):
        success = self.bot.utils.edit_quote(int(quote_id), new_quote)
        if success:
            await ctx.message.add_reaction('👍')
        else:
            await ctx.send("Something went wrong. Please check your ID and try again.")

    @commands.command()
    async def whosaidthat(self, ctx):
        quote_data = self.bot.utils.last_quote_read
        if quote_data == None:
            return
        if quote_data["author"] == '':
            author = "Unknown"
            timestamp = "Unknown"
        else:
            author = quote_data["author"]
            timestamp = quote_data["timestamp"]
        quote_str = f'Quote number {quote_data["id"]}, \"{quote_data["quote"]}\" was added by {author} at {timestamp}'
        await ctx.send(quote_str)

    @commands.command()
    async def twitter(self, ctx):
        """Prints Agnes' twitter handle and url."""
        await ctx.send('@BigAgnesBot https://twitter.com/BigAgnesBot')

    @commands.command()
    async def whatdidtheycallme(self, ctx):
        """Prints a random thing they called you in high school."""
        name = self.bot.utils.random_from_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\theycalledme.txt')
        await ctx.send(name)

    @commands.command()
    async def theycalledme(self, ctx, *, name):
        """Records a thing that they called you in high school.

        Syntax:
            !theycalledme <name>
        where <name> is the thing you want added to the list.
        """
        try:
            self.bot.utils.write_to_file(r'C:\Users\Tanner\Google Drive\Python\For fun\Discord Bot\txt_files\theycalledme.txt', name)
            await ctx.message.add_reaction('👍')
            print(f'Added that\'s what they called me: {name}')
        except:
            await ctx.send(config.error_message)

    @commands.command(aliases=['givemememe', 'givemem', 'givmeme', 'givemeem'])
    async def givememe(self, ctx):
        """Generates a random meme using meme templates and server quotes."""
        gifs = self.bot.utils.scrape_gifs(n_gifs=20)
        try:
            members = ctx.guild.members
        except AttributeError:
            await ctx.send('This command is only useable in a server text channel.')
            return
        quote = self.bot.utils.getquote()
        await ctx.send(f'{random.choice(members).name}: {quote}\n{random.choice(members).name}: {random.choice(gifs)}')

    @commands.command(name='identifyme', hidden=True)
    @commands.has_role('Admin')
    async def __identifyme(self, ctx):
        """Admin command. Returns user name and ID."""
        await ctx.send(f'you are: {ctx.message.author}, ID: {ctx.message.author.id}')

    @commands.command(name='identifyall', hidden=True)
    @commands.has_role('Admin')
    async def __identifyall(self, ctx):
        """Admin commands. Returns usernames and IDs for all users in ctx."""
        for user in ctx.message.channel.members:
            await ctx.send(f'{user.name}: {user.id}')