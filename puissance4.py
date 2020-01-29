#VERSION DISCORD PY D'UN JEU DE PUISSANCE 4
#******************
#******************

#from p4_funct import jouer,coup_gagnant #import des fonctions spécifiques au jeu
import csv
import discord
from discord.ext import commands
import asyncio
bot = commands.Bot(command_prefix='!')


@bot.command()
async def anniv(ctx):
    simon = discord.utils.get(ctx.guild.members, id = 291319580461236225)
    await ctx.send(f"Bon anniversaire {simon.mention} !")


#COMMANDES POUR LE FONCTIONNEMENT DU BOT #######################################
@bot.event #à la connexion
async def on_ready():
    print("Bot de jeux connecté")
    with open("summon.txt", "r") as summon :
        channel = summon.read()
        channel = bot.get_channel(int(channel))
    await channel.send("Je suis arrivé, utilise **!puissance** pour voir ?")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!puissance"))

@bot.command(hidden=True) #à la déconnnexion, commande réservée.
async def fin(ctx):
    if ctx.author.id == 404395089389944832 :
        await ctx.send("Déconnexion...")
        print("Bot de jeux déconnecté")
        await bot.close()
    else :
        await ctx.send("nope")


#COMMANDE POUR LES RANKINGS ####################################################

@bot.command()
async def winrate(ctx):
    winners = {}
    loosers = {}
    enemys = []
    with open('wins.txt', newline='', encoding="utf8") as wins:
        reader = csv.reader(wins)
        for row in reader:
            winner = row[1]
            looser = row[2]
            if winner in winners :
                winners[winner] += 1
            else :
                winners[winner] = 1

            if looser in loosers :
                loosers[looser] += 1
            else :
                loosers[looser] = 1

            enemys.append([row[1],row[2]])
    #
    try :
        name = f"{ctx.message.author.name}#{ctx.message.author.discriminator}"
        win_rate = winners[name]/(loosers[name]+winners[name])
        await ctx.send(f"{ctx.message.author.mention}, ton winrate est de : {int(win_rate*100)}%")
    except :
        await ctx.send("Tu n'as pas encore gagné de partie")

    # for personne in winners :
    #     if personne in loosers :
    #         win_rate = winners[personne]/(loosers[personne]+winners[personne])
    #     else :
    #         win_rate = 1
    #     print(personne, win_rate)


@bot.command()
async def top_winner(ctx):
    winners = {}
    with open('wins.txt', newline='', encoding="utf8") as wins:
        reader = csv.reader(wins)
        for row in reader:
            winner = row[1]
            if winner in winners :
                winners[winner] += 1
            else :
                winners[winner] = 1

    top_wins = 0
    for winner in winners :
        if winners[winner] > top_wins :
            top_wins = winners[winner]
            top_winner = winner
    print(top_wins, top_winner)

@bot.command()
async def top_wins(ctx):
    pass
    # with open("wins.txt", "r") as wins :


#DEFINITION DES FONCTIONS POUR LE JEU ##########################################

#************* CREATION/REINITIALISATION DE LA GRILLE **************************
#on initialise une grille de 7 colonnes et 6 lignes
#chaque colonne est une liste de taille 6
def new_grille():
    global grille
    grille = [[a for a in ["0"]*7] for b in ["0"]*6]
    #c'est beau les 'list comprehensions'

#PLACER UN JETON ***************************************************************
#un joueur sélectionne la colonne dans laquelle il veut placer son jeton
#le "joueur" est alors placé dans la liste à la position adéquate
def jouer(joueur, col):
    colonne = col
    if grille[5][colonne] != "0" :
        print("cette colonne est pleine, tu as perdu ton tour")
        return  "raté"
    else :
        i = 5
        #tant qu'aucun pion n'est trouvé, on descend dans la grille
        while grille[i][colonne] == "0" and i>=0:
            i -=1
        grille[i+1][colonne] = joueur
        position=[i+1, colonne]
        #"position" est retournée par la suite pour déterminer si le coup est gagnant

        if grille[5][colonne] != "0":
            pleine[colonne]=True

        #pour débugger ce merdier
        return position

#************** ON REGARDE SI LE PION PLACE EST GAGNANT ************************
def coup_gagnant(joueur, position):
#-------------- En colonne -----------------------------------------------------
#il y a juste besoin de compter les pions dans une seule direction
    ligne = position[0]
    colonne = position[1]
    compte = 0
    while compte <4 and position[0] > 0 :
        if grille[ligne][colonne] == joueur :
            compte += 1
            ligne -= 1
        else :
            break
    if compte == 4 :
        #print("gagné")
        return True

#-------------- En ligne de droite à gauche ------------------------------------
#à partir du pion posé, on explore d'abord vers la gauche
#puis on revient sur nos pas en comptant le nombre de pions
    curseur = position[1]
    compte = 0
    while grille[position[0]][curseur] == joueur :
        curseur-=1
    if grille[position[0]][curseur] != joueur :
        curseur+=1
    while compte <4 and 0 <= curseur < 7  :
        if grille[position[0]][curseur] == joueur :
            curseur += 1
            compte += 1
        else :
            break
    if compte == 4 :
        #print("gagné")
        return True

#-------------- En diagonale / dans les 2 directions ---------------------------
#même principe en diagonale, il faut tenir compte des limites de la grille
    curseur0 = position[0]
    curseur = position[1]
    compte = 0
    while grille[curseur0][curseur] == joueur  and curseur0 > 0 and curseur > 0:
        curseur0 -= 1
        curseur -= 1
    if grille[curseur0][curseur] != joueur :
        curseur0 += 1
        curseur += 1
    while compte <4 and 0 <= curseur < 6  and 0 <= curseur0 < 7:
        if grille[curseur0][curseur] == joueur :
            curseur0 += 1
            curseur += 1
            compte += 1
        else :
            break
    if compte == 4 :
        #print("gagné")
        return True

#-------------- En diagonale \ dans les 2 directions ---------------------------
    curseur0 = position[0]
    curseur = position[1]
    compte = 0
    while grille[curseur0][curseur] == joueur and curseur0 < 5 and curseur > 0 :
        curseur0 += 1
        curseur -= 1
    if grille[curseur0][curseur] != joueur :
        curseur0 -= 1
        curseur += 1
    while compte <4 and 0 <= curseur < 6  and 0 <= curseur0 < 7:
        if grille[curseur0][curseur] == joueur :
            curseur0 -= 1
            curseur += 1
            compte += 1
        else :
            break
    if compte == 4 :
        #print("gagné")
        return True

#AFFICHER LA GRILLE ************************************************************
#fonction permettant d'envoyer un embed discord avec la grille de jeu
#renvoie un objet "message" qui peut ensuite être supprimé
async def afficher_grille(ctx, j1, j2):
    chaine = ""
    for i in reversed(grille) :
        chaine+="|"
        for a in i :
            if a == j1 :
                chaine+=" 😶 |"
            elif a == j2 :
                chaine+=" 😡 |"
            else :
                chaine+=" 🥶 |"
        chaine+="\n"
    chaine+="\n|"
    for emoji in ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"] :
        chaine+=f" {emoji} |"
    embed = discord.Embed(
        title=f"Partie entre {j1.display_name} et {j2.display_name}",
        description=chaine)
    message = await ctx.send(embed=embed)
    return message

#************ FACTORISATION DE LA BOUCLE DE JEU ********************************
#à chaque tour, un joueur envoie un message pour sélectionner la colonne
#il faut filtrer les messages n'étant pas des coups joués
async def tour(ctx, joueur_actuel, opposant):

    #on vérifie que l'auteur du message est bien le joueur en cours
    def check_auteur(m):
        return m.author.id == joueur_actuel.id

    try :
        col = "7"
        while col not in ["0", "1", "2", "3", "4", "5", "6"] :
        #on vérifie que le contenu du message est bien un coup éligible
        #tant que ce n'est pas le cas, le bot attend
            message = (await bot.wait_for('message', timeout=20, check=check_auteur))
            col = message.content
        #quand le message correspond aux critères :
        await message.delete() #il est supprimé

        #et la position est jouée
        position = jouer(joueur_actuel, int(col))
        
        #création d'un log pour le debugging
        liste_lignes = [
        f"position = jouer('{joueur_actuel.display_name}', {col}, a, pleine)\n"
        f"if coup_gagnant('{joueur_actuel.display_name}', {position}, a):\n"
        "    print ('coup_gagnant')\n"
        "else :\n"
        "    print('non')\n",
        "print(position)\n",
        ]

        with open("log_parties.txt", "a+") as log :
            log.writelines(liste_lignes)

        if position != "raté" :
        #si la colonne était déjà pleine, le joueur n'avait qu'à ouvrir les yeux
        #sinon :
            if coup_gagnant(joueur_actuel, position) :
                print(f"bravo {joueur_actuel.display_name}, tu as gagné")
                await ctx.send(f"Bravo {joueur_actuel.mention}, tu as gagné !")
                gagné = True
                #----------Création d'un log
                from datetime import date
                today = date.today()
                with open ("wins.txt", "a", encoding="utf8") as wins:
                    try :
                        wins.write(f"{today},{joueur_actuel},{opposant}\n")
                    except :
                        print("Something went wrong...")

                return True
            else :
                return False
        else :
            await ctx.send(f"Tu as perdu ton tour {joueur_actuel.mention}, \
il ne fallait pas mettre le pion dans une colonne pleine !")
            return False
    except asyncio.TimeoutError:
        #un timeout pour dynamiser le jeu
        await ctx.send(f"Temps écoulé, {opposant.mention}, à toi de jouer !")
        return False


#*******************************************************************************
#************ BOUCLE DE JEU PRINCIPALE *****************************************

@bot.command()
async def puissance(ctx):
    if ctx.channel.id not in [667101857948237844, 640263768764317699] :
        channel = bot.get_channel(667101857948237844)
        await ctx.send(f"--> {channel.mention}")
    else :
        import asyncio
        pleine = [False]*7  #check si les colonnes sont pleines
        gagné = False       #pour sortir de la boucle

    #------------- SETUP -----------------------------------------------------------
        joueur1 = ctx.message.author
        message = await ctx.send(f"{joueur1.mention} veut faire un puissance4, cliques sur le 👍 pour le rejoindre")
        await message.add_reaction("👍")

        def check(reaction, user):
            return reaction.emoji == "👍" and reaction.message.id == message.id and not user.bot

        try :
            reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Personne n'a réagit, une autre fois peut être ?")
        else :
            joueur2 = user
            await ctx.send(f"{joueur2.mention}, tu es entré dans la partie !")
            new_grille()

            grille = await afficher_grille(ctx, joueur1, joueur2)
            await ctx.send(f"{joueur1.mention},entre le numéro de la colonne ou tu veux placer ton pion\n\
    {joueur1.display_name}, tu as les 😶\n\
    {joueur2.display_name}, tu as les 😡")
            #création d'un log pour le debugging
            with open("log_parties.txt", "a+") as log :
                import datetime
                x = datetime.datetime.now()
                log.write(f"\n\n{str(x)}\n")
                #log.write(f"joueur1 = {joueur1.display_name}\njoueur2 = {joueur2.display_name}\n")

    #---------------- BOUCLE -------------------------------------------------------

            while not all(pleine) and not gagné :
                try :
                    gagné = await tour(ctx, joueur1, joueur2)
                    await grille.delete()
                    grille = await afficher_grille(ctx, joueur1, joueur2)
                except :
                    pass
                if gagné :
                    break
                try :
                    gagné = await tour(ctx, joueur2, joueur1)
                    await grille.delete()
                    grille = await afficher_grille(ctx, joueur1, joueur2)
                except :
                    pass
            if all(pleine) and not gagné :
                await ctx.send("Match nul")


################################################################################
#NECESSAIRE AU FONCTIONNEMENT DU BOT, DOIT ÊTRE PLACE A LA FIN #################
#-------------------------------------------------------------------------------
with open('tok_jeux.txt', 'r') as token :
    t=token.read()
    bot.run(t)
