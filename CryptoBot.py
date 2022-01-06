import os
import CheckPrices
import asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix='!')
'''
alert_thresholds is a dictionary that should look like this:    
    {'ctx':the context of the last alert set, 'coin':['minprice', 'maxprice', booleantostartorstopalerts]}
'''
alert_thresholds = {'ctx': None}
    
@client.event
async def on_ready():
    """Starts the bot and begins the background task.

    """
    check_alert_prices.start()
    print("CryptoBot has connected to Discord!")



@tasks.loop(seconds=15)
async def check_alert_prices():
    """A background task that checks the prices and sends an alert to a channel.

    """
    print("background task")
    for k in alert_thresholds:
        if (k == 'ctx'):
            continue
        alert = price_alert(k)
        if alert != "False" and alert != "":
            print(alert)
            await alert_thresholds['ctx'].send(alert)


def price_alert(coin_name):
    """Checks the current price of a cryptocurrency and returns an alert based on the user set
        min and max values

    Parameters
    ----------
    coin_name : str
        The coin to get the price for

    Returns
    -------
    string
        a string of the alert message to be sent
    """
    alert = ""
    if alert_thresholds[coin_name][2] == False:
        return "False"
    min_price = alert_thresholds[coin_name][0]
    max_price = alert_thresholds[coin_name][1]
    current_price = CheckPrices.get_crypto_price(CheckPrices.search_coin(coin_name))
    if min_price > 0 and current_price < min_price:
        alert =  f"{coin_name} is below the alert minimum of ${min_price} at ${current_price}!"
        alert_thresholds[coin_name][0] = current_price
        
    if max_price > 0 and current_price > max_price:
            alert =  f"{coin_name} is above the alert maximum of ${max_price} at ${current_price}!"
            alert_thresholds[coin_name][1] = current_price
            
    return alert

async def replace_alert(c, symb, min_price, max_price):
    """Allows user to replace one alert when the alert dictionary gets "full".

    Parameters
    ----------
    c : discord object
        the context from the previous command
    symb : str
        the symbol of the cryptocurrency
    min_price : float
        the minimum price for the replacement coin
    max_price : float
        the maximum price for the replacement coin

    """
    await show_alerts(c)
    def check_msg(msg):
        return msg.author == c.author and msg.channel == c.channel and (msg.content in alert_thresholds or msg.content.lower() == "exit")
    try:
        await c.send("Which cryptocurrency alert would you like to replace? Enter the symbol of the coin or reply 'exit' if you changed your mind.")
        msg = await client.wait_for("message", check=check_msg,timeout=25)
        print(msg.content)
        if msg.content == "exit":
            await c.send("Replacement ceased.")
            return
        del alert_thresholds[msg.content]
        alert_thresholds[symb] = [min_price, max_price, True]
        await c.send(f"Replaced {msg.content} for an alert for {symb} with min of {min_price} and max of {max_price}!")
        print(alert_thresholds)
        
    except asyncio.TimeoutError:
        await c.send("You did not reply on time, replacement will not occur.")
    
@client.command(name="price")
async def curr_price(ctx, coin_name):
    """Gets the current price of the given coin.

    Parameters
    ----------
    ctx : discord object
        the context of the command
    coin_name : str
        the name of the coin

    """
    await ctx.send(CheckPrices.get_crypto_price(CheckPrices.search_coin(coin_name)))




@client.command(name="showmyalerts")
async def show_alerts(ctx):
    """Gets all of the currencies in the alert dictionary and sends them to the channel it was
        called in.

    Parameters
    ----------
    ctx : str
        the context of the command

    Returns
    -------
    str
        a string of the alert message to be sent
    """
    dict_str = ""
    for key in alert_thresholds:
        if key == "ctx":
            continue
        val = alert_thresholds[key]
        dict_str += f"{key}  :  Max threshold:  {val[0]} || Min threshold:  {val[1]} || Active?  {val[2]} \n"
    await ctx.send(dict_str)

@client.command(name="setalert")
async def set_alert(ctx, coin_name, min_price, max_price):
    """Sets an alert for a crypto with a min and max threshold, if the 

    Parameters
    ----------
    ctx : discord object
        the context of the command
    coin : str
        the name of the cryptocurrency
    min_price : float
        the minimum price for the replacement coin
    max_price : float
        the maximum price for the replacement coin

    """
    coin_dict = CheckPrices.search_coin(coin_name)
    try:
        min_price = float(min_price)
        max_price = float(max_price)
        symb = coin_dict["symbol"]
        if len(alert_thresholds) == 5:
            await ctx.send("You can only track four currencies at a time, would you like to replace one? (reply y or n)")
            def check_msg(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y', 'n', 'yes', 'no']
            reply = await client.wait_for("message", check=check_msg)
            if reply.content.lower() == 'y' or reply.content.lower() == 'yes':
                await replace_alert(ctx, symb, min_price, max_price)
                return
            else:
                return 
        alert_thresholds[symb] = [min_price, max_price, True]
        await ctx.send(f"Alert for {symb} set with min of {min_price} and max of {max_price}!")
        alert_thresholds['ctx'] = ctx
        print(alert_thresholds)
        return
        
    except TypeError:
        await ctx.send(f"{coin_name} was not found")

@client.command(name="turnoff")
async def turnoff_alert(ctx, coin_symb):
    """Turns off an alert and sends a message back to the channel.

    Parameters
    ----------
    ctx : discord object
        the context from the previous command
    coin_symb : str
        the symbol of the cryptocurrency
   
    """
    try:
        alert_thresholds[coin_symb][2] = False
        await ctx.send(f"{coin_symb} alerts turned off")
    except:
        await ctx.send(f"{coin_symb} was not found")

@client.command(name="turnon")
async def turnon_alert(ctx, coin_symb):
    """Turns on an alert and sends a message to the channel.

    Parameters
    ----------
    ctx : discord object
        the context from the previous command
    coin_symb : str
        the symbol of the cryptocurrency
   
    """
    try:
        alert_thresholds[coin_symb][2] = True
        await ctx.send(f"{coin_symb} alerts turned on")
    except:
        await ctx.send(f"{coin_symb} was not found")



client.run(TOKEN)
