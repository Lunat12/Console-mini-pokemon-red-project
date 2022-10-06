#Libraries-------------------------------------------------------------------------------------------------------
import requests
import random


#Global Variables------------------------------------------------------------------------------------------------
availableLocations = []
currentLocation = 0
pokedex = []


#Functions that get information out of the Api-------------------------------------------------------------------
def GetPokemon(_pokemon):#Access to species
    pokemonUrl = f'https://pokeapi.co/api/v2/pokemon-species/{str(_pokemon)}'
    getSpecies = requests.get(pokemonUrl)
    getSpecies = getSpecies.json()

    return getSpecies


def GetPokemonHabilities(_pokemon):#Access to pokemon
    pokemonUrl = f'https://pokeapi.co/api/v2/pokemon/{str(_pokemon)}'
    getSpecies = requests.get(pokemonUrl)
    getSpecies = getSpecies.json()

    return getSpecies


def GetPokemonsInArea():#Accesses location and gets all of the pokemons found there

    locationUrl = f'https://pokeapi.co/api/v2/location/{availableLocations[currentLocation]}'
    getLocation = requests.get(locationUrl)
    getLocation= getLocation.json()

    areaUrl = getLocation["areas"][0]["url"]
    getArea = requests.get(areaUrl)
    getArea = getArea.json()

   
    combatList = []
    for pokemon in getArea["pokemon_encounters"]:

        combatList.append(pokemon["pokemon"]["name"])
    
    return combatList


def SaveLocations():#Accesses region to get all the locations found there

    regionUrl = f'https://pokeapi.co/api/v2/region/kanto'
    getRegion = requests.get(regionUrl)
    getRegion= getRegion.json()

    for location in getRegion["locations"]:
        availableLocations.append(location["name"])


#tool functions---------------------------------------------------------------------------------------------
def Pokemon_selector():#Selects one of the users pokemons

    while True:
        currentPokemon = input('\nEnter the pokedex entry number of the pokemon you want to use (You must have it in order to use it): ')
        if currentPokemon.isdigit():
            currentPokemon = int(currentPokemon)
            if currentPokemon > 0 and currentPokemon < 152: 

                species = GetPokemon(currentPokemon)

                speciesName = species["varieties"][0]["pokemon"]["name"]

                if speciesName in pokedex: break
                else:
                    print("\nSorry, you don't have this pokemon")
                    Pokedex_Consult()
            else:
                print("\nSorry, this pokemon is not available on this generation. Theres currently only 151 pokemons, try one of those.")
        else:
            print("\nPokedex entrys must be in digits.")

    
    print(f'You chose {speciesName}')

    return currentPokemon, speciesName


def Pokemon_Asignation(pokemon):#Saves a pokemon on the user pokemon list

    print(f'\nCongratulations you captured a {pokemon}!')
    if pokemon not in pokedex:
        pokedex.append(pokemon)
        print(f'The pokemon was added to the pokedex.')


#Steps of the run functions-------------------------------------------------------------------------------------
def StarterPick():#Introduction to the app

    while True:
        definingChoice = input("\nWelcome Trainer, I'm professor Oak and im here to get you started on your adventure.\nLets pick your first pokemon:\n\n\t1.Charmander\n\n\t2.Squirtle\n\n\t3.Bulbasaur\n\n\tYour choice: ")
        if definingChoice == '1':
            Pokemon_Asignation("charmander")
            break
        elif definingChoice == '2':
            Pokemon_Asignation("squirtle")
            break
        elif definingChoice == '3':
            Pokemon_Asignation("bulbasaur")
            break 


def SwitchLocation():#Allows the user to change its location

    global currentLocation
    direction = str(input(f'\nYou find yourself at {availableLocations[currentLocation]} Where do you want to go (foward/back)? ')).lower()[0] == 'f'

    if direction and currentLocation < len(availableLocations):
        currentLocation += 1       
    elif not direction and currentLocation > 0:
        currentLocation -= 1

    print(f'You went to {availableLocations[currentLocation]}')


def Combat():#Allows the user to get one pokemon of the location

    combatList = GetPokemonsInArea()
    wildPokemon = random.randint(0,len(combatList)-1)
    wildPokemon = combatList[wildPokemon]

    print(f'\nA wild {wildPokemon} appeared!\nLets try to capture it\n\nUse one of your pokemons to fight {wildPokemon}.')

    currentPokemon, pokemonName = Pokemon_selector()
    
    species = GetPokemonHabilities(currentPokemon)

    print(f'\nYour {pokemonName} used {species["abilities"][0]["ability"]["name"]}\n{wildPokemon} was defeated.')

    Pokemon_Asignation(wildPokemon)


def Pokedex_Consult():#Allows the user to consult his pokemons and their information
    
    print("\nHere's a list of your pokemon:\n")

    for pokemon in pokedex:
        getID = GetPokemon(pokemon)
        getCombat = GetPokemonHabilities(pokemon)
        
        ID = getID["id"]
        Type = getCombat["types"][0]["type"]["name"]
        Hability = getCombat["abilities"][0]["ability"]["name"]

        print(f"\tPOKEDEX ENTRY: {ID}\tNAME: {pokemon}\tTYPE: {Type}\tMAIN ATTACK: {Hability}")


def Close():#closes app
    print('\nClosing, progress wont be saved...')
    exit()


#Menu Dictionary------------------------------------------------------------------------------------------------
options = { '1' : SwitchLocation, '2' : Pokedex_Consult, '3' : Combat, '4': Close}


#Run------------------------------------------------------------------------------------------------------------
SaveLocations()

StarterPick()

while True:

    action = input('\nWhat will you do now trainer?\n\n\t1-Move to another location\n\n\t2-Consult your Pokedex\n\n\t3-Fight\n\n\t4-End adventure\n\n\tSelect one: ')

    if action.isdigit():
        if int(action) > 0 and int(action) < 5:
            options[action]()
        else:
            print('\n\tInvalid Option')
    else:
        print('\n\tOptions must be digits')