import discord                          #on fait un bot pour discord, c'est de première nécessité
import random                           #importe la bilbiothèque nécessaire pour créer de l'aléatoire
import math                             #importe le module math pour la valeur aboslue
import re                               #importe les expressions régulières

from discord.ext import commands


bot = commands.Bot(command_prefix = '$', )



@bot.command(help="Cette comande répète le premier mot de ta phrase : ce bot est encore un enfant, OK ? ")      #tout est dans $help
async def repeat(ctx, arg):         #ctx = le contexte de la commande, arg = le truc à répéter
    await ctx.send(arg)

@bot.event                      #quand le bot se connecte, "bonjour" s'affiche dans la console
async def on_ready():
    print('bonjour')



@bot.command(help="Un petit jeu pour tuer le temps : il faut taper $score suivi d'un guess entre 0 et 100. Le bot trouve un nombre mystère aléatoire et fait la différence avec ton guess. Plus celle-ci est petite, plus tu es lucky")                           #commande $score : permet de faire un guess et d'obtenir la différence avec ce guess
async def score(ctx, guess):

    random.seed()                           #initialise la seed et
    score = random.randint(0,100)           #renvoie un nb pseudo aléatoire dans l'intervalle [0;100]

    guess = int(guess)
    delta = abs(score-guess)  # 2 lignes pour calculer la différence absolue entre le guess et le score obtenu (abs vient de la bibliothèque math)

    await ctx.send('nombre mystère : {}'.format(score)) #renvoie le résultat en msg discord
    await ctx.send('différence : {}'.format(delta))     #renvoie la différence

    from datetime import date
    today = date. today()       #2 lignes pour écrire la date d'obtention du score

    resultats = open("resultats.txt","a")   #ouvre le fichier resultats.txt en mode "append" : chaque écriture se fait à la suite de ce qui est déjà écrit
    resultats.writelines([str(ctx.message.author), " : " ,str(delta), " : ", str(today),"\n"]) #ecrit le nom d'utilisateur, le score et la date dans chaque nouvelle ligne du .txt
    resultats.close()   # a priori utile de fermer le fichier une fois écrit pour pouvoir l'ouvrir dans une autre commande

@score.error
async def score_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il faut mettre un nombre après $score")
    elif(error, commands.CommandInvokeError):
        await ctx.send("$score n'accepte pas les chaines de caractères :rage:")
    else:
        await ctx.send("erreur")

@bot.command(help="Cette commande renvoie le nom d'utilisateur ayant eu le meilleur delta par rapport à son guess. \nLes résultats sont rentrés dans un fichier quand $score est appelé, et cette commande lit le fichier qui en résulte.")                  #commande pour extraire celui ayant le meilleur guess, accompagné de la date
async def best(ctx):
    resultats = open("resultats.txt", "r")
    min = 101
    for i, line in enumerate(resultats):
        match = re.search('(: )(\d?\d)( :)', line) #chaque expression entre parenthèse correspond à un groupe
        if match:
            score_obtenu = match.group(2)          #le group(2) fait référence aux deuxièmes parenthèses du match
            score_obtenu = int(score_obtenu)
            if (score_obtenu < min):
                min = score_obtenu
                match = re.search('[^0-9^#]*', line)
                if match:
                    nom = match.group(0)
                match = re.search('\d{4}-\d{2}-\d{2}', line)
                if match:
                    date = match.group(0)
        else:
            print("il n'y a pas encore de résultat")
    await ctx.send("{} a obtenu le meilleur delta, à savoir {} le {}".format(nom, min, date))

@bot.command(help="Quelques phrases typiques 😉")
async def serrano(ctx):
    random.seed()                           #initialise la seed
    lol = ["Considérez les préfixes comme étant corrects",
            "N'oubliez pas, les distanciels c'est 80% du temps de travail !",
            "Merci à Emmanuel Desmontils :heartpulse: :heart_eyes:",
            "On range son portable !",
            "FAITES PASSER LE PAQUET !!! :rage:",
            "Ne soyez pas non plus de mauvaise foi !",
            "UN PAQUET C'EST UNE COPIE",
            "Ne prenez pas mon stylo sinon on va tous être malade :nauseated_face: ",
            "Faut être plus précis",
            "Vous devez compléter le tableau !"
            ]
    await ctx.send(lol[random.randint(0,(len(lol)-1))])


@bot.command(help="Quelques phrases typiques 😉")
async def mekaouche(ctx):
    random.seed()
    lol = ["Tu vas pas me salir, je vais pas te salir",
            "Et si on commençait par 30 minutes pour découvrir un nouveau language : Bash. Quoi ? vous avez eu des cours ?",
            "MAIS REGARDE DANS TON COURS !!",
            "Regarde dans ton cours..."]
    await ctx.send(lol[random.randint(0,(len(lol)-1))])



@bot.command()
async def teletchea(ctx):
    cartouches = open("cartouches.txt","r")
    qte=cartouches.read()
    await ctx.send('{} articles se sont pris une cartouche :gun:'.format(qte))
    qte=int(qte)
    qte=qte+1
    cartouches.close
    cartouches = open("cartouches.txt","w")
    qte=str(qte)
    cartouches.write(qte)
    cartouches.close


@bot.command(help="efface le nombre de messages indiqué", hidden=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nb_messages : int):
    await ctx.channel.purge(limit=nb_messages)


@clear.error
async def clear_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")
    elif (isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send("Il faut mettre un nombre après $score")




#création de salons privés
@bot.command(help="Ecrire la commande suivie du nom du salon.\nPour ecrire plusieurs mots, ecrire la phrase entre guillemets")
@commands.has_permissions(administrator=True)
async def salon(ctx, arg):   #nom de la commande
#création du rôle
    guild = ctx.guild
    role = await guild.create_role(name=arg)

#création du salon
    cat=ctx.channel.category #permet de connaitre la catégorie du salon textuel, sinon le salon est créé tout en haut dans le serveur
    roles = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    role: discord.PermissionOverwrite(read_messages=True)
}
    await guild.create_text_channel(name=arg, overwrites=roles, category=cat)   #puis création du salon avec le même nom
@salon.error
async def clear_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")


#suppression des rôles et salons
@bot.command(help="Supprime un salon et un rôle\nDonner le nom du salon et du rôle en arguments de la commande\nPour les noms composés de plusieurs mots, utiliser les guillemets")
@commands.has_permissions(administrator=True)
async def dels(ctx, ch : discord.TextChannel, rl : discord.Role):
    await rl.delete()
    await ch.delete()
@dels.error
async def clear_error():
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("tu n'as pas les droits, loser !")


@bot.command()
async def aide(ctx):
    embed = discord.Embed(title="Aide", description="Comment utiliser les différentes commandes ?\nLa commande $help joue un rôle similaire, en moins bien\nUtiliser $help <commande> te permettra (ou pas) d'obtenir des informations plus détaillés sur la commande")
    embed.add_field(name="$score", value="Mini jeu : le but est de d'entrer un nombre entre 0 et 100 après la commande. Le bot te dira quel nombre il avait tiré et la différence entre avec ton tirage")
    embed.add_field(name="$best", value="Renvoie le nom de celui ayant la plus petite différence. Je reset la commande quand quelqu'un a un 0")
    embed.add_field(name="$serrano, $teletchea, $mekaouche", value="Juste pour rire :)")
    embed.add_field(name="$repeat", value="Répète ce qui est donné en argument, rien de très intéressant")
    embed.add_field(name="$salon", value="Crée un salon et un rôle dont le nom est donné en argument, réservé aux admins")
    embed.add_field(name="$dels", value="Efface un salon et un rôle. Il faut mettre le nom du salon en premier argument et le nom du rôle en deuxième argument, réservé aux admins")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas")
    else:
        print(error)


@bot.command()
async def pins(ctx):
    pins = await ctx.channel.pins()
    await ctx.send(pins[-1])

token=open('token.txt', 'r')
t=token.read()
bot.run(t)
