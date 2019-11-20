from math import *
import pygame

pygame.init()


#Definition des constantes

screenSize = 1080,720
screen = pygame.display.set_mode ((screenSize))
pygame.display.flip ()

pygame.display.set_caption("Représentation graphique de l'ensemble de Julia")

nMax = 50
running = True

juliaSize = 2500
surfaceJulia = pygame.Surface ((juliaSize,juliaSize))
surfaceJuliaResized = None
resizeOrigin = 550

white = (230,230,230)
black = (10,10,10)
green = (50,200,50)
red = (200,50,50)

#Definition des variables

c = -0.85,0.2
step = 10
showAdvencement = False
R,G,B = True,True,False

mouseClick = False
mouseKeep = False
mouseSlide = False
dist = 0
select = 0
resizeSize = 550
newC = ["_","_"]
defC = False
showInfos = False
showSetings = False
showHelp = False


#Definition des fonctions

def pygameEvents () :
    global running, mouseClick, mouseKeep, defC, newC, select, showInfos

    if mouseClick == True : mouseClick = False

    for event in pygame.event.get () :
        if event.type == pygame.QUIT :
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
            mouseKeep = True
            mouseClick = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 : mouseKeep = False

        if event.type == pygame.KEYDOWN :
            if showInfos == True :
                if event.unicode == "" : showInfos = False

            if defC == True :

                if event.unicode == "" : defC = False

                if event.unicode == "+" and not (newC[select] == "" or newC[select] == "_") : select = 1

                if event.unicode == "-" :
                    if (newC[select] == "" or newC[select] == "_") and not "-" in newC[select] :
                        if newC[select] == "_" : newC[select] = ""
                        newC[select] += "-"

                if event.unicode == "" :
                    if (newC[select] == "" or newC[select] == "_") and select == 1 : select = 0
                    newC[select] = (newC[select])[:-1]

                if event.unicode == "," or event.unicode == "." :
                    if not newC[select] == "" and not newC[select] == "_" and not "." in newC[select] : newC[select] += "."

                try :
                    if  0 <= int(event.unicode) <= 9 :
                        if newC[select] == "_" : newC[select] = ""
                        newC[select] += event.unicode
                except : pass


    pygame.display.update()


def Julia (z0, c, Max) :
    """
    Cette fonction permet de tester si une valeure
    appartient à l'ensemble de Julia. Elle renvoie
    la valeure maximale que peut obtenir "Z"

    z0 : Le premier terme de la suite "Z".
    c : La variable C qui défini C.
    Max : Limite de N, à savoir le nombre d'éléments
          de la suite.
    """
    awnser = True
    z = z0
    zmax = 0

    for n in range (0, Max) :

        _z_ = sqrt (z[0]**2 + z[1]**2)

        # z0 ∈ Complexes   Zn+1 = (Zn**2) + C

        z = (z[0]**2) - (z[1]**2) + c [0] , 2 * z[0] * z[1] + c[1]

        if _z_ > zmax : zmax = _z_

        if _z_ > 2 :
            break

    return zmax


def drawJulia () :
    global juliaSize, c, zMax, surfaceJulia, step, running, R,G,B, black, green

    pygame.draw.rect(surfaceJulia, black, (0,0,juliaSize,juliaSize))

    p = 127.5

    for y in range (int(-juliaSize/2),int(juliaSize/2),step) :
        for x in range (int(-juliaSize/2),int(juliaSize/2),step) :

            xi,yi = x/(juliaSize/2*1.25),y/(juliaSize/2*1.25)

            z_0 = xi,yi

            Jul = Julia (z_0, c, nMax)

            if Jul <= 2 :


                if R == True : r = 255-Jul*p
                elif R == False : r = Jul*p
                if G == True : g = 255-Jul*p
                elif G == False : g = Jul*p
                if B == True : b = 255-Jul*p
                elif B == False : b = Jul*p

                pygame.draw.rect(surfaceJulia, (r,g,b), (x+(juliaSize/2),y+(juliaSize/2),step,step))


        if showAdvencement == True :
            blitJulia ()
        else :
            pygame.draw.rect(screen, (white), (140,400,800,50))
            pygame.draw.rect(screen, (green), (140,400,(800*(y+juliaSize/2))/juliaSize,50))

        pygameEvents ()

        if running == False :
            break



def blitJulia () :
    global surfaceJuliaResized, surfaceJulia, screenSize, resizeSize, defC, showInfos, showSetings

    if defC == False and showInfos == False and showSetings == False :
        if mouseKeep == True and not mouseSlide == False : pass

        """
        if mouseKeep == True and not mouseSlide == False :
            Button (840,300,225,160, ["Faites", "glisser","la souris"], None)
            dist = int(mouseSlide[0]-mousePos[1])
            resizeSize = resizeOrigin + dist
            if resizeSize < 500 :
                resizeSize = 500
                dist = resizeSize-resizeOrigin
            elif resizeSize > 3000 :
                resizeSize = 3000
                dist = resizeSize-resizeOrigin
        else : mouseSlide = False
        """
        """
        if (xC1 < mousePos[0] < xC1 + xC2 and yC1 < mousePos[1] < yC1 + yC2) or not mouseSlide == False :
            if mouseClick == True and mouseSlide == False: mouseSlide = mousePos[1] + dist, "move"
        """


    surfaceJuliaResized = pygame.transform.scale (surfaceJulia, (resizeSize,resizeSize))
    screen.blit (surfaceJuliaResized, (screenSize[0]/2 - resizeSize/2 , screenSize[1]/2 - resizeSize/2 + 85))


def Button (xC1,yC1,xC2,yC2, textString, name) :
    global step, R,G,B, black, white, red, dist, mouseSlide, mouseClick, mouseKeep, resizeOrigin, resizeSize, showAdvencement, showHelp, c, defC, select, newC, showInfos, showSetings

    if R == True : r = 50
    elif R == False : r = 150
    if G == True : g = 50
    elif G == False : g = 150
    if B == True : b = 50
    elif B == False : b = 150

    customColor = (r,g,b)

    textFont = pygame.font.SysFont("consolas", 30)

    mousePos = pygame.mouse.get_pos ()

    keys=pygame.key.get_pressed()

    if xC1 < mousePos[0] < xC1 + xC2 and yC1 < mousePos[1] < yC1 + yC2 and mouseSlide == False:
        pygame.draw.rect(screen, white, (xC1,yC1,xC2,yC2))
        pygame.draw.rect(screen, black, (xC1,yC1,xC2,yC2),10)
        if type(textString) is list :
            cText = []
            for text in textString :
                cText.append (textFont.render(text, True, customColor))
        else : cText = [textFont.render(textString, True, customColor)]

        if mouseClick == True and defC == False and showInfos == False :
            if name == "generate" and showSetings == False :
                if showAdvencement == True : tellMessage (("     Veuillez patienter pendant la","        génération de l'image."),(0,50))
                else : tellMessage (("     Veuillez patienter pendant la","        génération de l'image.","","","","","","","  (Si le chargement stoppe, relancez"," le programme.)"),(0,50))
                drawJulia ()

            if name == "c" and showSetings == False :
                defC = True
                newC = ["_","_"]
                select = 0

            if name == "info" and showSetings == False :
                showInfos = True

            if name == "config" and showSetings == False :
                showSetings = True

            if name == "red" :
                if R == True : R = False
                else : R = True
            if name == "green" :
                if G == True : G = False
                else : G = True
            if name == "blue" :
                if B == True : B = False
                else : B = True

            if name == "showAd" :
                if showAdvencement == True : showAdvencement = False
                else : showAdvencement = True

            if name == "step" :
                if step == 50 : step = 1
                elif step == 20 : step = 50
                elif step == 10 : step = 20
                elif step == 5 : step = 10
                elif step == 2 : step = 5
                elif step == 1 : step = 2

            if name == "help" :
                showHelp = True
                mouseClick = False

            if name == "save" : pygame.image.save(surfaceJulia,'Julia.png')




    else :
        if textString == "X" : pygame.draw.rect(screen, red, (xC1,yC1,xC2,yC2))
        else : pygame.draw.rect(screen, black, (xC1,yC1,xC2,yC2))
        pygame.draw.rect(screen, customColor, (xC1,yC1,xC2,yC2),10)
        if type(textString) is list :
            cText = []
            for text in textString :
                cText.append (textFont.render(text, True, white))
        else : cText = [textFont.render(textString, True, white)]


    a = 0
    if len (cText) > 1 : b = len (cText) * 10
    else : b = 0
    for text in cText :
        textSize = text.get_rect().size
        newX = xC2 - 15
        if textSize[0] > newX :
            text2 = pygame.transform.scale(text, (newX, int(textSize[1]*newX/textSize[0])))
            textSize = text2.get_rect().size
        else : text2 = text

        screen.blit (text2, (xC1 + xC2/2- textSize[0]/2,yC1 + yC2/2 + a - textSize[1]/2 - b))
        a+= 30


    if showHelp == True and name == "help":
        tellMessage (["","","","  Qualité de l'image","                         Edition","  Afficher l'image    des couleurs.","pendant le chargement"],(0,0))
        if mouseClick == True or keys[pygame.K_RETURN] : showHelp = False


    if name == "cconfirm" or name == "closeInfo" or name=="configQuit" :
        if (xC1 < mousePos[0] < xC1 + xC2 and yC1 < mousePos[1] < yC1 + yC2 and mouseClick == True) or keys[pygame.K_RETURN] :
            if name == "cconfirm" :
                if not newC[1] == "" and not newC[1] == "_" :
                    defC = False
                    c = float(newC[0]), float(newC[1])
            elif name == "closeInfo" : showInfos = False
            elif name == "configQuit" : showSetings = False


    if name == "zoom" and defC == False and showInfos == False and showSetings == False :
        if mouseKeep == True and not mouseSlide == False :
            if mouseSlide[1] == "zoom" :
                Button (840,300,225,160, ["Faites", "glisser","la souris"], None)
                dist = int(mouseSlide[0]-mousePos[1])
                resizeSize = resizeOrigin + dist
                if resizeSize < 500 :
                    resizeSize = 500
                    dist = resizeSize-resizeOrigin
                elif resizeSize > 3000 :
                    resizeSize = 3000
                    dist = resizeSize-resizeOrigin
        else : mouseSlide = False

        if (xC1 < mousePos[0] < xC1 + xC2 and yC1 < mousePos[1] < yC1 + yC2) or not mouseSlide == False :
            if mouseClick == True and mouseSlide == False: mouseSlide = mousePos[1] + dist, "zoom"

    if defC == True and name == "c" :

        if newC[select] == "" : newC[select] = "_"

        if newC[0] == "_" : select = 0
        elif keys[pygame.K_RETURN] or keys[pygame.K_PLUS] or keys[pygame.K_SPACE] : select = 1


        textMessage = ["   Entrez une valeur pour 'c'.","","         c = " + str(newC[0]) + " + " + str(newC[1]) + "i"]
        positionMessage = 50,150
        tellMessage (textMessage,positionMessage)
        Button (400,400,250,60, "Confirmer", "cconfirm")

    if showInfos == True and name == "c":
        textMessage = ["Ce projet a été entierement réalisé par","Yves-Antoine Gangner dans le cadre d'un","mini-projet dans la spécialité ''ISN'',","dans l'établissement Saint Andrée à","Niort. Le projet consiste à représenter","graphiquement l'ensemble de Julia à","l'aide d'un algorithme dans le langage","python. J'ai réalisé ce projet en","utilisant, en plus des outils intégrés","à python, le module ''pygame'' qui","simplifie grandement la création","d'interfaces graphiques."]

        positionMessage = 10,0
        for i in range (0,2) : tellMessage (textMessage,positionMessage)

        Button (800,650,250,60, "Fermer", "closeInfo")



def blitInterface () :
    global screen, white, screenSize, black, R,G,B, c, resizeSize, juliaSize, step, showAdvencement

    pygame.draw.rect(screen, black, (0,0,screenSize[0],screenSize[1])) #Reset de l'écran

    titleFont = pygame.font.SysFont("century", 50, "bold")

    textFont = pygame.font.SysFont("consolas", 30)

    if R == True : r = 50
    elif R == False : r = 150
    if G == True : g = 50
    elif G == False : g = 150
    if B == True : b = 50
    elif B == False : b = 150

    customColor = (r,g,b)

    if showSetings == False : blitJulia ()

    pygame.draw.rect(screen, white, (0,-96,screenSize[0],screenSize[1]+530),530) #zone blanche

    if showSetings == False :
        title = titleFont.render("L'ensemble de Julia", True, black)
        screen.blit (title, (265,30))
        pygame.draw.rect(screen, black, (450,85,300,5))

        #Bouton "générer"
        Button (20,400,225,60, "générer", "generate")

        #Bouton Zoom
        Button (840,300,225,160, "Zoom x " + str(round ((resizeSize/juliaSize),2)),"zoom")

        #Bouton "paramètres"
        Button (20,500,225,60, "configurations", "config")

        #Bouton "info"
        Button (840,500,225,60, "informations", "info")

        #Bouton "C"
        Button (20,300,225,60, "c=" + str(c[0]) + "+" + str(c[1]) + "i", "c")

    else :
        blitBlackRect ()
        deca = 50
        pygame.draw.rect(screen, white, (deca,deca,screenSize[0]-2*deca,screenSize[1]-2*deca)) #zone blanche
        pygame.draw.rect(screen, customColor, (deca,deca,screenSize[0]-2*deca,screenSize[1]-2*deca),20) #zone blanche

        title = titleFont.render("Configuration", True, black)
        screen.blit (title, (350,80))
        pygame.draw.rect(screen, black, (450,140,300,5))

        #Bouton "X"
        Button (screenSize[0]-1.5*deca,deca/2,deca,deca,"X", "configQuit")

        Button (85,200,390,60,"Taille de pixels = " + str(step), "step")

        Button (85,300,390,60,"Montrer la génération : " + str(showAdvencement), "showAd")

        Button (85,400,390,60,"Enregistrer l'image", "save")

        Button (550,200,390,60,"Variations de Rouge = " + str(R), "red")
        Button (550,300,390,60,"Variations de Vert = " + str(G), "green")
        Button (550,400,390,60,"Variations de Bleu = " + str(B), "blue")

        Button (840,500,100,60,"Aide", "help")



def blitBlackRect () :
    global screenSize
    black_rect = pygame.Surface(screenSize)
    black_rect.fill(black)
    black_rect.set_alpha (220)
    screen.blit (black_rect,(0,0))


def tellMessage (message,position) :
    global white, black, screenSize

    newPos = position

    if not message == "" :

        blitBlackRect ()

        try : message.split (",")
        except : pass
        T = []
        x = 0
        for lines in message :
            T.append ("")
            T[x] = text ()
            T[x].blit (lines, newPos)
            newPos = newPos[0], newPos[1] + 60
            x += 1

class text :
    def blit (self, message, position) :
        textFont = pygame.font.SysFont("consolas", 50)
        messageText = textFont.render(message, True, white)
        screen.blit (messageText,(position))


#Main-Loop

while running :

    blitInterface ()

    pygameEvents ()

pygame.quit ()