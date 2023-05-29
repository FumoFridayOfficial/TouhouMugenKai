print("LOADING GAMES INFO")
TouhouGames = {
                1:{
                    "Title": "Touhou 1 - Highly Responsive to Prayers",
                    "Developer": "ZUN Soft",
                    "Publisher": "Amusement Makers",
                    "Released": "1st display: November 1996, Full Release: 15/08/1997",
                    "Genre": "Scroll-less Action Shooting Game",
                    "Description": "HRtP. The first one.",
                    "Id": 1,
                    "Link": "https://en.touhouwiki.net/images/9/97/Th01cover.jpg",
                    "Cover": "th01.jpg",
                    "Abbr": "HRtP",
                    "Number": "1",
                    "Char": "Reimu Hakurei",
                    "File": "Touhou01"
                },
                2:{
                    "Title": "Touhou 2 - Story of Eastern Wonderland",
                    "Developer": "ZUN Soft",
                    "Publisher": "Amusement Makers",
                    "Released": "15/08/1997",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "SoEW, the second game also first bullet hell in the series.",
                    "Id": 2,
                    "Link": "https://en.touhouwiki.net/images/8/8c/Th02cover.jpg",
                    "Cover": "th02.jpg",
                    "Abbr": "SoEW",
                    "Number": "2",
                    "Char": "Marisa Kirisame,Reimu Hakurei,Mima",
                    "File": "Touhou02"
                },
                3:{
                    "Title": "Touhou 3 - Phantasmagoria of Dimensional Dream",
                    "Developer": "ZUN Soft",
                    "Publisher": "Amusement Makers",
                    "Released": "29/12/1997",
                    "Genre": "Competitive Vertical Bullet Hell Shooting Game",
                    "Description": "PoDD, two players indirectly battle one another.",
                    "Id": 3,
                    "Link": "https://en.touhouwiki.net/images/1/15/Th03cover.jpg",
                    "Cover": "th03.jpg",
                    "Abbr": "PoDD",
                    "Number": "3",
                    "Char": "Reimu Hakurei and many others",
                    "File": "Touhou03"
                },
                4:{
                    "Title": "Touhou 4 - Lotus Land Story",
                    "Developer": "ZUN Soft",
                    "Publisher": "Amusement Makers",
                    "Released": "14/08/1998",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "LLS, Yuuka!!",
                    "Id": 4,
                    "Link": "https://en.touhouwiki.net/images/3/35/Th04cover.jpg",
                    "Cover": "th04.jpg",
                    "Abbr": "LLS",
                    "Number": "4",
                    "Char": "Reimu Hakurei, Marisa Kirisame",
                    "File": "Touhou04"
                },
                5:{
                    "Title": "Touhou 5 - Mystic Square",
                    "Developer": "ZUN Soft",
                    "Publisher": "Amusement Makers",
                    "Released": "30/12/1998",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "MS, last PC-98 game :( but mima is a playable character!!!",
                    "Id": 5,
                    "Link": "https://en.touhouwiki.net/images/5/56/Th05cover.jpg",
                    "Cover": "th05.jpg",
                    "Abbr": "MS",
                    "Number": "5",
                    "Char": "Reimu Hakurei",
                    "File": "Touhou05"
                },
                6:{
                    "Title": "Touhou 6 - Embodiment of Scarlet Devil",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "08/11/2002",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "A toho game, EoSD",
                    "Id": 6,
                    "Link": "https://en.touhouwiki.net/images/8/8b/Th06cover.jpg",
                    "Cover": "th06.jpg",
                    "Abbr": "EoSD",
                    "Number": "6",
                    "Char": "Flandre Scarlet",
                    "File": "Touhou06"
                },
                7:{
                    "Title": "Touhou 7 - Perfect Cherry Blossom",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "17/08/2003",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "PCB, seventh game, pretty 'cool' game!",
                    "Id": 7,
                    "Link": "https://en.touhouwiki.net/images/5/52/Th07cover.jpg",
                    "Cover": "th07.jpg",
                    "Abbr": "PCB",
                    "Number": "7",
                    "Char": "Yukari Yakumo",
                    "File": "Touhou07"
                },
                8:{
                    "Title": "Touhou 7.5 - Immaterial and Missing Power",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "30/12/2004",
                    "Genre": "Fighting Game",
                    "Description": "IaMP,First fighting game!!",
                    "Id": 8,
                    "Link": "https://en.touhouwiki.net/images/8/88/Th075Cover.jpg",
                    "Cover": "th075.jpg",
                    "Abbr": "IaMP",
                    "Number": "7.5",
                    "Char": "Suika Ibuki",
                    "File": "Touhou075"
                },
                9:{
                    "Title": "Touhou 8 - Imperishable Night",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "15/08/2004",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "IN, third game released from the windows era!",
                    "Id": 9,
                    "Link": "https://en.touhouwiki.net/images/5/59/Th08cover.jpg",
                    "Cover": "th08.jpg",
                    "Abbr": "IN",
                    "Number": "8",
                    "Char": "Kayuga Hourasai and Moukou Fujiwara",
                    "File": "Touhou08"
                },
                10:{
                    "Title": "Touhou 9 - Phantasmagoria of Flower View",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "14/08/2005",
                    "Genre": "Competitive Vertical Bullet Hell Shooting Game",
                    "Description": "PoDD gameplay comesback with better looks!!(Cirno is playable)",
                    "Id": 10,
                    "Link": "https://en.touhouwiki.net/images/2/25/Th09cover.jpg",
                    "Cover": "th09.jpg",
                    "Abbr": "PoFV",
                    "Number": "10",
                    "Char": "Eiki Shiki, Yamaxanadu",
                    "File": "Touhou09"
                },
                11:{
                    "Title": "Touhou 9.5 - Shoot the Bullet",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "30/12/2005",
                    "Genre": "Vertical Bullet Hell Photography Shooting Game",
                    "Description": "StB, awesome new mechanics! Aya!",
                    "Id": 11,
                    "Link": "https://en.touhouwiki.net/images/0/09/Th095cover.jpg",
                    "Cover": "th095.jpg",
                    "Abbr": "StB",
                    "Number": "9.5",
                    "Char": "Aya Shameimaru",
                    "File": "Touhou095"
                },
                12:{
                    "Title": "Touhou 10 - Mountain of Faith",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "17/08/2007",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "The start of the 2nd Generation of Touhou games!",
                    "Id": 12,
                    "Link": "https://en.touhouwiki.net/images/6/6b/Th10cover.jpg",
                    "Cover": "th10.jpg",
                    "Abbr": "MoF",
                    "Number": "10",
                    "Char": "Kanako Yasaka",
                    "File": "Touhou10"
                },
                13:{
                    "Title": "Touhou 10.5 - Scarlet Weather Rhapsody",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "25/05/2008",
                    "Genre": "Fighting Game",
                    "Description": "SWR, the succesor of IaMP",
                    "Id": 13,
                    "Link": "https://en.touhouwiki.net/images/e/e1/Th105.jpg",
                    "Cover": "th105.jpg",
                    "Abbr": "SWR",
                    "Number": "10.5",
                    "Char": "Tenshi Hinanawi",
                    "File": "Touhou105"
                },
                14:{
                    "Title": "Touhou 11 - Subterranean Animism",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "16/08/2008",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "SA, NUCLEAR BIRD!!!!!",
                    "Id": 14,
                    "Link": "https://en.touhouwiki.net/images/7/75/Th11_Cover.jpg",
                    "Cover": "th11.jpg",
                    "Abbr": "SA",
                    "Number": "11",
                    "Char": "Utsuho Reiuji",
                    "File": "Touhou11"
                },
                15:{
                    "Title": "Touhou 12 - Undefined Fantastic Object",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "15/08/2009",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "UFO!UFO!UFO!",
                    "Id": 15,
                    "Link": "https://en.touhouwiki.net/images/a/ae/Th12cover.jpg",
                    "Cover": "th12.jpg",
                    "Abbr": "UFO",
                    "Number": "12",
                    "Char": "Byakuren Hijiri",
                    "File": "Touhou12"
                },
                16:{
                    "Title": "Touhou 12.3 - Hisoutensoku",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "15/08/2009",
                    "Genre": "Fighting Game",
                    "Description": "Succesor to SWR, Hisoutensoku",
                    "Id": 16,
                    "Link": "https://en.touhouwiki.net/images/7/72/Th123.jpg",
                    "Cover": "th123.jpg",
                    "Abbr": "Hiso",
                    "Number": "12.3",
                    "Char": "Cirno",
                    "File": "Touhou123"
                },
                17:{
                    "Title": "Touhou 12.5 - Double Spoiler",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "14/03/2010",
                    "Genre": "Vertical Bullet Hell Photography Shooting Game",
                    "Description": "Succesor to StB",
                    "Id": 17,
                    "Link": "https://en.touhouwiki.net/images/3/3b/Th125cover.jpg",
                    "Cover": "th125.jpg",
                    "Abbr": "DS",
                    "Number": "12.5",
                    "Char": "Hatate Himekaidou",
                    "File": "Touhou125"
                },
                18:{
                    "Title": "Touhou 12.8 - Fairy Wars",
                    "Developer": "Team Shanghai Alice/Makoto Hirasaka(portrait art)",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "14/08/2010",
                    "Genre": "Vertical Bullet Hell Freezing Game",
                    "Description": "CIRNO GAME",
                    "Id": 18,
                    "Link": "https://en.touhouwiki.net/images/2/23/Th128cover.jpg",
                    "Cover": "th128.jpg",
                    "Abbr": "FW",
                    "Number": "12.8",
                    "Char": "Cirno",
                    "File": "Touhou128"
                },
                19:{
                    "Title": "Touhou 13 - Ten Desires",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "13/08/2011",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "This one changes gameplay features!!",
                    "Id": 19,
                    "Link": "https://en.touhouwiki.net/images/6/66/Th13cover.jpg",
                    "Cover": "th13.jpg",
                    "Abbr": "TD",
                    "Number": "13",
                    "Char": "Toyosatomimi no Miko",
                    "File": "Touhou13"
                },
                20:{
                    "Title": "Touhou 13.5 - Hopeless Masquerade",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "26/05/2013",
                    "Genre": "Competitive Fighting Game",
                    "Description": "Fighting game wich you don't touch the ground.",
                    "Id": 20,
                    "Link": "https://en.touhouwiki.net/images/d/de/Th135_cover.jpg",
                    "Cover": "th135.jpg",
                    "Abbr": "HRtP",
                    "Number": "13.5",
                    "Char": "Hata no Kokoro",
                    "File": "Touhou135"
                },
                21:{
                    "Title": "Touhou 14 - Double Dealing Character",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "12/08/2013",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "First game to be playable in the west with untranslated game (Based)",
                    "Id": 21,
                    "Link": "https://en.touhouwiki.net/images/d/d7/Th14cover.jpg",
                    "Cover": "th14.jpg",
                    "Abbr": "DDC",
                    "Number": "14",
                    "Char": "Shinmyoumaru Sukuna",
                    "File": "Touhou14"
                },
                22:{
                    "Title": "Touhou 14.3 - Impossible Spell Card",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "11/05/2014",
                    "Genre": "Single-player Puzzle Bullet Hell Shooting Game",
                    "Description": "This one is impossible",
                    "Id": 22,
                    "Link": "https://en.touhouwiki.net/images/3/37/Th143cover.jpg",
                    "Cover": "th143.jpg",
                    "Abbr": "ISC",
                    "Number": "14.3",
                    "Char": "Seija Kijin",
                    "File": "Touhou143"
                },
                23:{
                    "Title": "Touhou 14.5 - Urban Legend in Limbo",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "10/05/2015",
                    "Genre": "Competitive Fighting Game",
                    "Description": "Fifth fighting game!",
                    "Id": 23,
                    "Link": "https://en.touhouwiki.net/images/f/f8/Th145front.jpg",
                    "Cover": "th145.jpg",
                    "Abbr": "ULiL",
                    "Number": "23",
                    "Char": "Sumireki Usami",
                    "File": "Touhou145"
                },
                24:{
                    "Title": "Touhou 15 - Legacy of Lunatic Kingdom",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "14/08/2015",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "Possibly the hardest game in the bullet hell series.",
                    "Id": 24,
                    "Link": "https://en.touhouwiki.net/images/d/d7/Th15front.jpg",
                    "Cover": "th15.jpg",
                    "Abbr": "LoLK",
                    "Number": "15",
                    "Char": "Junko",
                    "File": "Touhou15"
                },
                25:{
                    "Title": "Touhou 15.5 - Antinomy of Common Flowers",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "29/12/2017",
                    "Genre": "Competitive Fighting Game",
                    "Description": "Interesting mechanics in this new fighting game!Also it was released on the nintendo switch",
                    "Id": 25,
                    "Link": "https://en.touhouwiki.net/images/f/f9/TH155front.jpg",
                    "Cover": "th155.jpg",
                    "Abbr": "AoCF",
                    "Number": "15.5",
                    "Char": "Joon Yorogami & Shion Yorogami",
                    "File": "Touhou155"
                },
                26:{
                    "Title": "Touhou 16 - Hidden Star in Four Seasons",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "11/08/2017",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "Tan Cirno?!??!",
                    "Id": 26,
                    "Link": "https://en.touhouwiki.net/images/5/5e/Th16front.jpg",
                    "Cover": "th16.jpg",
                    "Abbr": "HSiFS",
                    "Number": "16",
                    "Char": "Okina Matara",
                    "File": "Touhou16"
                },
                27:{
                    "Title": "Touhou 16.5 - Voilet Detector",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "10/08/2018",
                    "Genre": "Vertical Bullet Hell Photography Shooting Game",
                    "Description": "Photography comes back!!",
                    "Id": 27,
                    "Link": "https://en.touhouwiki.net/images/7/76/Th165cover.jpg",
                    "Cover": "th165.jpg",
                    "Abbr": "VD",
                    "Number": "16.5",
                    "Char": "Sumireko Usami",
                    "File": "Touhou165"
                },
                28:{
                    "Title": "Touhou 17 - Wily Beast and Weakest Creature",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "12/08/2019",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "Youmu is playable character!!",
                    "Id": 28,
                    "Link": "https://en.touhouwiki.net/images/9/90/Th17cover.png",
                    "Cover": "th17.jpg",
                    "Abbr": "WBaWC",
                    "Number": "17",
                    "Char": "Saku Kurokoma & Keiki Haniyasushin & Yachie Kicchou",
                    "File": "Touhou17"
                },
                29:{
                    "Title": "Touhou 17.5 - Sunken Fossil World",
                    "Developer": "Team Shanghai Alice/Twilight Frontier",
                    "Publisher": "Team Shanghai Alice/Twilight Frontier",
                    "Released": "24/10/2022",
                    "Genre": "Horizontal Side-scrolling Bullet Hell Water Action Game",
                    "Description": "This one got some delays and still is a very good one!",
                    "Id": 29,
                    "Link": "https://en.touhouwiki.net/images/f/fa/Th175_cover.jpg",
                    "Cover": "th175.jpg",
                    "Abbr": "SFW",
                    "Number": "17.5",
                    "Char": "Yuuma Toutetsu",
                    "File": "Touhou175"
                },
                30:{
                    "Title": "Touhou 18 - Unconnected Marketeers",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "04/05/2021",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "The ability cards are AWESOME",
                    "Id": 30,
                    "Link": "https://en.touhouwiki.net/images/2/2e/Th18cover.jpg",
                    "Cover": "th18.jpg",
                    "Abbr": "UM",
                    "Number": "18",
                    "Char": "Chimata Tenkyuu",
                    "File": "Touhou18"
                },
                31:{
                    "Title": "Touhou 18.5 - 100th Black Market",
                    "Developer": "Team Shanghai Alice",
                    "Publisher": "Team Shanghai Alice",
                    "Released": "14/08/2022",
                    "Genre": "Vertical Bullet Hell Shooting Game",
                    "Description": "Rogue-like Touhou game!",
                    "Id": 31,
                    "Link": "https://en.touhouwiki.net/images/c/ce/Th185cover.png",
                    "Cover": "th185.jpg",
                    "Abbr": "BM",
                    "Number": "18.5",
                    "Char": "Marisa Kirisame",
                    "File": "Touhou185"
                }
            }

#Print the whole dictionary
#print(TouhouGames)

#Print every game inside the dictionary
#for i in TouhouGames:
#     print(TouhouGames[i])

#Print the keys and values of each game
#for i in TouhouGames:
#    print(TouhouGames[i].keys())
#    print(TouhouGames[i].values())

#Print specific games details like the title.
#print("\n",TouhouGames[6]["Title"])
#print(TouhouGames[6]["Developer"])
#print(TouhouGames[6]["Description"])

#UserInput = input("Select from 1 to 31: ")
#print(TouhouGames[int(UserInput)]["Title"])

# OMG WHO PUT THIS IN HERE IT'S WASTING SO MUCH SPACE WTFFFFFFF
# Oh god i forgot to remove this when i uploaded it. Too late now.
# Also "GamesInfo.py" doesn't serve much purpose honestly.
# #%#(,&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.(&%%&@@@@@@@@@@@@@@@@@@@@@@@@@@@&(*%&&&@@@@@@@@@@@@@@@@@@@@@#######
# @@@* ,####(.&@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@* ,%%###,&@@@@@@@@@@@&*,&%*.. ,***********,. ./&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@* .%####*&@@@@@@@@@@@@*/&*(*.********************,...(&@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@*..%(#%@%@@@@@@@@@@(.,/&# *****************,,,........    .*#@@@@&#(%%(***/#@@@@@@@@@@#*,. .,,,**********///*..,.... 
# @@@*..#%@&@@@@@@@@@@@,(%@@#.,***********************,,,,,*******,, ,******,......(*  ..,,...........,************,......
# @@@*,*@&&@@@@@@@@@@@@&,,%@(.**********,...  .,,**********,,,.............    .. .,********************,,,,,,*****..... *
# @@@/#%#@@@@@@@@@@@@@/ .*%@*,**,  ,**************************************************.   .*********************,...... /@
# @@@@//@@@@@@@@@@@@@&*,##/..,*******************,..****************************************.  ,**************,........&@@
# @@@#(@@@&@@@@@@@@@@@/.,************..********, ******************. ,************ ,*********,.,   .,*******,........ #@&%
# @@@@@@@&@@@@@@@@&/ ,****..*******,.********,...*************. .**   .********. ,*, **********, .   ..,**,.......... ,*&%
# @@@@@@%&@@@@@%..*****,.***,,*****.,*******, . .***********,.. **./(((*.******,  ,* ,,**********. .   .............,.#%#(
# @@@@@@@@@@@(.**..***..**  .,*****,*******  ./(*./********,.  ./***/%&%%(. ,***. . .** .*********. .  .,............(#,..
# @@@@@@@@@&.,*..****,.*. .,***** .**,..  *(/./&@@@/.,***,../(((##&@ç@@@@#/&@@@&#/.,(*.**. .********  ..  ......... #&%%%&@
# @@@@@@@@@(,*, *, ,*,...***.  ,(, .(#%#/ *@@@@@@@@@@&(#&@#*#&@@/  ,.     ./#&@@@@%(((/..*,  ,****, ....  ...... /&%,.*//.
# @@@@@@@@@#,*,,*..,**, .  ,/.            ,%@@@@@@@@@@@@@@@@@@* .   .*///*,       /@@&#/, ..,,  ,* ......  ... (&%#*.#%&@@
# @@@@@@@@@@@@# , .***.  #*.* #@*        ,*. (@@@@@@@@@@@@@@@@@&&@*        /@@&,   *@@@&/.******..,,  ...  .. .(##%%@( %@@
# @@@@@@@@@@@@@%, .  ... #@@@#         .@@@@@&%@@@@@@@@@@@@@@@@@*          %@@@@% ,,@@@@%,.. .,****,. ...  .#%%%%####( #@@
# @@@@@@@@@@@@@@@( .... .%@@#            /%%(  @@@@@@@@@@@@@@@@/             */,   /@@@&#(*   ,*****, ...  ,&%%(.,../&@@@@
# @@@@@@@@@@&/  */####/..#@@%.                .@@@@@@@@@@@@@@@@(                   ,@@@&#/.*(&%#(##%&&/    /@&#(.#&@@@@@&&
# **(%@@&*.#@@@@&,,,,,,/#/%&@@%.             /@@@@@@@@@@@@@@@@@@/                 ,&@&%(*,,,#%/*&@@@@@@@@@&*  ......,/*,,#
# .(@@( #@@@@@@@@@@@&&(*(((@@@@@@#*     *(&@@@@@@@@@@@@@@@@@@@@@@@%,          ./%@@@%*,,,,,*/(%&@@@@@@@@@@@@#.  ...  #@@/#
# @&.*@@@@@@@@@@@@@@@@&,,(@@@@@@@@@@@@@@@@@@@@@@@@@&,.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%(**/&@@@@@@@@@@@@@@@@%/.    ,%*/#&@
# @@*,@@@@@@@@@@@@@@@@@&#//%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.*&@&#*/////*,@@@@@@@@@@@@@@@&#((, #%/(/,%@@
# @&.#@@@@&#/&@@@@@@@@@@@@@@%/*(&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&*,/*#@@@&,,@@@@@@&,/***,.%@@@@@@@@@@@@@@@&(((* (%#%%(.&@
# @&./#&@@@@&@@@@@@@@@@@@@@@@@&&@@@&%%&&#/,*((,,*(&&@@@@@@@@@@@@@@@%#/(#(.,&@@@@@@@&((#&@@@@@@@@@@@@@@@@@@&#(((. ,@@@@@@@@
# @@% /((&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@(,,,,,,/%&(*,**,////, @@@@@%**#@@@@@@@@@@@@@@@@@@@@@&#((((* ,@@@@@@@@@
# @@@@( *((((#%&&@@@@@@@@@@@@@@@@@@@@#.*//#&&@@@@@@@@@@%(#&&%/%@&/**&&&&&( (@@@@@@@@@@@@@@@@@@@@@@&%#(((((((/. .&@@@@@@@@@
# (**&@@@#  */(((((((((((((((*/(#@@@@@%/////(&@@@@@@@@@@@@@@@@@@&/,&@&#%@@@@&&@@@@@&&&&%#(((((((((((((((((,    .#@@@@@@@@@
# *.,(&@@@@@@%*            .,. .,,  ,#&@@&&&%//(&@@@@@@@@@@@@@@@@@@@&/*/*&&%%#(((((((((((((((((((((/*,     ,,,,,..,#@@@@@@
# @@@@@@@@@@@@@@/.   ..,*,.*,. ..,. ..,.    ./(@@@@@@@@@@@@@@@@&%#((((((((*,.    .. .*,              ..,,....**@@@@@@@@@@@
# @@@@@@@@* ///(#%/.   ,%( .,....,,...,*...  ..( /(#######((((((((*  .(#(.,   .*. ....,,...       .,,*&#. .....#@@@@@@@@@@
# @@@@@@@@,.*/////////*/((*,....,**.    .***.,#%( *((((((((((((((. /#%%%#,,***.,     .....,*/####((%&  ..  ... (@@@@@@@@@@
# (@@@@@@@, %//////////*,/////**/(/.*******.*&%%%%(./(((((((/,.*#%%%%&&%%%.*&@@&%#((###(///////////, .. . ./ ..(@@@@@@@@@@
# @@@@@@@@,(*.*/////////////*  ,///*.*****./@@@@@@#*/(#,.#@@@@@@@@@@@@@&,&%//***///*.  *////////*,  ,*  . (@@#&@@@@@@@@@@@
# &@@@@@&,%(,..(///////*. ./////////,,/**,/@@@/.#&&%#(((#%**@@@@@@@@@%,&&(///,,///////////////*  *#(,.   /@@@@@@@@@@@@@@@@
# @@@@@@.%&.%@#...*///////////////**/(#&(,*//*.,&&&&&&&&&&&,..*&@@%//&#//*/////..*/////////*.  .##*.   ,%@@@@@@@@@@@@@@@@&
# @@@@@,%@&@@#.&&**.,*///////////*,,*/////////#*.(&&&&&&&%......*%&/////*,*/////////////,     ,#(    ,&@@@@@@@@@@@@@@@@@@@
# @@@@@#,&@@&&@@%./(   ..///////////////////*..,*//////////////**///////////////////*.     /##*     *@@@@@@@@@@@@@@@@@&%&&
# @@@@@#,&@@@@@/#@&,,/,        .,**/////////////////////////  .**////////////(#/,   .,,,./#%/  .   .@@@@@@@@@@@@@@@@@@@&&@
# @@@@@#.(#&@@@@&,*/,,,,*/######/.     ,.,,,****///////////////////**,..         ,,..(../*,@&.*.%@&,*@@@@@@@@@@@@@@@@&@@%@
# @@@@@#,((((&@@(.      /#(/****((#####((#/.                       .//,**/####/ .,./@,*,&&,&@#.(.(@%#./@@@@@@@@@@%#@@&*(&/
# @@@@@& ((((((#/,,.,,           .(#(/**,***,*(############(*,,,*(#/*(#####(*,./&,,*@@%#@@@@@%.&@#,&%#,.@@@@@@@@@* %@@&,(#
# @@@@@@/.(##(((/, ,,.  .,,,,,,.      .,,,.     .,*///***,...,,*,,*//,          /@@@@@@@@@@@@#.&@&,#%##.&@@@@@@@@@*/@@@%/*
# @@@@@% ,.*((((( .#%%#*.    .**,,,.                                    .,,,,   . %@@@@@@@@#...@@@(,%%#,&@@@@@@@@@%/&@@@#*
# @@@@@/ **       /&%%%%%/#%%,  ..     .,,,,,,,,,,.     .,,,..      .,,.....     .. /&&%#(((((,(@@%.(%#.&@@@@@@@@@@/%@/#@*
# @@@@@***/    *,,@&%%%%####/  ********,((*,,......,,,..,,.      .,,...,*,.......... ..,((((((/.@@@(,#.,@@@@@@@@@@@@&@@@@&
# @@@@@//,/      &&%%%%#%%%%. ,*******./%&&&&&&&&&&&&&&*/&&&&&&&% */****..............,/        %@@&,,.#@@@@@@@@@@@@&@@@
